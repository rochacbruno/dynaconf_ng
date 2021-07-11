from pathlib import Path
from typing import Any, Optional, Union

from pydantic import BaseModel, BaseSettings, Extra, Field


SettingsField = Field  # noqa
"""Extendable settings field"""


class BaseDynaconf:
    """Extendable model"""

    def _d_get_value(self, key: str, default: Any = None) -> Any:
        """Get a setting value.

        :param key: The setting key
        :param default: The default value to return if the setting is not found
                        or an exception to raise if the setting is not found.
        :return: The setting value

        - This is called only when the attribute is not found in the instance.
        - if the key has `__` in it, it is treated as a compound setting.
          (__ will be replaced with . to get the key)
        - If the key is a dot separated path, e.g. 'a.b.c',
          it will be split into a list of keys and passed to
          d_get_value for recursive nesting lookup.
        - try to get a swaped case A -> b, B -> a, etc.
        - try to get a lower case version of the key
        - try to get an uppercase version of the key
        - if the final value is a callable it will be called with the
          key + settings instance as arguments.

        """
        if "__" in key or "." in key:
            key = key.replace("__", ".")
            head, *tail = key.split(".")
            return self._d_get_value(
                head, default
            )._d_get_value(
                ".".join(tail), default
            )

        for lookup_key in (
            key.swapcase(),
            key.lower(),
            key.upper(),
        ):
            try:
                return self.__getattribute__(lookup_key)
            except AttributeError:
                continue

        if issubclass(default, Exception):
            raise default(
                f"'{self.__class__.__name__}' object has no attribute '{key}'"
            )

        return default(key, self) if callable(default) else default

    def __getattr__(self, name: str) -> Any:
        """Get a setting value by its attribute name."""
        return self._d_get_value(name, default=AttributeError)

    def __getitem__(self, key: str) -> Any:
        """Get a setting value by its key name (simulate a dictionary).

        try to get the get as an attribute as it is
        if an exception is raised then try the get_value lookup.
        """
        try:
            return getattr(self, key)
        except AttributeError:
            return self._d_get_value(key, default=KeyError)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value by its key name.

        Delegate to __getitem__ to simulate a dictionary.

        :param key: The setting key
        :param default: The default value to return if the setting is not found
        :return: The setting value
        """
        try:
            return self[key]
        except KeyError:
            return default


class SubModel(BaseDynaconf, BaseModel):
    """A Type for compound settings.

    Represents a Dict under a Dynaconf object.
    """


class Dynaconf(BaseDynaconf, BaseSettings):
    """Settings Management."""

    def __init__(
        __pydantic_self__,
        _env_file: Union[Path, str, None] = None,
        _env_file_encoding: Optional[str] = None,
        _secrets_dir: Union[Path, str, None] = None,
        **values: Any
    ) -> None:
        super().__init__(
            _env_file=_env_file,
            _env_file_encoding=_env_file_encoding,
            _secrets_dir=_secrets_dir,
            **values
        )

    class Config(BaseSettings.Config):
        """Settings Configuration."""
        env_prefix = "DYNACONF_"
        env_file = None
        env_file_encoding = 'utf-8'
        secrets_dir = None
        validate_all = True
        extra = Extra.allow
        arbitrary_types_allowed = True
        case_sensitive = False

    __config__: Config  # type: ignore
