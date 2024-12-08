from ..exercise_2 import Point, repeat_offset_point


def test_repeat_offset_point_a() -> None:
    a: Point = Point(0, 0)
    b: Point = Point(3, 1)

    antinodes: list[Point] = []
    iter = repeat_offset_point(b, a)
    for _ in range(2):
        antinodes.append(next(iter))

    assert antinodes == [Point(6, 2), Point(9, 3)]


def test_repeat_offset_point_b() -> None:
    a: Point = Point(0, 0)
    b: Point = Point(1, 2)

    antinodes: list[Point] = []
    iter = repeat_offset_point(b, a)
    for _ in range(3):
        antinodes.append(next(iter))

    assert antinodes == [Point(2, 4), Point(3, 6), Point(4, 8)]
