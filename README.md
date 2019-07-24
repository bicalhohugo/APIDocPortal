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

8) Não menos importante, configure o seu mongodb local ou na nuvem (atlas) através do arquivo config/properties.config

9) Execute os passos a partir do 3, descritos abaixo para acessar o site

# Rodando no Docker

1) Instale o Docker e o docker-compose no seu ambiente

2) Rode o comando docker-compose up --build -d para efetuar o build da imagem e subir o compose

3) Acesse "localhost:5000" e o site estará no ar e conectado ao mongodb

4) Crie um usuário admin padrão acessando a rota "locahost:5000/configuration/seed"

5) Retorne ao site e digite: admin@apidocs.com.br com senha: admin