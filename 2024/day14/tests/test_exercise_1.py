from pathlib import Path

from pytest import fixture

from ..exercise_1 import Robot, move, parse_robots


@fixture(scope="module")
def data_exmample_1() -> list[Robot]:
    example_1 = Path(__file__).parent.parent / "data" / "example_1"
    return list(parse_robots(example_1))


def test_move_robot_1_sec(data_exmample_1: list[Robot]):
    robot: Robot = data_exmample_1[10]

    dest: tuple[int, int] = move((11, 7), robot, 1)
    assert dest == (4, 1)


def test_move_robot_2_sec(data_exmample_1: list[Robot]):
    robot: Robot = data_exmample_1[10]

    dest: tuple[int, int] = move((11, 7), robot, 2)
    assert dest == (6, 5)


def test_move_robot_3_sec(data_exmample_1: list[Robot]):
    robot: Robot = data_exmample_1[10]

    dest: tuple[int, int] = move((11, 7), robot, 3)
    assert dest == (8, 2)


def test_move_robot_4_sec(data_exmample_1: list[Robot]):
    robot: Robot = data_exmample_1[10]

    dest: tuple[int, int] = move((11, 7), robot, 4)
    assert dest == (10, 6)


def test_move_robot_5_sec(data_exmample_1: list[Robot]):
    robot: Robot = data_exmample_1[10]

    dest: tuple[int, int] = move((11, 7), robot, 5)
    assert dest == (1, 3)
