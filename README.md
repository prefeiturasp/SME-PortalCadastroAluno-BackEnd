# SME-PortalCadastroAluno-BackEnd

## Executar o projeto com docker

- Clone o repositório
```console
git clone https://github.com/prefeiturasp/SME-PortalUniforme-BackEnd.git
```

- Entre no diretório criado
```console
cd SME-PortalUniforme-BackEnd
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

### Criando um token para ter acesso a aplicação 

Após a realização do passo anterior um container com o backend
está executando, então siga os passos abaixo.

- Acesse a aplicação usando o browse
```console
http://localhost:8000/admin
``` 
Digite login e senha do super usuário criado na etapa anterior e assim terá acesso ao admin.
No menu em ```TOKEN DE AUTENTICAÇÃO``` clique em adicionar.
Então selecione o usuário criado anteriormente e clique em salvar.
 
Para requisição na API com rotas ```IsAuthenticated``` é necessário enviar o token
no header.
