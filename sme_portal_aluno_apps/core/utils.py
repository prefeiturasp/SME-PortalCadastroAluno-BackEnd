import environ

from config.settings.base import URL_CONFIGS

env = environ.Env()


def url_configs(variable, content):
    return env('REACT_APP_URL') + URL_CONFIGS[variable].format(**content)


def ofuscar_email(email):
    m = email.split('@')
    return f'{m[0][0]}{"*" * (len(m[0]) - 2)}{m[0][-1]}@{m[1]}'
