from __future__ import annotations

from server import security_headers


def main() -> None:
    headers = security_headers()
    required = ["content-security-policy", "x-content-type-options", "referrer-policy"]
    missing = [name for name in required if name not in headers]
    if missing:
        raise SystemExit(f"missing headers: {missing}")
    print("ok")


if __name__ == "__main__":
    main()
