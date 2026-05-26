import json
import logging
import os
import secrets
import threading
from datetime import datetime, timezone
from functools import lru_cache
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import joblib
import pandas as pd

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
COUPON_REGISTRY_PATH = DATA_PROCESSED_DIR / "generated_coupons.jsonl"
COUPON_LOCK = threading.Lock()
COUPON_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
VALID_RISK_LEVELS = {"HIGH", "MEDIUM", "LOW"}
DEFAULT_HOST = os.getenv("CHURN_API_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("CHURN_API_PORT", "62880"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _json_default(value: Any) -> Any:
    if isinstance(value, (pd.Timestamp, datetime)):
        if getattr(value, "tzinfo", None) is None:
            return value.isoformat()
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: Any) -> None:
    body = json.dumps(payload, default=_json_default).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _read_json_body(handler: BaseHTTPRequestHandler) -> dict:
    content_length = int(handler.headers.get("Content-Length", "0"))
    if content_length <= 0:
        raise ValueError("Request body is required")
    raw_body = handler.rfile.read(content_length)
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object")
    return payload


def _latest_explainability_path() -> Path:
    matches = sorted(DATA_PROCESSED_DIR.glob("churn_explainability_*.parquet"))
    if not matches:
        raise FileNotFoundError("No explainability parquet file found")
    return matches[-1]


@lru_cache(maxsize=1)
def _latest_scoring_metadata() -> dict:
    bundle_paths = sorted(MODELS_DIR.glob("churn_scoring_package_*.joblib"), reverse=True)
    if not bundle_paths:
        explainability_path = _latest_explainability_path()
        fallback_tag = explainability_path.stem.split("_")[-1]
        return {
            "run_id": f"canonical_v2c_{fallback_tag}",
            "run_date_tag": fallback_tag,
            "model_version": "unknown",
            "pipeline_tag": "unknown",
            "source_file": explainability_path.name,
        }

    bundle_path = bundle_paths[0]
    bundle = joblib.load(bundle_path)
    metadata = bundle.get("metadata", {}) if isinstance(bundle, dict) else {}
    run_date_tag = metadata.get("run_date_tag", bundle_path.stem.split("_")[-1])
    return {
        "run_id": metadata.get("run_id", f"canonical_v2c_{run_date_tag}"),
        "run_date_tag": run_date_tag,
        "model_version": metadata.get("model_version", metadata.get("version_name", "unknown")),
        "pipeline_tag": metadata.get("pipeline_tag", "unknown"),
        "source_file": bundle_path.name,
    }


def _load_latest_explainability(customer_id: str | None = None, risk_level: str | None = None, limit: int | None = None) -> dict:
    path = _latest_explainability_path()
    df = pd.read_parquet(path)

    if "snapshot_date" in df.columns:
        snapshot_dates = pd.to_datetime(df["snapshot_date"], errors="coerce")
        latest_snapshot = snapshot_dates.max()
        if pd.notna(latest_snapshot):
            df = df.loc[snapshot_dates.eq(latest_snapshot)].copy()
        else:
            latest_snapshot = None
    else:
        latest_snapshot = None

    if customer_id:
        df = df.loc[df["customer_unique_id"].astype(str) == str(customer_id)].copy()

    if risk_level:
        normalized = str(risk_level).upper()
        df = df.loc[df["risk_tier"].astype(str).str.upper() == normalized].copy()

    df = df.sort_values([c for c in ["churn_probability", "customer_unique_id"] if c in df.columns], ascending=[False, True][: len([c for c in ["churn_probability", "customer_unique_id"] if c in df.columns])])

    if limit is not None:
        df = df.head(limit).copy()

    records = df.to_dict(orient="records")
    return {
        "source_file": path.name,
        "latest_snapshot_date": _json_default(latest_snapshot) if latest_snapshot is not None else None,
        "record_count": len(records),
        "generated_at": _utc_now_iso(),
        "records": records,
    }


def _load_existing_coupon_codes() -> set[str]:
    if not COUPON_REGISTRY_PATH.exists():
        return set()
    existing_codes: set[str] = set()
    with COUPON_REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            code = payload.get("coupon_code")
            if isinstance(code, str):
                existing_codes.add(code)
    return existing_codes


