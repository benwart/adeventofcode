from pathlib import Path

from pytest import fixture

from ..exercise_2 import parse_data, fix_order


@fixture(scope="module")
def data_exmample_1() -> tuple[dict[int, list[int]], list[list[int]]]:
    example_1 = Path(__file__).parent.parent / "data" / "example_1"
    return parse_data(example_1)


def test_fix_order_example_1_manual_3(data_exmample_1) -> None:
    rules = dict[int, list[int]]
    manuals = list[list[int]]
    rules, manuals = data_exmample_1

    fixed: list[int] = fix_order(rules, manuals[5])
    assert fixed == [97, 75, 47, 29, 13]
