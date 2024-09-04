# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o restante do código da aplicação para o contêiner
COPY . .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Defina o comando para rodar o programa (ajuste "app.py" conforme necessário)
CMD ["python", "src/main.py"]
