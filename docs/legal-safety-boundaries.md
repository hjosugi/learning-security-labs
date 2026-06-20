# Legal and Safety Boundaries

Last verified: 2026-06-20

## Non-Negotiable Rules

- Test only systems you own or have explicit written permission to test.
- Keep labs local by default.
- Do not publish working exploit chains against real services.
- Do not collect, store, or transmit third-party credentials.
- Do not include persistence, stealth, malware, or evasion content.
- Do not run scans against public IPs or domains from this repo.

## Lab Scope Template

Each lab should define:

- target
- owner
- allowed actions
- disallowed actions
- network boundary
- data classification
- cleanup procedure

## Reporting Template

Each finding should include:

- summary
- affected component
- local reproduction steps
- impact
- root cause
- remediation
- retest result

## Public Repository Checklist

Before committing lab material, confirm:

- target is local or intentionally created for the lab
- no real hostnames, IPs, tokens, cookies, or user data are included
- screenshots and logs are sanitized
- exploit detail is limited to what is needed to understand the defensive fix
- remediation and retest are included
- generated reports are either ignored by Git or intentionally sanitized
