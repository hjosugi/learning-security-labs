# Access Control Lab: Broken Object-Level Authorization (IDOR)

A safe, local, defensive hands-on for the OWASP **Broken Access Control**
category, specifically **Insecure Direct Object Reference (IDOR)** /
**Broken Object-Level Authorization (BOLA)**.

It is built with **only** `python3` standard library (`http.server`) and
**synthetic data**. It serves two parallel endpoints so you can see the broken
shape and the fixed shape side by side:

- `GET /vuln/documents/{id}` returns **any** document by id, ignoring who is
  authenticated (the bug).
- `GET /safe/documents/{id}` checks the document's owner against the
  authenticated caller and returns `403` otherwise (the fix).

Authentication is a clearly fake bearer token (`FAKE-TOKEN-ALICE`,
`FAKE-TOKEN-BOB`). There are no real users, no real credentials, and no network
egress.

Last verified: 2026-06-21

## Authorization scope

- **Target:** this in-repo lab app only, bound to `127.0.0.1` (localhost).
- **Owner:** you, running it on your own machine.
- **Allowed actions:** read the synthetic documents through the two local
  endpoints, run the test suite, run a local OWASP ZAP baseline scan against
  this app.
- **Disallowed actions:** pointing any tooling at third-party systems, public
  IPs, or production domains; using real credentials or tokens.
- **Network boundary:** localhost only. The server binds `127.0.0.1` and uses an
  ephemeral port in tests. No outbound network is used at runtime.
- **Data classification:** synthetic / fake only. Nothing here is real data.
- **Cleanup:** stop the process (Ctrl-C); nothing is persisted to disk.

## Run

```bash
python3 projects/access-control-lab/server.py
```

