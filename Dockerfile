FROM python:3.11-slim

WORKDIR /app

# Salin dan install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin seluruh file
COPY . .

# Port
ENV PORT=8080

# Run aplikasi
CMD exec gunicorn --bind :$PORT main:app