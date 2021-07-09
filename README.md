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
from dynaconf import Dynaconf

class MySettings(Dynaconf):
    server: str         # no default value so it is required
    port: int = 8080    # type validation and default value provided
    options: List[str] = ["default"]  # Typed defaults

    class Config(Dynaconf.Config):
        envvar_prefix = "MYAPP_"



settings = MySettings()
```
