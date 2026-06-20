"""Access control lab: Broken Object-Level Authorization (IDOR).

Defensive / educational only. Localhost only. Synthetic data only.

This tiny stdlib HTTP API hosts two synthetic accounts, each owning a set of
synthetic "documents". It deliberately exposes two parallel endpoints so the
same request can be compared side by side:

    GET /vuln/documents/{id}   VULNERABLE: returns ANY document by id and never
                               checks whether the authenticated caller owns it.
                               This is the classic Insecure Direct Object
                               Reference (IDOR) / Broken Object-Level
                               Authorization (BOLA) shape from the OWASP Top 10
                               "Broken Access Control" category.

    GET /safe/documents/{id}   FIXED: looks up the document, then enforces that
                               the document's owner equals the authenticated
                               caller. Returns 403 on an ownership mismatch and
                               404 when the document does not exist, so the two
                               failure modes stay distinct.

Authentication here is intentionally fake: a clearly synthetic bearer token in
the ``Authorization`` header maps to a synthetic account. There are NO real
credentials, NO real users, and NO network egress. Everything is in-memory.

The key teaching point is that authentication ("who are you") is NOT the same as
authorization ("are you allowed to touch THIS object"). The vulnerable endpoint
authenticates the caller and then forgets to authorize the object access.
"""

from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


# ---------------------------------------------------------------------------
# Synthetic data. None of this is real. The tokens are obviously fake on
# purpose so nobody mistakes them for credentials worth protecting.
# ---------------------------------------------------------------------------

# Map a clearly fake bearer token -> synthetic account id.
SYNTHETIC_TOKENS: dict[str, str] = {
    "FAKE-TOKEN-ALICE": "alice",
    "FAKE-TOKEN-BOB": "bob",
}

# Each document records its owner so authorization can be checked server side.
# Document ids are deliberately small sequential integers, which is exactly the
# pattern that makes IDOR easy to discover by enumeration.
SYNTHETIC_DOCUMENTS: dict[int, dict[str, str]] = {
    1: {"owner": "alice", "title": "Alice salary review (synthetic)"},
    2: {"owner": "alice", "title": "Alice vacation request (synthetic)"},
    3: {"owner": "bob", "title": "Bob performance notes (synthetic)"},
    4: {"owner": "bob", "title": "Bob banking memo (synthetic)"},
}


# Route pattern shared by both endpoints; the prefix decides the behavior.
_DOC_ROUTE = re.compile(r"^/(?P<mode>vuln|safe)/documents/(?P<doc_id>\d+)$")


def authenticate(authorization_header: str | None) -> str | None:
    """Resolve a synthetic bearer token to an account id, or None.

    This stands in for real authentication. It only proves *who is calling*.
    It says nothing about *what that caller may access* -- that is the job of
    authorization, which the vulnerable endpoint skips.
    """

    if not authorization_header:
        return None
    parts = authorization_header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return SYNTHETIC_TOKENS.get(parts[1].strip())


def get_document_vulnerable(account: str, doc_id: int) -> tuple[int, dict[str, Any]]:
    """VULNERABLE handler: classic IDOR / BOLA.

    The caller is authenticated (``account`` is set), but the function returns
    the requested document purely by id. It never compares the document owner
    against ``account``, so any authenticated user can read every user's data
    just by changing the id in the URL.
    """

    document = SYNTHETIC_DOCUMENTS.get(doc_id)
    if document is None:
        return 404, {"error": "not found"}
    # BUG (on purpose): no ownership check here.
    return 200, {"id": doc_id, "owner": document["owner"], "title": document["title"]}


def get_document_safe(account: str, doc_id: int) -> tuple[int, dict[str, Any]]:
    """FIXED handler: enforce object-level authorization.

    Look up the object first, then verify the authenticated caller owns it.
    Return 403 on an ownership mismatch and 404 when the object is absent.

    Returning a distinct 403 vs 404 is a deliberate teaching choice for this
    lab so the access-control failure is observable in tests. In a hardened
    production system you may prefer to return 404 for both "missing" and "not
    yours" so the API does not confirm that a foreign id exists at all.
    """

    document = SYNTHETIC_DOCUMENTS.get(doc_id)
    if document is None:
        return 404, {"error": "not found"}
    if document["owner"] != account:
        # Authorization failure: authenticated, but not the owner.
        return 403, {"error": "forbidden"}
    return 200, {"id": doc_id, "owner": document["owner"], "title": document["title"]}


class Handler(BaseHTTPRequestHandler):
    """Routes both /vuln and /safe document reads through the helpers above."""

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        # Defensive header: keep responses from being sniffed as another type.
        self.send_header("x-content-type-options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        match = _DOC_ROUTE.match(self.path)
        if match is None:
            self._send_json(404, {"error": "not found"})
            return

        # Step 1: authenticate the caller (who are you?).
        account = authenticate(self.headers.get("Authorization"))
        if account is None:
            self._send_json(401, {"error": "unauthorized"})
            return

        mode = match.group("mode")
        doc_id = int(match.group("doc_id"))

        # Step 2: route to the vulnerable or fixed authorization behavior.
        if mode == "vuln":
            status, payload = get_document_vulnerable(account, doc_id)
        else:
            status, payload = get_document_safe(account, doc_id)

        self._send_json(status, payload)

    def log_message(self, format: str, *args: Any) -> None:
        # Stay quiet so the lab and tests produce clean output.
        return


def make_server(port: int = 0) -> ThreadingHTTPServer:
    """Create a server bound to localhost only.

    ``port=0`` requests an ephemeral port from the OS, which is what the test
    suite uses so it never collides with anything already listening.
    """

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def run(port: int = 8092) -> None:
    """Run the lab server in the foreground (manual exploration only)."""

    server = make_server(port)
    host, bound_port = server.server_address[0], server.server_address[1]
    print(f"access-control lab listening on http://{host}:{bound_port}")
    print("synthetic tokens: FAKE-TOKEN-ALICE, FAKE-TOKEN-BOB")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
