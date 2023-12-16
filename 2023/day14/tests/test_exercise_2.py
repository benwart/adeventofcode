from pathlib import Path

from pytest import fixture

from ..exercise_2 import panel_weight, rotate_panel, shift_rocks, transpose_panel


@fixture(scope="module")
def data_exmample_1() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_1"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


@fixture(scope="module")
def data_exmample_1_shift() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_1_shift"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


@fixture(scope="module")
def data_exmample_2() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_2"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


@fixture(scope="module")
def data_exmample_2_transpose() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_2_transpose"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


@fixture(scope="module")
def data_exmample_2_rotation_1() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_2_rotation_1"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


@fixture(scope="module")
def data_exmample_2_rotation_1_shift() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_2_rotation_1_shift"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


@fixture(scope="module")
def data_exmample_2_cycle_1() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_2_cycle_1"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


@fixture(scope="module")
def data_exmample_2_cycle_2() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_2_cycle_2"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


@fixture(scope="module")
def data_exmample_2_cycle_3() -> tuple[str]:
    example_2 = Path(__file__).parent.parent / "data" / "example_2_cycle_3"
    with open(example_2, "r") as f:
        return tuple(f.read().splitlines())


def test_example_1_shift(data_exmample_1: tuple[str], data_exmample_1_shift: tuple[str]) -> None:
    panel = data_exmample_1
    expected = data_exmample_1_shift
    panel = shift_rocks(panel)

    assert panel == expected

    weight = panel_weight(panel)

    assert weight == 136


def test_rotate_panel_one_turn(data_exmample_2: tuple[str], data_exmample_2_rotation_1: tuple[str]) -> None:
    panel = data_exmample_2
    expected = data_exmample_2_rotation_1
    panel = rotate_panel(panel)

    assert panel == expected


def test_rotate_panel_one_cycle(data_exmample_2: tuple[str]) -> None:
    expected = data_exmample_2
    rotated = data_exmample_2

    for _ in range(4):
        rotated = rotate_panel(rotated)

    assert rotated == expected


def test_transpose_panel(data_exmample_2: tuple[str], data_exmample_2_transpose: tuple[str]) -> None:
    panel = data_exmample_2
    expected = data_exmample_2_transpose

    panel = transpose_panel(panel)

    assert panel == expected


def test_transpose_panel_and_back(data_exmample_2: tuple[str]) -> None:
    panel = data_exmample_2
    expected_2 = data_exmample_2

    for _ in range(2):
        panel = transpose_panel(panel)

    assert panel == expected_2


def test_rotate_panel_shift(
    data_exmample_2: tuple[str],
    data_exmample_2_rotation_1_shift: tuple[str],
) -> None:
    panel = data_exmample_2
    panel = rotate_panel(panel)
    panel = shift_rocks(panel)

    assert panel == data_exmample_2_rotation_1_shift


def test_rotate_panel_1_cycle_with_shift(
    data_exmample_2: tuple[str],
    data_exmample_2_cycle_1: tuple[str],
) -> None:
    shifted = panel = data_exmample_2
    expected = data_exmample_2_cycle_1

    for _ in range(4):
        shifted = shift_rocks(panel)
        panel = rotate_panel(shifted)

    assert panel == expected


def test_rotate_panel_2_cycle_with_shift(
    data_exmample_2: tuple[str],
    data_exmample_2_cycle_2: tuple[str],
) -> None:
    shifted = panel = data_exmample_2
    expected = data_exmample_2_cycle_2

    for _ in range(8):
        shifted = shift_rocks(panel)
        panel = rotate_panel(shifted)

    assert panel == expected


def test_rotate_panel_3_cycle_with_shift(
    data_exmample_2: tuple[str],
    data_exmample_2_cycle_3: tuple[str],
) -> None:
    shifted = panel = data_exmample_2
    expected = data_exmample_2_cycle_3

    for _ in range(12):
        shifted = shift_rocks(panel)
        panel = rotate_panel(shifted)

    assert panel == expected
