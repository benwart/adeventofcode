from pytest import mark

from ..exercise_2 import invalid_check

invalid_data = [
    11,
    22,
    99,
    111,
    999,
    1010,
    1188511885,
    222222,
    446446,
    38593859,
    565656,
    824824824,
    2121212121,
]

valid_data = [
    2,
    101,
    456,
]


@mark.parametrize("n", invalid_data)
def test_invalid_numbers(n: int):
    assert invalid_check(n)


@mark.parametrize("n", valid_data)
def test_valid_numbers(n: int):
    assert not invalid_check(n)