def _generate_coupon_code(existing_codes: set[str]) -> str:
    for _ in range(1000):
        block1 = "".join(secrets.choice(COUPON_ALPHABET) for _ in range(4))
        block2 = "".join(secrets.choice(COUPON_ALPHABET) for _ in range(4))
        code = f"VIVA-{block1}-{block2}"
        if code not in existing_codes:
            return code
    raise RuntimeError("Unable to generate a unique coupon code")


def _generate_coupon(payload: dict) -> dict:
    customer_unique_id = str(payload.get("customer_unique_id") or payload.get("customer_id") or "").strip()
    risk_tier = str(payload.get("risk_tier") or payload.get("risk_level") or "").strip().upper()
    discount_pct = payload.get("discount_pct")
    scoring_metadata = _latest_scoring_metadata()

    if not customer_unique_id:
        raise ValueError("customer_unique_id is required")
    if risk_tier not in VALID_RISK_LEVELS:
        raise ValueError("risk_tier must be one of HIGH, MEDIUM, LOW")
    if discount_pct is None:
        raise ValueError("discount_pct is required")

    try:
        discount_value = float(discount_pct)
    except (TypeError, ValueError) as exc:
        raise ValueError("discount_pct must be numeric") from exc

    if not 0 <= discount_value <= 100:
        raise ValueError("discount_pct must be between 0 and 100")

    COUPON_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with COUPON_LOCK:
        existing_codes = _load_existing_coupon_codes()
        coupon_code = _generate_coupon_code(existing_codes)
        created_at = _utc_now_iso()
        coupon_payload = {
            "customer_unique_id": customer_unique_id,
            "risk_tier": risk_tier,
            "discount_pct": int(discount_value) if discount_value.is_integer() else round(discount_value, 2),
            "coupon_code": coupon_code,
            "created_at": created_at,
            "run_id": scoring_metadata["run_id"],
            "run_date_tag": scoring_metadata["run_date_tag"],
            "model_version": scoring_metadata["model_version"],
        }
        with COUPON_REGISTRY_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(coupon_payload, ensure_ascii=False) + "\n")
    return coupon_payload


class ChurnServiceHandler(BaseHTTPRequestHandler):
    server_version = "ChurnService/1.0"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            scoring_metadata = _latest_scoring_metadata()
            _json_response(
                self,
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "service": "daily-customer-churn-api",
                    "timestamp": _utc_now_iso(),
                    "run_id": scoring_metadata["run_id"],
                    "run_date_tag": scoring_metadata["run_date_tag"],
                    "model_version": scoring_metadata["model_version"],
                    "pipeline_tag": scoring_metadata["pipeline_tag"],
                    "source_file": scoring_metadata["source_file"],
                },
            )
            return

        if parsed.path == "/explainability/latest":
            params = parse_qs(parsed.query)
            customer_id = params.get("customer_id", [None])[0]
            risk_level = params.get("risk_level", [None])[0]
            limit_value = params.get("limit", [None])[0]
            limit = None
            if limit_value is not None:
                try:
                    limit = max(1, int(limit_value))
                except ValueError:
                    _json_response(self, HTTPStatus.BAD_REQUEST, {"error": "limit must be an integer"})
                    return
            try:
                payload = _load_latest_explainability(customer_id=customer_id, risk_level=risk_level, limit=limit)
            except FileNotFoundError as exc:
                _json_response(self, HTTPStatus.NOT_FOUND, {"error": str(exc)})
                return
            except Exception as exc:  # pragma: no cover
                logger.exception("Unexpected explainability error")
                _json_response(self, HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
                return
            _json_response(self, HTTPStatus.OK, payload)
            return

        _json_response(self, HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/coupons/generate":
            _json_response(self, HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        try:
            payload = _read_json_body(self)
            response_payload = _generate_coupon(payload)
        except ValueError as exc:
            _json_response(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        except Exception as exc:  # pragma: no cover
            logger.exception("Unexpected coupon generation error")
            _json_response(self, HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return

        _json_response(self, HTTPStatus.CREATED, response_payload)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        logger.info("%s - %s", self.address_string(), format % args)


def create_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), ChurnServiceHandler)


def run_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
    server = create_server(host=host, port=port)
    logger.info("Starting churn service on %s:%s", host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Stopping churn service")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
