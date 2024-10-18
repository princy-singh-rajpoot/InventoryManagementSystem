# Backend API for Inventory Management System

## Project Overview
This project involves building a Backend API for a simple Inventory Management System using Django Rest Framework (DRF). The system supports CRUD operations on inventory items and includes JWT-based authentication for secure access. Key technologies include Django, PostgreSQL, Redis for caching, and a logging system. Unit tests are implemented to verify API functionality.

## Features
- **API Framework**: Django Rest Framework (DRF)
- **Database**: PostgreSQL for inventory items storage
- **Caching**: Redis for caching frequently accessed items
- **Authentication**: JWT for secure access to API endpoints
- **Logging**: Integrated logger for monitoring and debugging
- **Testing**: Unit tests for all API functionalities

## Functionalities
1. **JWT Authentication**: 
   - Secure all endpoints using JWT tokens.
   - Endpoints for user registration, login, and token retrieval.
   
2. **CRUD Operations**: 
   - **Create Item**: Add new items to the inventory (`POST /items/`).
   - **Read Item**: Retrieve item details by ID (`GET /items/{item_id}/`), with Redis caching for performance.
   - **Update Item**: Modify existing items (`PUT /items/{item_id}/`).
   - **Delete Item**: Remove items from inventory (`DELETE /items/{item_id}/`).

3. **Redis Caching**: 
   - Cache frequently accessed items on the Read Item endpoint.

4. **Logging**: 
   - Log API usage, errors, and other significant events.

5. **Unit Tests**: 
   - Comprehensive test coverage for all endpoints, ensuring reliability.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup PostgreSQL**:
   - Ensure PostgreSQL is installed and running.
   - Create a database and update the `DATABASES` setting in `settings.py`.

5. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Run Redis**:
   - Ensure Redis is installed and running.

7. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
- **POST /register/**: Register a new user
- **POST /login/**: Login and retrieve JWT token
- **POST /items/**: Create a new item
- **GET /items/{item_id}/**: Retrieve item details (uses Redis caching)
- **PUT /items/{item_id}/**: Update item details
- **DELETE /items/{item_id}/**: Delete an item

## Running Tests
To run the unit tests:
```bash
python manage.py test
```

## Logging
Logs can be found in the log files, capturing important API events such as requests, errors, and debug messages.

---