This starts the lab on `http://127.0.0.1:8092`. Explore the difference with two
synthetic tokens (Alice reading Bob's document id `3`):

```bash
# VULNERABLE: Alice can read Bob's doc (IDOR) -> HTTP 200 with Bob's data
curl -s -H "Authorization: Bearer FAKE-TOKEN-ALICE" \
  http://127.0.0.1:8092/vuln/documents/3

# FIXED: same cross-account attempt is rejected -> HTTP 403
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer FAKE-TOKEN-ALICE" \
  http://127.0.0.1:8092/safe/documents/3

# FIXED: the real owner still succeeds -> HTTP 200
curl -s -H "Authorization: Bearer FAKE-TOKEN-BOB" \
  http://127.0.0.1:8092/safe/documents/3
```

You do **not** need to start the server to run the tests; the test suite starts
its own server in-process on an ephemeral port.

## Test

```bash
python3 -m unittest discover -s projects/access-control-lab -p 'test_*.py'
```

The suite is non-interactive, starts the server in a background thread on an
ephemeral localhost port, asserts against it over real HTTP, shuts it down, and
exits non-zero on any failure.

## Finding write-up

This section matches the repo reporting Definition of Done
(`docs/lab-strategy.md`, `docs/legal-safety-boundaries.md`).

### Summary

The `GET /vuln/documents/{id}` endpoint returns a document purely by its id and
never verifies that the authenticated caller owns it. Any authenticated user can
read any other user's document by incrementing the id in the URL.

### Affected component

- Local lab app `projects/access-control-lab/server.py`
- Route `GET /vuln/documents/{id}`, handler `get_document_vulnerable`

### Severity rationale

**High.** Per the repo severity guide, High applies when "authorization fails in
a direct way." This is a direct object-level authorization failure: an
authenticated user crosses a clear data boundary and reads another account's
data with a trivial, enumerable change (sequential integer ids). No special
tooling, timing, or chaining is required. Confidentiality impact is direct.
(Severity is assigned to this **local lab target only**, never to any real
system.)

### Local reproduction

1. Start the server: `python3 .../access-control-lab/server.py`.
2. As Alice, request Bob's document id `3`:
   `curl -H "Authorization: Bearer FAKE-TOKEN-ALICE" http://127.0.0.1:8092/vuln/documents/3`
3. Observe `HTTP 200` and Bob's document body in the response.

### Root cause

The endpoint conflates **authentication** with **authorization**. It confirms
*who* is calling (a valid token) but never checks *whether that caller may
access this specific object*. The owner field on the document is available but
unused in the vulnerable path. Predictable sequential ids make enumeration
trivial, but the predictability is not the root cause; the missing ownership
check is.

### Fix

`GET /safe/documents/{id}` (`get_document_safe`) loads the object, then enforces
`document.owner == authenticated_account` before returning it. On mismatch it
returns `403 Forbidden`; on a missing object it returns `404 Not Found`, keeping
the two failure modes distinct for teaching. The general rule: **authorize every
object access against the authenticated principal on the server, for every
request.**

### Retest evidence

Run the test suite (above). It proves all three required outcomes:

- `test_vuln_allows_cross_account_read` -> `/vuln` leaks Bob's doc to Alice (200).
- `test_safe_blocks_cross_account_read` -> `/safe` rejects Alice reading Bob (403).
- `test_safe_allows_owner_read` -> `/safe` still serves Bob his own doc (200).

Supporting checks confirm `401` without a token and `404` for a missing object.

### Regression check / out of scope

- **Regression check:** keep `test_safe_blocks_cross_account_read` green for
  every change to the document-read path.
- **Out of scope (intentionally):** write/update/delete authorization,
  function-level (role/admin) access control, rate limiting, audit logging, and
  the production debate of `403` vs `404` for foreign ids. These are listed in
  Exercises as next steps.

## Exercises

1. **Enumerate the boundary.** Write a loop that requests ids `1..4` through
   `/vuln` as Alice and prints which documents leak. Then repeat against `/safe`
   and confirm only Alice's own ids return `200`.
2. **Add a write path and break it the same way.** Add a vulnerable
   `POST /vuln/documents/{id}` that edits any doc, then add a `safe` variant that
   reuses the ownership check. Add tests proving the cross-account write is
   blocked.
3. **Function-level access control.** Add an `admin` account and an
   `/admin/documents` endpoint. Show the broken version (any authenticated user
   reaches it) and the fixed version (role checked server-side). This extends
   the lesson from object-level (BOLA) to function-level (BFLA) authorization.
4. **404 vs 403 trade-off.** Change `/safe` to return `404` for both "missing"
   and "not yours" so the API never confirms a foreign id exists. Update the
   tests and write one sentence on why an enumeration-resistant API might prefer
   this.
5. **Centralize the check.** Refactor the ownership check into a single helper or
   decorator used by every object route, so a new endpoint cannot forget it.
   Argue in a comment why centralized authorization is harder to get wrong than
   per-handler checks.

## Upgrade path

This lab is a stdlib foundation. To swap in the real heavy dynamic-testing tool,
run an **OWASP ZAP baseline scan** against the same local app:

1. Start this lab locally: `python3 .../access-control-lab/server.py`
   (listening on `http://127.0.0.1:8092`).
2. Run ZAP's baseline scan against the local target only. With the official ZAP
   Docker image (added later, not part of this stdlib lab):

   ```bash
   docker run --rm -v "$(pwd):/zap/wrk/:rw" \
     ghcr.io/zaproxy/zaproxy:stable \
     zap-baseline.py -t http://host.docker.internal:8092 \
     -r zap-baseline-report.html
   ```

   The baseline scan is passive: it spiders and inspects responses without
   active attacks, which fits the defensive, localhost-only boundary. Note that
   a passive baseline scan will surface header/config issues but will **not**
   by itself discover IDOR, because object-level authorization requires
   authenticated, owner-aware comparison logic. That gap is exactly why this lab
   exists and why the `unittest` proof is the primary evidence.
3. **Where a finding-report template fits.** Capture the ZAP report under
   `reports/` (Git-ignored per `.gitignore`) and transcribe the access-control
   finding into the repo finding-report template
   (`docs/finding-report-template.md`, planned in `docs/2026-learning-items.md`).
   The "Finding write-up" section above is already shaped to that template:
   summary, affected component, severity rationale, local reproduction, root
   cause, fix, retest evidence, regression check.

ZAP references (canonical roots, see `docs/learning-resources.md`):
<https://www.zaproxy.org/docs/> and the OWASP Top 10 Broken Access Control
category at <https://owasp.org/www-project-top-ten/>.

## Rule

Do not point this lab or any scanner at third-party systems. It is intentionally
scoped to localhost with synthetic data only.
