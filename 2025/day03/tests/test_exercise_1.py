from pytest import mark

from ..exercise_1 import max_jolts_per_bank

example_data = [
    ([9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1], 98),
    ([8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9], 89),
    ([2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8], 78),
    ([8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1], 92),
]


@mark.parametrize("input,expected", example_data)
def test_max_jolts_per_bank(input: list[int], expected: int):
    assert max_jolts_per_bank(input) == expected
