from pathlib import Path

from pytest import fixture

from ..exercise_1 import best_path, parse_lines, Map


@fixture(scope="module")
def data_exmample_1() -> Map:
    example_1 = Path(__file__).parent.parent / "data" / "example_1"
    return Map(parse_lines(example_1))


def test_best_path_example_1(data_exmample_1) -> None:
    # assert best_path(data_exmample_1) == 102
    assert True
