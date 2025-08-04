
# Utilisation locale

1. Installez les dépendances :
   ```powershell
   pip install -r requirements.txt
   ```

2. Lancez le serveur Flask :
   ```powershell
   python app/main.py
   ```

   > Lors du premier démarrage, la base SQLite (`database.sqlite3`) sera automatiquement créée si elle n'existe pas, avec le bon schéma.

3. Accédez à la documentation Swagger/OpenAPI :
   Ouvrez http://localhost:5000/swagger/ dans votre navigateur.

# Utilisation avec Docker

1. Lancez l'API avec Docker Compose :
   ```powershell
   docker-compose up --build
   ```

   - Les fichiers et la base sont persistés sur votre machine via les volumes.
   - L'API est accessible sur http://localhost:5000
   - La documentation Swagger est disponible sur http://localhost:5000/swagger/
