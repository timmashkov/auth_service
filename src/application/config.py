from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=False,
    environments=True,
    settings_files=["settings.yml"],
)
