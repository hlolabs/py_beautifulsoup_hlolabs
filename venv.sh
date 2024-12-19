#!/bin/bash

# Verificar se o ambiente virtual já existe
if [ ! -d "venv" ]; then
    # Criar o ambiente virtual
    python3 -m venv venv
fi

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar as dependências listadas no requirements.txt
pip install -r requirements.txt

# Manter o ambiente virtual ativado e preservar a coloração do prompt
exec bash --rcfile <(echo "source ~/.bashrc; source venv/bin/activate")
