import environ
import requests
from rest_framework import status


env = environ.Env()
DJANGO_EOL_API_TOKEN = env('DJANGO_EOL_API_TOKEN')
DJANGO_EOL_API_URL = env('DJANGO_EOL_API_URL')


class EOL(object):
    DEFAULT_HEADERS = {'Authorization': f'Token {DJANGO_EOL_API_TOKEN}'}
    DEFAULT_TIMEOUT = 5

    @classmethod
    def cpf_divergente(cls, codigo_eol, cpf):
        response = requests.get(f'{DJANGO_EOL_API_URL}/responsaveis/{codigo_eol}',
                                headers=cls.DEFAULT_HEADERS,
                                timeout=cls.DEFAULT_TIMEOUT)
        if response.status_code == status.HTTP_200_OK:
            cpf_eol = ''
            results = response.json()['results']
            if results and results[0]['responsaveis']:
                cpf_eol_api = results[0]['responsaveis'][0].pop('cd_cpf_responsavel')
                cpf_eol = str(cpf_eol_api)[:-2]
            return cpf != cpf_eol
