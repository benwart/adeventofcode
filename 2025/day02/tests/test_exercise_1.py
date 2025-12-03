from pytest import mark

from ..exercise_1 import invalid_check

invalid_data = [
    11,
    22,
    99,
    1010,
    1188511885,
    222222,
    446446,
    38593859,
]


@mark.parametrize("n", invalid_data)
def test_invalid_numbers(n: int):
    assert invalid_check(n)
