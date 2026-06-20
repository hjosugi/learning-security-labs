"""Non-interactive tests for the access control (IDOR / BOLA) lab.

These tests start the lab server IN-PROCESS on an ephemeral localhost port in a
background thread, exercise both endpoints over real HTTP, then shut it down.
A human never has to start a server. The suite exits non-zero on any failure.

It proves two things:

1. The vulnerability is real: account "alice" can read account "bob"'s document
   through ``/vuln/documents/{id}`` (HTTP 200 with bob's data).
2. The fix works: the same cross-account attempt through ``/safe/documents/{id}``
   is rejected with HTTP 403, while bob's own request still succeeds with 200.
"""

from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request

from server import make_server


# Synthetic tokens that mirror server.SYNTHETIC_TOKENS. Clearly fake.
ALICE = "FAKE-TOKEN-ALICE"
BOB = "FAKE-TOKEN-BOB"

# Document id 3 is owned by bob (see server.SYNTHETIC_DOCUMENTS).
BOB_DOC_ID = 3


class AccessControlLabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # port=0 -> the OS assigns a free ephemeral port, bound to 127.0.0.1.
        cls.server = make_server(port=0)
        host, port = cls.server.server_address[0], cls.server.server_address[1]
        cls.base_url = f"http://{host}:{port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def _get(self, path: str, token: str | None) -> tuple[int, dict]:
        request = urllib.request.Request(self.base_url + path, method="GET")
        if token is not None:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            # urllib raises on 4xx/5xx; capture the status and body for asserts.
            try:
                return error.code, json.loads(error.read().decode("utf-8"))
            finally:
                error.close()

    # --- proof of the vulnerability ---------------------------------------

    def test_vuln_allows_cross_account_read(self) -> None:
        # Alice authenticates with her own token but reads BOB's document.
        status, body = self._get(f"/vuln/documents/{BOB_DOC_ID}", token=ALICE)
        self.assertEqual(status, 200, "IDOR: vulnerable endpoint should leak the doc")
        self.assertEqual(body["owner"], "bob")
        self.assertIn("Bob", body["title"])

    # --- proof of the fix --------------------------------------------------

    def test_safe_blocks_cross_account_read(self) -> None:
        # Same cross-account attempt, but against the fixed endpoint.
        status, body = self._get(f"/safe/documents/{BOB_DOC_ID}", token=ALICE)
        self.assertEqual(status, 403, "fix: cross-account read must be forbidden")
        self.assertEqual(body["error"], "forbidden")

    def test_safe_allows_owner_read(self) -> None:
        # The legitimate owner still gets a 200 from the fixed endpoint.
        status, body = self._get(f"/safe/documents/{BOB_DOC_ID}", token=BOB)
        self.assertEqual(status, 200, "fix: owner must still be able to read")
        self.assertEqual(body["owner"], "bob")

    # --- supporting authorization behavior --------------------------------

    def test_missing_token_is_unauthorized(self) -> None:
        # No authentication at all -> 401 on both endpoints.
        for mode in ("vuln", "safe"):
            status, _ = self._get(f"/{mode}/documents/{BOB_DOC_ID}", token=None)
            self.assertEqual(status, 401, f"{mode}: missing token must be 401")

    def test_safe_missing_doc_is_not_found(self) -> None:
        # Unknown id -> 404 (distinct from the 403 ownership failure).
        status, _ = self._get("/safe/documents/999", token=ALICE)
        self.assertEqual(status, 404, "fix: unknown doc must be 404, not 403")


if __name__ == "__main__":
    unittest.main()
