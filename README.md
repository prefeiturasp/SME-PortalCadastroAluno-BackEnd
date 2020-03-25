# SME-PortalCadastroAluno-BackEnd
========

Portal do programa de solicitação de uniforme da Secretaria de Educação da cidade de São Paulo.

License: MIT

Versão: 1.1.0


## Release Notes

### 1.1.0 - 25/03/2020
* Consulta aos alunos desatualizados pela Escola
* Painel Gerencial para o Perfil SME
* Painel Gerencial para o Perfil Escola
* Reset de Senha do Sistema para os servidores municipais

### 1.0.0 - 09/03/2020
* Entrada do sistema em produção
* Busca e atualização cadastral dos alunos da rede pelos responsaveis
* Busca e atualização cadastral dos alunos da escola pelo servidor da escola
* Cadastro e Login de Senha do Sistema para os servidores municipais


## Executar o projeto com docker

- Clone o repositório
```console
git clone https://github.com/prefeiturasp/SME-PortalCadastroAluno-BackEnd.git
```

- Entre no diretório criado
```console
cd SME-PortalCadastroAluno-BackEnd
```

- Configure a instância com o .env
```console
cp env_sample .env
```

- Execute o docker usando o docker compose
```console
docker-compose up --build -d
```

- Crie um super usuário no container criado
```console
make create_superuser_docker
```

- Acesse a aplicação usando o browse
```console
http://localhost:8000
```
