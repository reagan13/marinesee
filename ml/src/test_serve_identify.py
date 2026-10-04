from serve_identify import identify_payload


def test_empty_body() -> None:
    status, payload = identify_payload(b"")
    assert status == 400
    assert payload["success"] is False


def test_too_large() -> None:
    status, payload = identify_payload(b"x" * (8 * 1024 * 1024 + 1))
    assert status == 413
    assert payload["success"] is False


if __name__ == "__main__":
    test_empty_body()
    test_too_large()
    print("ok")
