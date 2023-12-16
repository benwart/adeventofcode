from pathlib import Path

from pytest import fixture

from ..exercise_1 import hash_string, parse_init_sequence


@fixture(scope="module")
def data_exmample_1() -> list[int]:
    example_1 = Path(__file__).parent.parent / "data" / "example_1"

    sequeence = parse_init_sequence(example_1)
    return sequeence


def test_hash_string() -> None:
    assert hash_string("HASH") == 52


def test_example_1_init_sequence(data_exmample_1: list[int]) -> None:
    assert sum(data_exmample_1) == 1320
