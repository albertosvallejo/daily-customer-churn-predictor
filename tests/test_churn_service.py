import json
import os
import sys
import threading
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

_tmpdir = tempfile.TemporaryDirectory()
os.environ["CHURN_DB_URL"] = f"sqlite:///{Path(_tmpdir.name) / 'test_ops.sqlite'}"

from api.churn_service import COUPON_REGISTRY_PATH, create_server


class TestChurnService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._registry_backup = None
        if COUPON_REGISTRY_PATH.exists():
            cls._registry_backup = COUPON_REGISTRY_PATH.read_text(encoding="utf-8")
        COUPON_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        COUPON_REGISTRY_PATH.write_text("", encoding="utf-8")

        cls.server = create_server(host="127.0.0.1", port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)
        if cls._registry_backup is None:
            if COUPON_REGISTRY_PATH.exists():
                COUPON_REGISTRY_PATH.unlink()
        else:
            COUPON_REGISTRY_PATH.write_text(cls._registry_backup, encoding="utf-8")

    def _url(self, path: str) -> str:
        return f"http://127.0.0.1:{self.port}{path}"

    def test_health_endpoint(self):
        with urlopen(self._url("/health")) as response:
            self.assertEqual(response.status, 200)
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["status"], "ok")
        self.assertIn("run_id", payload)
        self.assertIn("run_date_tag", payload)
        self.assertIn("model_version", payload)
        self.assertIn("risk_thresholds", payload)

    def test_explainability_latest_endpoint(self):
        with urlopen(self._url("/explainability/latest?limit=5")) as response:
            self.assertEqual(response.status, 200)
            payload = json.loads(response.read().decode("utf-8"))
        self.assertIn("source_file", payload)
        self.assertIn("records", payload)
        self.assertLessEqual(payload["record_count"], 5)
        self.assertEqual(len(payload["records"]), payload["record_count"])

    def test_thresholds_latest_endpoint(self):
        with urlopen(self._url("/thresholds/latest")) as response:
            self.assertEqual(response.status, 200)
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["status"], "ok")
        self.assertIn("run_id", payload)
        self.assertIn("run_date_tag", payload)
        self.assertIn("risk_thresholds", payload)
        self.assertIn("high_min_score", payload["risk_thresholds"])
        self.assertIn("medium_min_score", payload["risk_thresholds"])

    def test_coupon_generation_endpoint(self):
        request = Request(
            self._url("/coupons/generate"),
            data=json.dumps(
                {
                    "customer_unique_id": "cust_001",
                    "risk_tier": "HIGH",
                    "discount_pct": 25,
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            self.assertEqual(response.status, 201)
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["customer_unique_id"], "cust_001")
        self.assertEqual(payload["risk_tier"], "HIGH")
        self.assertIn("run_id", payload)
        self.assertIn("run_date_tag", payload)
        self.assertRegex(payload["coupon_code"], r"^VIVA-[A-Z0-9]{4}-[A-Z0-9]{4}$")

    def test_coupon_generation_validation(self):
        request = Request(
            self._url("/coupons/generate"),
            data=json.dumps({"customer_unique_id": "cust_001"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as context:
            urlopen(request)
        self.assertEqual(context.exception.code, 400)

    def test_event_health_endpoint(self):
        with urlopen(self._url("/health/events")) as response:
            self.assertEqual(response.status, 200)
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["event_table"], "retention_events")

    def test_onesignal_event_ingestion_endpoint(self):
        body = {
            "events": [
                {
                    "event": "notification.clicked",
                    "event_time": "2026-05-28T14:30:00Z",
                    "external_user_id": "cust_001",
                    "notification_id": "notif-123",
                    "run_date_tag": "20260528",
                }
            ]
        }
        request = Request(
            self._url("/events/onesignal"),
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            self.assertEqual(response.status, 201)
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["received"], 1)
        self.assertEqual(payload["inserted"], 1)
        self.assertEqual(payload["duplicates"], 0)

        with urlopen(self._url("/health/events")) as response:
            health_payload = json.loads(response.read().decode("utf-8"))
        self.assertGreaterEqual(health_payload["event_count"], 1)

    def test_onesignal_event_ingestion_is_idempotent(self):
        body = {
            "events": [
                {
                    "event": "notification.delivered",
                    "event_time": "2026-05-28T14:31:00Z",
                    "external_user_id": "cust_002",
                    "notification_id": "notif-duplicate",
                    "run_date_tag": "20260528",
                }
            ]
        }
        request = Request(
            self._url("/events/onesignal"),
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            first = json.loads(response.read().decode("utf-8"))
        self.assertEqual(first["inserted"], 1)

        request = Request(
            self._url("/events/onesignal"),
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            second = json.loads(response.read().decode("utf-8"))
        self.assertEqual(second["inserted"], 0)
        self.assertEqual(second["duplicates"], 1)


if __name__ == "__main__":
    unittest.main()
