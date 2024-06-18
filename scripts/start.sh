#!/bin/sh

# Verificar a existência do diretório migrations
if [ ! -d "migrations" ]; then
  echo "Inicializando as migrações..."
  flask db init
fi

# Criar uma migração inicial, se não existir
if [ ! -f "migrations/env.py" ]; then
  echo "Criando arquivo de migração inicial..."
  flask db migrate -m "initial migration"
fi

# Executar as migrações
echo "Executando flask db upgrade..."
flask db upgrade

# Iniciar o servidor Flask
echo "Iniciando o servidor Flask..."
flask run --host=0.0.0.0
