from lab import safe_query, unsafe_query, validate_username


def test_unsafe_query_demonstrates_risk() -> None:
    query = unsafe_query("a' or '1'='1")
    assert "or" in query


def test_safe_query_rejects_untrusted_shape() -> None:
    try:
        validate_username("a' or '1'='1")
    except ValueError:
        pass
    else:
        raise AssertionError("expected validation error")


def test_safe_query_uses_parameters() -> None:
    query, params = safe_query("alice_01")
    assert query.endswith("username = ?")
    assert params == ("alice_01",)


if __name__ == "__main__":
    test_unsafe_query_demonstrates_risk()
    test_safe_query_rejects_untrusted_shape()
    test_safe_query_uses_parameters()
    print("ok")

