import pytest
from dynaconf import Dynaconf

EXPECTED_FOO = "bar"


settings = Dynaconf(
    foo=EXPECTED_FOO
)


# ATTR lookup


def test_variable_lookup_as_attr_lowercase():
    assert settings.foo == EXPECTED_FOO


def test_variable_lookup_as_attr_uppercase():
    assert settings.FOO == EXPECTED_FOO


def test_variable_lookup_as_attr_mixedcase():
    assert settings.fOo == EXPECTED_FOO


def test_variable_lookup_for_undefined_attr_raises_error():
    with pytest.raises(AttributeError):
        assert settings.do_not_exist


# KEY lookup


def test_variable_lookup_as_key_lowercase():
    assert settings["foo"] == EXPECTED_FOO


def test_variable_lookup_as_key_uppercase():
    assert settings["FOO"] == EXPECTED_FOO


def test_variable_lookup_as_key_mixedcase():
    assert settings["fOo"] == EXPECTED_FOO


def test_variable_lookup_for_undefined_key_raises_error():
    with pytest.raises(KeyError):
        assert settings["do_not_exsit"]


# .get lookup


def test_variable_lookup_as_get_lowercase():
    assert settings.get("foo") == EXPECTED_FOO


def test_variable_lookup_as_get_uppercase():
    assert settings.get("FOO") == EXPECTED_FOO


def test_variable_lookup_as_get_mixedcase():
    assert settings.get("fOo") == EXPECTED_FOO


def test_variable_lookup_for_undefined_get_returns_default():
    assert settings.get("do_not_exist") is None
    assert settings.get("do_not_exist1", 4567) == 4567
    assert settings.get("do_not_exist2", "dddd") == "dddd"
