# Use a imagem oficial do Python
FROM python:3.10

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo de requerimentos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante da aplicação
COPY . .

# Exponha a porta da aplicação
EXPOSE 8000

# Comando para rodar as migrações e iniciar o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
