FROM python:3.12-slim

WORKDIR /app

# Instalamos dependencias del sistema necesarias para psycopg
RUN apt update && apt install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiamos dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código Django
COPY . .

# Gunicorn para dev y prod
CMD ["gunicorn", "huella_project.wsgi:application", "--bind", "0.0.0.0:8000"]
