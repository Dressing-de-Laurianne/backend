# Utilise une image Python officielle
FROM python:3.13-slim

WORKDIR /app

# Installe les dépendances
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code
COPY app /app/app

# Crée le dossier pour les photos
RUN mkdir -p photos

# Expose le port Flask
EXPOSE 5000

# Lance l'API
CMD ["python", "app/main.py"]
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.main:app"]
