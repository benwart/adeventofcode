from pathlib import Path

from pytest import fixture

from ..exercise_2 import Calibration, combinations, is_calibratable, parse_calibrations


@fixture(scope="module")
def data_exmample_1() -> list[Calibration]:
    example_1 = Path(__file__).parent.parent / "data" / "example_1"
    return list(parse_calibrations(example_1))


def test_calibration_1(data_exmample_1: list[Calibration]) -> None:
    found = is_calibratable(data_exmample_1[1])
    assert found == True


def test_calibration_2(data_exmample_1: list[Calibration]) -> None:
    found = is_calibratable(data_exmample_1[2])
    assert found == False


def test_calibration_3(data_exmample_1: list[Calibration]) -> None:
    found = is_calibratable(data_exmample_1[3])
    assert found == True


def test_combinations() -> None:
    combos: list[str] = []
    for c in combinations("+=!", 1):
        combos.append(c)

    assert combos == ["+", "=", "!"]
