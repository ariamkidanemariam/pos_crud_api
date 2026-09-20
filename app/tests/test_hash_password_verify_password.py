from core.security import hash_password, verify_password


def test_hash_password_returns_different_value():
    password = "mysecretpassword"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_hash_password_returns_non_empty_value():
    password = "mysecretpassword"

    hashed_password = hash_password(password)

    assert hashed_password
    assert isinstance(hashed_password, str)


def test_hash_password_does_not_return_same_hash_twice():
    password = "mysecretpassword"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash


def test_verify_password_returns_true_for_correct_password():
    password = "mysecretpassword"

    hashed_password = hash_password(password)

    assert verify_password(
        password,
        hashed_password,
    ) is True


def test_verify_password_returns_false_for_wrong_password():
    password = "mysecretpassword"

    hashed_password = hash_password(password)

    assert verify_password(
        "wrongpassword",
        hashed_password,
    ) is False


def test_verify_password_returns_false_for_empty_password():
    password = "mysecretpassword"

    hashed_password = hash_password(password)

    assert verify_password(
        "",
        hashed_password,
    ) is False


def test_different_passwords_do_not_verify_against_same_hash():
    password = "mysecretpassword"

    hashed_password = hash_password(password)

    assert verify_password(
        "anotherpassword",
        hashed_password,
    ) is False