import pytest
from majava.basic import InInterval, IsType, DictContains, AnyOf, SimilarList


def test_ininterval():
    assert 7 == InInterval(1, 7)
    assert 10 != InInterval(1, 7)
    assert 7 == InInterval(None, 7)
    assert 4 == InInterval(None, 7)
    assert 1 == InInterval(1, None)


def test_istype():
    assert 2 != IsType(str)
    assert 2 == IsType(int, str)
    assert "b" == IsType(int, str)
    assert "b" != IsType(int)
    assert "b" == IsType(str)


def test_dict__plain_match():
    assert {"a": 1, "b": 2} == DictContains({"a": 1, "b": 2})
    assert {"a": 1, "b": 2} == DictContains({"a": 1})
    assert {"a": 1, "b": 2} == DictContains({"b": 2})
    assert {"a": 1, "b": 2} == DictContains({})


def test_anyof():
    assert [8, "a", 3.5] == AnyOf(8)
    assert [8, "a", 3.5] == AnyOf("a")
    assert [8, "a", 3.5] != AnyOf(4)


def test_similarlist():
    assert [8, "a", 3.5] == SimilarList(["a", 8, 3.5])
    assert [8, "a", 3.5] == SimilarList([3.5, 8, "a"])
    assert [8, "a", 3.5] != SimilarList([3.5, 9, "a"])
    assert [8, "a", 3.5] != SimilarList([3.5, 8, "a", 10])


@pytest.mark.parametrize("actual, expected, message", [
    ({"a": 1, "b": 2}, {"a": 1, "b": 3}, "Value 2 at 'b' does not match - 2 != 3"),
    ({"a": 1}, {"b": 1}, "Value {'a': 1} at 'b' does not match - key 'b' not found")
])
def test_dict__plain_mismatch(actual, expected, message):
    with pytest.raises(AssertionError, match=f"\n *{message}$"):
        assert actual == DictContains(expected)


@pytest.mark.parametrize("actual, expected, message", [
    (
        {"a": 1, "b": {"c": {"d": 2, "e": 3}}},
        {"b": {"c": {"e": 4}}},
        "Value 3 at 'b.c.e' does not match - 3 != 4"
    ),
])
def test_dict__nested_mismatch(actual, expected, message):
    with pytest.raises(AssertionError, match=f"\n *{message}$"):
        assert actual == DictContains(expected)
