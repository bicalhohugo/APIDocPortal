# APIDocPortal
Portal de Documentações de Serviços e APIs

# Rodando local

1) Instale o Python 3.6+

2) Instale o pip

3.1) Instale via pip o virtual env: pip install virtualenv

3.2) Crie uma venv na raiz da aplicação pelo comando: virtualenv venv

4) Uma outra alternativa é instalar o venv pelo comando: python -m venv venv

5) Ative a venv criada pelo comando: source venv/bin/activate

6) Instale todos os requisitos através do comando pip: pip install -r requirements.txt

7) Rode o comando: sh startup.sh e sua app será iniciada na porta 8080 no localhost

8) Não menos importante, configure o seu mongodb local ou na nuvem (atlas)

9) Acesse sua APP e rode os comandos abaixo, a partir do 3, pra criar seu usuário padrão

# Rodando no Docker

1) Rode o comando docker-compose up --build -d

2) Acesse "localhost:5000" e o site estará no ar

3) Crie um usuário no mongodb através da conexão ao banco "mongo:27017" do docker

4.1) Exemplo de uma criação após conectar no container: 

4.2) mongo > use apidocs > db.users.insert({ 'name' : 'Admin', 'email' : 'admin@apidocs.com.br', 'password' : '123456', 'status' : 'A', 'profile' : 'A' })

5) Retorne ao site e digite: admin@apidocs.com.br com senha 123456