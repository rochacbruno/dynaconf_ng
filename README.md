# Dynaconf 4.0

## What is Dynaconf

Dynaconf is a configuration management library written in Python, it is designed to provide the following features:

- Environment first config management 
    - Environment variables rules
        - unless you explicitly say it doesn't (e.g: CLI arguments)
    - If not then config maps and settings servers (Vault, Redis, Etcd)
    - If not then fall back to settings.{anyformat} files on the filesystem
    - If not then go with default values
- Schema is optional but can be strict and validated
- Everything is Lazy and it allows interpolations, transformations, parsing
- Pure Python, Django, Flask, FastAPI are supported
- Dependencies are vendored for easy packaging and distribution
- Settings can be layered on multiple environments


## Quick Start

`project/config.py`
```py

from dynaconf import Dynaconf

settings = Dynaconf(
    settings_file="settings.yaml"
)
```

then

`project/app.py`
```py
from project.config import settings
print(settings.NAME)
```

`NAME` will hold the value of one of those

If your CLI app receives arguments it has the highest precedence once you mark it as an `important` key.

```bash
$ myapp.py --key=value
```

Then environment variables will rule over anything else.

```bash
$ export DYNACONF_KEY=value
$ myapp.py
```

Then if there is no environment variable defined, values coming from services such as config maps, Redis, Vault, Etcd and others.

> Assuming redis is an enabled loader for your Dynaconf instance

```bash
$ redis-cli set key value
$ myapp.py
```

> Also can work for Vault, Etcd, k8s config map and any other custom loader.

Then if there is no external service:

> Assuming there is a `settings.yaml` on the local file system.

```yaml
key: value
```
```bash
$ myapp.py
```

Then if there is NO source of configuration, the default values might be used.

```py
# app.py
settings = Dynaconf(key="value")
print(settings.get("key", "default value))
```

> There are some ways to define default values, on Validators, as explicit passed in keyword arguments.

---

Everything explained on https://dynaconf.com works out of the box, no breaking changes (except big / design bug fixes)

---

> **To be NEW in 4.0**

## 💡 Schema and class-based Validation (optional, opt-in)


```py
from dynaconf import Dynaconf, schema

class ServerType(schema.StringType):
    host: str
    port: int

    def read(self, value):
        """Hipotetically take http://foo.bar:5000 """
        host, port = value.rpartition(":")
        self.host = host.strip()
        self.port = int(port.strip())

    def validate(self, settings, value):
        if not value.startswith("http"):
            raise schema.ValidationError("Invalid Server")
```

```py
class MySettings(schema.BaseSettings):
    name: str
    server: ServerType   # Types are composable
    port: int

    class Meta:
        strict = True
        strict_fields = ['name']  # for when wide strict is False
        readonly = ["name"]

    def validate_<field_name>(...):

    def read_<field_name>(...):

    def write_<field_name>(...):
```

then

```py 
settings = Dynaconf(
    settings_file="settings.yaml",
    schema=MySettings
)
```

- Loaders will occur normally, but there will be a de-serialization step based on the schema
- Validation will be performed first using the schema, then fall back to legacy Validators
- Dynaconf Validators will be deprecated in favor of class-based schema
- When `strict=False` (the default) the Schema will be used for validation and parsing, but variables out of the schema will still be loaded
- When `strict=True` only variables defined on the schema will be loaded

## Questions

- Pydantic or purely Python types?
- Refactor or write from scratch?
- Keep Box or replace with ChainMap? (how to do that without breaks)
- YAML must be the preferred format instead of TOML?
- Make TOML parser for envvars optional?


