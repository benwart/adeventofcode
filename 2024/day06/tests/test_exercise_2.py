from pathlib import Path

from pytest import fixture

from ..exercise_2 import Map, Point, Result, parse_map, walk_map


@fixture(scope="module")
def data_exmample_1() -> Map:
    example_1 = Path(__file__).parent.parent / "data" / "example_1"
    return parse_map(example_1)


def test_starting_map_example_1(data_exmample_1: Map) -> None:
    _, result = walk_map(data_exmample_1)
    assert result == Result.DONE


def test_adding_obstacle_a_example_1(data_exmample_1: Map) -> None:
    data_exmample_1.add_obstacle(Point(3, 6))
    _, result = walk_map(data_exmample_1)
    assert result == Result.LOOP


def test_adding_obstacle_b_example_1(data_exmample_1: Map) -> None:
    data_exmample_1.add_obstacle(Point(6, 7))
    _, result = walk_map(data_exmample_1)
    assert result == Result.LOOP
