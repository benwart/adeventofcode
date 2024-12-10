from ..exercise_1 import Point, Trail


def test_point_hash_match() -> None:
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p1h = hash(p1)
    p2h = hash(p2)
    assert hash(p1) == hash(p2)


def test_point_hash_mismatch() -> None:
    p1 = Point(1, 2)
    p2 = Point(1, 3)
    p1h = hash(p1)
    p2h = hash(p2)
    assert hash(p1) != hash(p2)


def test_trail_hash_match() -> None:
    t1 = Trail([Point(2, 0), Point(0, 3)])
    t2 = Trail([Point(2, 0), Point(0, 3)])
    t1h = hash(t1)
    t2h = hash(t2)
    assert hash(t1) == hash(t2)


def test_trail_hash_mismatch() -> None:
    t1 = Trail([Point(1, 2), Point(1, 3)])
    t2 = Trail([Point(1, 2), Point(1, 4)])
    t1h = hash(t1)
    t2h = hash(t2)
    assert hash(t1) != hash(t2)


def test_trails_in_set_dedupe() -> None:
    t1 = Trail([Point(1, 2), Point(1, 3)])
    t2 = Trail([Point(1, 2), Point(1, 3)])
    s = {t1, t2}
    assert len(s) == 1


def test_trails_in_set_diff() -> None:
    t1 = Trail([Point(1, 2), Point(1, 3)])
    t2 = Trail([Point(1, 2), Point(1, 4)])
    s = {t1, t2}
    assert len(s) == 2
