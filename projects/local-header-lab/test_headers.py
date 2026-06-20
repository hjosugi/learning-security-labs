from server import security_headers


def test_security_headers_are_present() -> None:
    headers = security_headers()
    assert headers["content-security-policy"] == "default-src 'self'"
    assert headers["x-content-type-options"] == "nosniff"
    assert headers["referrer-policy"] == "no-referrer"


if __name__ == "__main__":
    test_security_headers_are_present()
    print("ok")

