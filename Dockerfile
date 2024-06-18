# Usar a imagem base do Python
FROM python:3.8-slim

# Instalar as dependências necessárias
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo requirements.txt e instalar as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instalar o Locust
RUN pip install locust

# Copiar o restante do código da aplicação
COPY . .

# Copiar os scripts wait-for-it.sh e start.sh para o diretório /scripts
COPY scripts/wait-for-it.sh /scripts/wait-for-it.sh
COPY scripts/start.sh /scripts/start.sh
RUN chmod +x /scripts/wait-for-it.sh /scripts/start.sh

# Copiar o arquivo .env para a imagem Docker
# COPY .env.example .env

# Definir a variável de ambiente para o Flask
ENV FLASK_APP=create_app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expor a porta 5000
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["/scripts/wait-for-it.sh", "db:3306", "--", "/scripts/start.sh"]
