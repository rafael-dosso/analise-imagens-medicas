# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt (que contém as dependências) para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o contêiner
COPY . .

RUN chmod +x /app/start.sh

# Defina o comando para rodar o programa (ajuste "app.py" conforme necessário)
CMD ["/app/start.sh"]
