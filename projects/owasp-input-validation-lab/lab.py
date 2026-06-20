from __future__ import annotations

import re


USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,24}$")


def unsafe_query(username: str) -> str:
    return f"select * from users where username = '{username}'"


def validate_username(username: str) -> str:
    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError("username must be 3-24 chars: letters, numbers, underscore")
    return username


def safe_query(username: str) -> tuple[str, tuple[str]]:
    clean = validate_username(username)
    return "select * from users where username = ?", (clean,)


def main() -> None:
    username = "alice_01"
    print("unsafe:", unsafe_query(username))
    print("safe:", safe_query(username))


if __name__ == "__main__":
    main()

