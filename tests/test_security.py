from app.core.security import hash_password, verify_password


def test_hash_password_returns_a_different_string():
    password = "testpassword"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password


def test_hash_password_is_not_deterministic():
    password = "testpassword"
    assert hash_password(password) != hash_password(password)


def test_verify_password_correct():
    password = "testpassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    hashed = hash_password("testpassword")
    assert verify_password("wrong-password", hashed) is False