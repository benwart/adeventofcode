from ..exercise_1 import MappingRange


def test_mapping_range_transform_1():
    r = MappingRange(56, 60, 37)
    assert r.transform(78) == 82
    assert r.transform(43) == 43
    assert r.transform(82) == 86
    assert r.transform(35) == 35


def test_mapping_range_transform_2():
    r = MappingRange(93, 56, 4)
    assert r.transform(78) == 78
    assert r.transform(43) == 43
    assert r.transform(82) == 82
    assert r.transform(35) == 35
