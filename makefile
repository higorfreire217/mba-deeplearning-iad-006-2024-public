# Makefile

# Nome da imagem Docker
IMAGE_NAME = xboost-api

# Comando para construir a imagem Docker
build:
	docker build -t $(IMAGE_NAME) .

# Comando para executar a imagem Docker
run:
	docker run -d --name $(IMAGE_NAME) -p 8000:8000 $(IMAGE_NAME)