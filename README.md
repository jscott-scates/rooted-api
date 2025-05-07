# Rooted Deck – Server Side

This is the server-side API for **Rooted Deck**, a reflection and journaling app that allows users to draw oracle cards, engage in meaningful spreads, and document their insights. This Django project serves as the backend for the React client application, providing user authentication, data persistence, and business logic.

## Features

- RESTful API built with Django REST Framework
- User registration, login, and JWT-based authentication
- Journal entries with mood and lunar phase tracking
- Card draws and spread assignments
- Card keyword tagging and element association
- Full CRUD functionality for cards, spreads, and journals
- CORS enabled for frontend communication

## Tech Stack

- **Backend**: Django
- **API**: Django REST Framework (DRF)
- **Authentication**: JWT via `djangorestframework-simplejwt`
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Cross-Origin**: `django-cors-headers` for local dev and deployment
- **Environment Management**: `python-decouple`

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rooted-deck-server.git
cd rooted-deck-server ```

### 2. Set Up Virtual Environment 
```python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate```

### 3. Install Dependencies
```python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate```

### 4. Set Up Environment Variables
```DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3```

### 5. Run Migrations
```python manage.py migrate```

### 6. Create Superuser (optional)
```python manage.py createsuperuser```

### 7. Run the Development Server
```python manage.py runserver```

API is now available at http://localhost:8000.

## API Overview

| Endpoint                | Method   | Description                          |
|------------------------|----------|--------------------------------------|
| `/api/auth/register/`  | POST     | Register a new user                  |
| `/api/auth/login/`     | POST     | Obtain JWT token                     |
| `/api/journals/`       | GET, POST| List or create journal entries       |
| `/api/journals/<id>/`  | GET, PUT, DELETE | Retrieve, update, or delete a journal entry |
| `/api/cards/`          | GET      | Retrieve available oracle cards      |
| `/api/cards/<id>/`     | GET      | Retrieve a specific card             |
| `/api/spreads/`        | GET      | List available spread templates      |
| `/api/entry-cards/`    | GET, PUT | Retrieve or update linked entry cards |
| `/api/entry-cards/?journal-entry=<id>` | GET | Retrieve cards linked to a specific journal |

You can test endpoints using [Postman](https://www.postman.com/) or [Yaak](https://yaak.ai/).

##Project Structure
/rooted_deck_api    → Main Django project
/journals           → App for journal entries
/cards              → App for card data and spreads
/users              → App for authentication
/manage.py          → Project runner

##Future Enhancements
-Add user-customizable spreads
-Support for multiple deck types
-Rate-limiting and throttling
-Admin-side deck and keyword editing
