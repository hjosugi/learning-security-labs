# 2026 Learning Items: Security Labs

Last verified: 2026-06-20

## Must Learn

### Web application security

- OWASP Top 10 2025 awareness
- authentication and session risks
- access control
- input validation
- secure error handling
- logging without leaking secrets

Projects:

- `labs/local-web-security`
- `labs/auth-session-lab`
- `labs/access-control-lab`

### Security testing workflow

- scope and authorization
- test plan
- safe local environment
- evidence collection
- severity and impact
- remediation notes
- retest checklist

Projects:

- `docs/lab-strategy.md`
- report template

### Defensive tooling

- dependency scanning
- secret scanning
- static analysis
- dynamic testing with ZAP against local apps
- security headers
- TLS configuration checks

Projects:

- `labs/dependency-scanning`
- local ZAP baseline scan notes

### Secure design

- threat modeling
- trust boundaries
- data classification
- abuse cases
- rate limiting
- audit logs
- ASVS-style verification requirements

Projects:

- threat model template
- secure design review checklist

### Reporting and remediation

- finding summary
- severity rationale
- local reproduction
- root-cause explanation
- fix notes
- retest evidence
- regression check

Projects:

- `docs/finding-report-template.md`

## Definition of Done

- Every lab runs locally.
- Every lab has explicit authorization scope.
- Every finding includes remediation.
- No real targets, real credentials, or private data.
- Reports and evidence are ignored by Git unless intentionally sanitized.
