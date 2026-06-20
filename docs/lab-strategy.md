# Lab Strategy

Last verified: 2026-06-20

## Approach

Security labs should teach defensive understanding, not unsafe behavior.

Use this loop:

1. define local scope
2. create or run intentionally vulnerable behavior
3. observe the weakness
4. fix the weakness
5. write a short report
6. add a regression test or checklist

## Lab Types

| Lab | Purpose |
| --- | --- |
| local web security | understand common web risks safely |
| auth/session lab | learn cookies, sessions, rotation, logout, CSRF |
| access-control lab | learn object-level and function-level authorization |
| dependency scanning | learn supply-chain hygiene |
| security headers | learn browser-facing hardening |
| threat modeling | learn design review before code |

## Tooling

- OWASP WSTG for test structure
- OWASP ASVS for verification requirements
- OWASP ZAP for local dynamic testing
- language-native dependency scanners
- GitHub secret scanning and dependency alerts where available

## Finding Quality Bar

A lab is not done when a weakness is observed. It is done when the defensive lesson is clear.

Each finding should include:

- the exact local target and route/component
- why the behavior matters
- minimum reproduction steps
- affected data or capability
- root cause
- fix
- retest result
- one regression check or checklist item

## Severity Notes

Use severity to prioritize learning, not to dramatize a lab.

| Severity | Use it when |
| --- | --- |
| Low | the issue is mostly hardening or defense-in-depth |
| Medium | a realistic user or data boundary can be crossed in the local app |
| High | authentication, authorization, or sensitive data protection fails in a direct way |
| Critical | a local lab intentionally demonstrates full compromise of the lab target |

Do not assign severity to real third-party systems from this repo.
