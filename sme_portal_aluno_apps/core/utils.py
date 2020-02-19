import environ

from config.settings.base import URL_CONFIGS

env = environ.Env()


def url_configs(variable, content):
    return env('REACT_APP_URL') + URL_CONFIGS[variable].format(**content)
