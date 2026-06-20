# Further learning resources

Curated, canonical primary sources for this repo's named learning area:
**access control / Broken Object-Level Authorization (IDOR)** and the wider
defensive web-security workflow. Localhost-only, defensive, educational.

Last verified: 2026-06-21

## Access control and the OWASP Top 10

- **OWASP Top 10** — <https://owasp.org/www-project-top-ten/>
  The canonical web risk list. "Broken Access Control" is the category this
  access-control lab demonstrates; start here for definitions and references.

- **OWASP API Security Top 10** — <https://owasp.org/www-project-api-security/>
  Defines API1 Broken Object Level Authorization (BOLA) and API5 Broken
  Function Level Authorization (BFLA). This is the precise vocabulary for the
  IDOR shape in this lab and its function-level follow-up exercise.

- **OWASP Cheat Sheet Series** — <https://cheatsheetseries.owasp.org/>
  Concise, authoritative remediation guidance, including the Authorization
  Cheat Sheet. Maps directly to the "enforce ownership on every object access"
  fix used here.

## Security testing workflow

- **OWASP Web Security Testing Guide (WSTG)** — <https://owasp.org/www-project-web-security-testing-guide/>
  The standard methodology for structuring tests, including the authorization
  testing section. Use it to shape evidence and reproduction steps.

- **OWASP Application Security Verification Standard (ASVS)** — <https://owasp.org/www-project-application-security-verification-standard/>
  Verification requirements (access control chapter) that turn "looks fixed"
  into checkable, testable controls. Pairs with the regression test idea.

## Dynamic testing tool (upgrade path)

- **OWASP ZAP documentation** — <https://www.zaproxy.org/docs/>
  Official docs for the ZAP baseline scan referenced in the lab's Upgrade path.
  Explains passive vs active scanning and why a baseline scan stays defensive.

## Standards and references

- **MITRE CWE** — <https://cwe.mitre.org/>
  CWE-639 (Authorization Bypass Through User-Controlled Key) and CWE-285
  (Improper Authorization) are the formal weakness ids for IDOR/BOLA. Useful
  for precise finding write-ups.

- **NIST Computer Security Resource Center** — <https://csrc.nist.gov/>
  Authoritative definitions and access-control guidance (e.g. SP 800-53 access
  control family) for grounding severity and remediation language.

## Python standard library (implementation)

- **Python `http.server` docs** — <https://docs.python.org/3/library/http.server.html>
  The stdlib module this lab is built on; explains `BaseHTTPRequestHandler` and
  the threading server used with an ephemeral localhost port.

## Books

- *The Web Application Hacker's Handbook* (Stuttard & Pinto) — covers access
  control testing and IDOR in depth; the classic primary reference for the
  manual testing mindset behind this lab.
- *Real-World Bug Hunting* (Peter Yaworski) — practitioner-level explanations of
  IDOR/BOLA findings and how owner checks fail in practice.
