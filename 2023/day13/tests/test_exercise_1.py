from pytest import fixture

from ..exercise_1 import Map, horizontal_mirrors, vertical_mirrors


@fixture(scope="function")
def no_mirror_found_map_1() -> Map:
    return Map(
        [
            "...#..........#..",
            "###.###....###.##",
            "##.###.####.###.#",
            "..###.#.##.#.###.",
            "...##.#.##.#.##..",
            "#####........####",
            "..#.#.##..##.#.#.",
            "..#####.##.#####.",
            "...#...####...#..",
            "##..##..##..##..#",
            "....#.##..##.#...",
            "..#.####..####.#.",
            "...##.##..##.##..",
            "..##..........##.",
            ".....#..##..#..#.",
            "###.#........#.##",
            "..#...#.##.#...#.",
        ]
    )


def test_no_mirror_found_map_1(no_mirror_found_map_1: Map) -> None:
    h = horizontal_mirrors(no_mirror_found_map_1)
    v = vertical_mirrors(no_mirror_found_map_1)

    assert h == 1
    assert v is None
