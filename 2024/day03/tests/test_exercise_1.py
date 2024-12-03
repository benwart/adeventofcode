# from pathlib import Path


# from pytest import fixture

# from ..exercise_1 import mul_func, parse_lines


# @fixture(scope="module")
# def data_exmample_1() -> str:
#     example_1 = Path(__file__).parent.parent / "data" / "example_1"
#     return [l for l in parse_lines(example_1)][0]


# def test_regex_example_1(data_exmample_1) -> None:
#     print(data_exmample_1)
#     funcs = mul_func.findall(data_exmample_1)
#     assert len(funcs) > 0
