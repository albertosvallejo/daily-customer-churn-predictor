import json
import sys
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

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

    def test_explainability_latest_endpoint(self):
        with urlopen(self._url("/explainability/latest?limit=5")) as response:
            self.assertEqual(response.status, 200)
            payload = json.loads(response.read().decode("utf-8"))
        self.assertIn("source_file", payload)
        self.assertIn("records", payload)
        self.assertLessEqual(payload["record_count"], 5)
        self.assertEqual(len(payload["records"]), payload["record_count"])

    def test_coupon_generation_endpoint(self):
        request = Request(
            self._url("/coupons/generate"),
            data=json.dumps(
                {
                    "customer_id": "cust_001",
                    "risk_level": "HIGH",
                    "discount_pct": 25,
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            self.assertEqual(response.status, 201)
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["customer_id"], "cust_001")
        self.assertEqual(payload["risk_level"], "HIGH")
        self.assertRegex(payload["coupon_code"], r"^VIVA-[A-Z0-9]{4}-[A-Z0-9]{4}$")

    def test_coupon_generation_validation(self):
        request = Request(
            self._url("/coupons/generate"),
            data=json.dumps({"customer_id": "cust_001"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as context:
            urlopen(request)
        self.assertEqual(context.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
