# Learning Security Labs

Ethical hacking, secure coding, web security testing, threat modeling, and defensive security labs.

Last verified: 2026-06-21

## Development Environment

If Python is missing locally, enter the Nix shell:

```bash
nix develop
```

## Runnable Starter Project

Run the localhost-only defensive header lab:

```bash
python3 projects/local-header-lab/check.py
python3 projects/local-header-lab/test_headers.py
```

## Target Hands-On Projects

OWASP input validation:

```bash
python3 projects/owasp-input-validation-lab/lab.py
python3 projects/owasp-input-validation-lab/test_lab.py
```

Access control (Broken Object-Level Authorization / IDOR):

```bash
python3 projects/access-control-lab/server.py
python3 -m unittest discover -s projects/access-control-lab -p 'test_*.py'
```

Keep these labs local and defensive: demonstrate the vulnerable shape, then prove the safe version.

See `docs/learning-resources.md` for curated primary sources.

## Safety Boundary

This repository is for authorized, local, educational security practice only.

Allowed:

- local vulnerable training apps
- your own applications
- intentionally created lab environments
- defensive testing and verification
- secure coding notes

Not allowed:

- scanning or attacking third-party systems
- bypassing access controls on real services
- credential theft
- persistence, stealth, or malware
- instructions for real-world abuse

## What This Repo Teaches

This repo is for learning attacker-informed defensive engineering without crossing authorization boundaries.

Each lab should make these parts explicit:

- authorization scope
- target environment
- test objective
- evidence to collect
- expected finding format
- remediation
- verification after the fix
- what is intentionally out of scope

## Learning Path

1. Security mindset and legal boundaries
2. OWASP Top 10 awareness
3. OWASP Web Security Testing Guide workflow
4. Authentication and session testing in local labs
5. Input validation and injection prevention
6. Access control testing
7. Dependency and secret scanning
8. Threat modeling and secure design reviews
9. Reporting: finding, impact, reproduction, remediation

## Lab Rules

- Default target is `localhost`.
- Prefer intentionally vulnerable training apps or tiny apps created inside this repo.
- Tool output should be trimmed to the useful evidence, not dumped wholesale.
- No real credentials, real tokens, production domains, or private targets.
- Each lab must include a defensive fix or verification step.

## Planned Structure

```text
labs/
  local-web-security/
  auth-session-lab/
  access-control-lab/
  dependency-scanning/
docs/
  2026-learning-items.md
  lab-strategy.md
  legal-safety-boundaries.md
  repository-profile.md
```

## What Belongs Elsewhere

- general platform security checklists belong in `learning-platform-engineering`
- production incident/runbook notes do not belong in a public lab repo
- P2P abuse-resistance design belongs in `learning-platform-engineering`
- backend implementation fixes can be mirrored in `learning-backend-ddd`

## First Milestones

1. Add a local vulnerable web lab with a clear legal/scope statement.
2. Add ZAP baseline scanning against localhost only.
3. Add an auth/session lab.
4. Add an access-control lab.
5. Add dependency and secret scanning examples.
6. Add a finding report template.

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- ZAP documentation: https://www.zaproxy.org/docs/
