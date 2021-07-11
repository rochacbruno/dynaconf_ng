import os
from typing import List, Optional
import pytest
from dynaconf import Dynaconf

os.environ["TEST002_NAME"] = "overwritten by instance arg"
os.environ["TEST002_NUMBER"] = "1313"
os.environ["TEST002_MONEY"] = "42.1"
os.environ["TEST002_ENABLED"] = "1"
os.environ["TEST002_colors"] = '["red", "green", "blue", 32]'
os.environ["TEST002_never_empty"] = 'has a value'


EXPECTED_FOO = "bar"


class MySettings(Dynaconf):
    never_empty: str               # no default value, so it is required
    name: str = "No Name"          # default value so it is optional
    number: Optional[int] = None   # explicit validation type and default value
    money: Optional[float] = None
    enabled: Optional[bool] = None
    colors: Optional[List[str]] = None

    class Config(Dynaconf.Config):
        env_prefix = "TEST002_"


settings = MySettings(
    foo=EXPECTED_FOO,   # arbitrary value
    name="Bruno",       # overrides env vars
)

# __import__("ipdb").set_trace()

# envvars and types


def test_variable_type_casting():
    assert settings.number == 1313
    assert settings.money == 42.1
    assert settings.enabled is True
    assert settings.colors == ["red", "green", "blue", "32"]

# ATTR lookup


def test_variable_lookup_as_attr_lowercase():
    assert settings.foo == EXPECTED_FOO
    assert settings.number == 1313
    assert settings.name == "Bruno"


def test_variable_lookup_as_attr_uppercase():
    assert settings.FOO == EXPECTED_FOO
    assert settings.NUMBER == 1313
    assert settings.NAME == "Bruno"


def test_variable_lookup_as_attr_mixedcase():
    assert settings.fOo == EXPECTED_FOO
    assert settings.nuMBer == 1313
    assert settings.naME == "Bruno"


def test_variable_lookup_for_undefined_attr_raises_error():
    with pytest.raises(AttributeError):
        assert settings.do_not_exist


# KEY lookup


def test_variable_lookup_as_key_lowercase():
    assert settings["foo"] == EXPECTED_FOO
    assert settings["number"] == 1313
    assert settings["name"] == "Bruno"


def test_variable_lookup_as_key_uppercase():
    assert settings["FOO"] == EXPECTED_FOO
    assert settings["NUMBER"] == 1313
    assert settings["NAME"] == "Bruno"


def test_variable_lookup_as_key_mixedcase():
    assert settings["fOo"] == EXPECTED_FOO
    assert settings["numBEr"] == 1313
    assert settings["NaMe"] == "Bruno"


def test_variable_lookup_for_undefined_key_raises_error():
    with pytest.raises(KeyError):
        assert settings["do_not_exsit"]


# .get lookup


def test_variable_lookup_as_get_lowercase():
    assert settings.get("foo") == EXPECTED_FOO
    assert settings.get("number") == 1313
    assert settings.get("name") == "Bruno"


def test_variable_lookup_as_get_uppercase():
    assert settings.get("FOO") == EXPECTED_FOO
    assert settings.get("NUMBER") == 1313
    assert settings.get("NAME") == "Bruno"


def test_variable_lookup_as_get_mixedcase():
    assert settings.get("fOo") == EXPECTED_FOO
    assert settings.get("nuMBer") == 1313
    assert settings.get("nAMe") == "Bruno"


def test_variable_lookup_for_undefined_get_returns_default():
    assert settings.get("do_not_exist") is None
    assert settings.get("do_not_exist1", 4567) == 4567
    assert settings.get("do_not_exist2", "dddd") == "dddd"
