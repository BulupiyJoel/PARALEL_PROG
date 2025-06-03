FROM python:3.11-slim

# Installer les dépendances système pour mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    python3-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de l'application
WORKDIR /app

# Copier tous les fichiers dans l'image
COPY . .

# Définir le répertoire où se trouve manage.py
WORKDIR /app/django_blog

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
