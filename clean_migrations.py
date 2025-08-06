import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(BASE_DIR):
    if os.path.basename(root) == "migrations":
        for file in files:
            if file != "__init__.py" and file.endswith(".py"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
