import os

from dynaconf import Dynaconf, SubModel


os.environ["TEST003_SERVER"] = '{"host": "localhost", "port": 8080}'


class ServerType(SubModel):
    host: str = None
    port: int = None


class Settings(Dynaconf):
    server: ServerType = ServerType()

    class Config(Dynaconf.Config):
        env_prefix = "TEST003_"


settings = Settings()


def test_dot_dunder_lookup():
    """Test that we can lookup a value from a dot-separated key"""
    assert settings.server.port == 8080


def test_dot_dunder_lookup_upper_case():
    """Test that we can lookup a value from a dot-separated key"""
    assert settings.SERVER.port == 8080


def test_dot_dunder_lookup_upper_case_nested():
    """Test that we can lookup a value from a dot-separated key"""
    assert settings.SERVER.PORT == 8080
    assert settings.server.PORT == 8080
    assert settings.SERVER.port == 8080


def test_dot_dunder_lookup_with_get():
    """Test that we can lookup a value from a dot-separated key"""
    assert settings.get("server.host") == "localhost"
    assert settings.get("server__host") == "localhost"
    assert settings.get("server.port") == 8080
    assert settings.get("server__port") == 8080
    assert settings.get("SERVER__port") == 8080
    assert settings.get("SERVER__PORT") == 8080
    assert settings.get("SERVER__Port") == 8080
