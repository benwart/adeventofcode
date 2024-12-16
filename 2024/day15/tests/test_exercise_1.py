from pathlib import Path

from pytest import fixture

from ..exercise_1 import Move, Warehouse, apply, parse_input


@fixture(scope="function")
def data_exmample_1() -> tuple[Warehouse, list[Move]]:
    example_1 = Path(__file__).parent.parent / "data" / "example_1"
    return parse_input(example_1)


@fixture(scope="function")
def data_exmample_2() -> tuple[Warehouse, list[Move]]:
    example_2 = Path(__file__).parent.parent / "data" / "example_2"
    return parse_input(example_2)


def test_example_1_applied(data_exmample_1: tuple[Warehouse, list[Move]]) -> None:
    warehouse: Warehouse
    moves: list[Move]
    warehouse, moves = data_exmample_1
    warehouse = apply(warehouse, moves)

    expected: str = "\n".join(
        [
            "##########",
            "#.O.O.OOO#",
            "#........#",
            "#OO......#",
            "#OO@.....#",
            "#O#.....O#",
            "#O.....OO#",
            "#O.....OO#",
            "#OO....OO#",
            "##########",
        ]
    )

    assert expected == str(warehouse)


def test_example_2_applied(data_exmample_2: tuple[Warehouse, list[Move]]) -> None:
    warehouse: Warehouse
    moves: list[Move]
    warehouse, moves = data_exmample_2
    warehouse = apply(warehouse, moves)

    expected: str = "\n".join(
        [
            "########",
            "#....OO#",
            "##.....#",
            "#.....O#",
            "#.#O@..#",
            "#...O..#",
            "#...O..#",
            "########",
        ]
    )

    assert expected == str(warehouse)
