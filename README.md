
# Dressing API Project

This project is a Django REST API for managing a virtual wardrobe, built with Django, Django REST Framework and SQLite. It includes a Swagger UI for API exploration and is based on the official Django REST Framework tutorial.

## 🚀 Running with Docker

To start the project in production mode:

```bash
docker compose up --build
```

This will:
- Build the Docker image
- Start the Django app containing the SQLite database
- Run migrations and create an initial superuser (admin/admin)

## 🛠️ Development with Docker

For development, use the dev compose file to mount your local code and see changes live:

```bash
docker compose -f docker-compose.dev.yml up --build
```

This will:
- Mount your local folder into the container
- Reload code changes automatically
- Use the same database and admin credentials

## 📚 Project Details

The project is organized into several Django apps:
- `item`: Manage clothing items
- `outfit`: Manage group of items
- `order`: Manage orders
- `hanger`, : Manage connected hander

### API Endpoints

The API exposes endpoints for managing items, orders, and more. Example endpoints:

- `/api/items/` — List and create clothing items
- `/api/orders/` — List and manage orders

> The API is based on the Django REST Framework tutorial: [DRF Serialization Tutorial](https://www.django-rest-framework.org/tutorial/1-serialization/)

### 🔎 API Documentation (Swagger UI)

Interactive API documentation is available at:

```
http://localhost:8000/api/schema/swagger-ui/
```

You can explore and test all endpoints directly from the browser.

---

Feel free to contribute or adapt this project for your own needs!

---

## TODO

- Check and validate image upload and serving for items (media support)
- Add tag logic for items, similar to the original project (tagging system)
- Switch the environment to production mode (update settings, security, etc.)
