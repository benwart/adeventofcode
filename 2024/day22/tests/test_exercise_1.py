from ..exercise_1 import mix, next_secret, nth_secret, prune


def test_mix_example() -> None:
    result: int = mix(42, 15)
    assert result == 37


def test_prune_example() -> None:
    result: int = prune(100000000)
    assert result == 16113920


def test_next_secret_123() -> None:
    secrets: list[int] = []
    secret: int = 123
    for _ in range(10):
        secret = next_secret(secret)
        secrets.append(secret)

    expected: list[int] = [
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]

    assert secrets == expected


def test_nth_secret_1() -> None:
    secret: int = nth_secret(1, 2000)
    assert secret == 8685429


def test_nth_secret_10() -> None:
    secret: int = nth_secret(10, 2000)
    assert secret == 4700978


def test_nth_secret_100() -> None:
    secret: int = nth_secret(100, 2000)
    assert secret == 15273692


def test_nth_secret_2024() -> None:
    secret: int = nth_secret(2024, 2000)
    assert secret == 8667524
