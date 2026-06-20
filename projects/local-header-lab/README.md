# Local Header Lab

A defensive localhost-only lab for checking basic HTTP security headers.

## Run The Check

```bash
python3 projects/local-header-lab/check.py
```

The checker verifies the expected defensive header policy without opening a socket.

To run the local server manually:

```bash
python3 projects/local-header-lab/server.py
```

## Rule

Do not point this lab at third-party systems. It is intentionally scoped to localhost.
