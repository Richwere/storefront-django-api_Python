# Storefront Django API

A backend e-commerce API built with **Django** and **Django REST Framework (DRF)**. The project provides RESTful endpoints for managing products and collections, with JWT-based authentication and user-specific product ownership.

The project is being developed as a practical backend engineering project to strengthen skills in **Django, REST APIs, authentication, authorization, database management, testing, and Git/GitHub workflows**.

---

## Project Overview

The Storefront API provides a backend system for managing products and product collections.

The API currently supports:

* User authentication using JWT
* Authenticated API access
* Product management
* Product collection management
* Product ownership
* User-specific product access
* Role/staff-based permission concepts
* Database relationships using Django ORM
* RESTful API endpoints
* Environment-based configuration
* Git version control

The project follows Django's Model-ViewSet-Serializer architecture through Django REST Framework.

---

## Technologies Used

### Backend

* **Python 3.12.4**
* **Django 6.0.7**
* **Django REST Framework**
* **Django REST Framework Simple JWT**
* **MariaDB**
* **Django ORM**

### Development Tools

* **Git**
* **GitHub**
* **Visual Studio Code**
* **DBeaver**
* **Pipenv**
* **Linux / Kali Linux**

---

## Project Structure

```text
storefront/
│
├── manage.py
├── Pipfile
├── Pipfile.lock
├── .gitignore
│
├── store/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── storefront/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── likes/
├── tags/
├── store_custom/
├── playground/
│
├── permissions.py
└── seed_data.py
```

---

# Getting Started

## 1. Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/Richwere/storefront-django-api_Python.git
```

Move into the project directory:

```bash
cd storefront-django-api_Python
```

---

## 2. Create a Virtual Environment

Using Python's built-in virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

If using Pipenv:

```bash
pipenv install
```

Activate the Pipenv environment:

```bash
pipenv shell
```

Alternatively, install dependencies using:

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```text
storefront/
├── .env
├── manage.py
└── ...
```

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=storefront_db
DB_USER=storefront_user
DB_PASSWORD=your-database-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Important

Do not commit `.env` to GitHub.

The `.gitignore` file already excludes environment files:

```gitignore
.env
```

For production deployments, use a secure secret key and set:

```env
DEBUG=False
```

---

# Database Setup

The project can be configured to use **MariaDB**.

Create the database and database user in MariaDB, then configure the credentials through environment variables.

After configuring the database, run the migrations:

```bash
python manage.py migrate
```

---

# Create a Superuser

Create an administrative account with:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter the username, email, and password.

---

# Run the Development Server

Start Django's development server:

```bash
python manage.py runserver
```

The API will normally be available at:

```text
http://127.0.0.1:8000/
```

---

# API Features

## Authentication

The API uses **JSON Web Tokens (JWT)** for authentication.

The authentication flow is:

```text
User Login
    ↓
JWT Access + Refresh Tokens
    ↓
Client sends Access Token
    ↓
Django verifies token
    ↓
request.user is identified
    ↓
API request is authorized
```

The access token is configured to expire after **30 minutes**, while the refresh token lasts for **1 day**.

---

## Product Management

Products can be managed through the REST API.

Supported operations include:

* List products
* Retrieve a product
* Create a product
* Update a product
* Delete a product

The Product API uses a Django REST Framework `ModelViewSet`.

---

## Product Ownership

Products are associated with the authenticated user who creates them.

For example:

```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

The API also restricts product queries to the authenticated user's products:

```python
def get_queryset(self):
    return Product.objects.select_related(
        "collection"
    ).filter(
        owner=self.request.user
    )
```

This prevents one authenticated user from accessing another user's products through the product endpoints.

---

# API Endpoints

## Products

Base endpoint:

```text
/store/products/
```

### List Products

```http
GET /store/products/
```

Requires authentication.

Example:

```bash
curl http://127.0.0.1:8000/store/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### Retrieve a Product

```http
GET /store/products/{id}/
```

Example:

```bash
curl http://127.0.0.1:8000/store/products/7/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### Create a Product

```http
POST /store/products/
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/store/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tittle": "Laptop",
    "slug": "laptop",
    "description": "A development laptop",
    "price": 85000,
    "inventory": 10,
    "collection": 1
  }'
```

The authenticated user is automatically assigned as the product owner.

---

### Update a Product

```http
PUT /store/products/{id}/
```

Example:

```bash
curl -X PUT http://127.0.0.1:8000/store/products/7/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tittle": "Updated Laptop",
    "slug": "updated-laptop",
    "description": "Updated product description",
    "price": 90000,
    "inventory": 8,
    "collection": 1
  }'
```

---

### Delete a Product

```http
DELETE /store/products/{id}/
```

Example:

```bash
curl -X DELETE http://127.0.0.1:8000/store/products/7/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

# Collections API

Base endpoint:

```text
/store/collections/
```

Collections can be accessed through the Django REST Framework router.

Example:

```http
GET /store/collections/
```

---

# JWT Authentication

## Obtain Tokens

The project uses Simple JWT for authentication.

Example endpoint:

```text
/api/token/
```

Request:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

A successful request returns:

```json
{
    "refresh": "YOUR_REFRESH_TOKEN",
    "access": "YOUR_ACCESS_TOKEN"
}
```

---

## Use the Access Token

Include the access token in the `Authorization` header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Example:

```bash
curl http://127.0.0.1:8000/store/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Refresh an Access Token

When the access token expires, the refresh token can be used to obtain another access token.

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

---

# Permissions and Authorization

The project distinguishes between authentication and authorization.

### Authentication

Determines:

> Who is the user?

This is handled using JWT authentication.

### Authorization

Determines:

> What is the user allowed to do?

The project uses Django REST Framework permissions such as:

```python
IsAuthenticated
```

Custom permissions can also be implemented using:

```python
from rest_framework.permissions import BasePermission
```

Example:

```python
class IsAdministrator(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )
```

---

# Django Management Commands

Check the project for configuration problems:

```bash
python manage.py check
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the Django shell:

```bash
python manage.py shell
```

---

# Git Workflow

The project uses Git for version control.

Check the current status:

```bash
git status
```

View commits:

```bash
git log --oneline
```

Create a new commit:

```bash
git add .
git commit -m "Describe your changes"
```

Push changes to GitHub:

```bash
git push
```

Pull the latest changes:

```bash
git pull
```

Create a new branch:

```bash
git checkout -b feature-name
```

Switch back to the main branch:

```bash
git checkout main
```

---

# Testing

Django's testing framework can be used to test application behavior.

Run the project's tests with:

```bash
python manage.py test
```

Tests can cover areas such as:

* Authentication
* Product creation
* Product retrieval
* Product updates
* Product deletion
* Permissions
* Product ownership
* API validation

---

# Security Considerations

The project follows several basic security practices:

* JWT-based authentication
* Authenticated API endpoints
* User-specific product access
* Environment variables for sensitive configuration
* `.env` excluded from Git
* Django's built-in security mechanisms
* Permission-based authorization

Before production deployment, additional security configuration should be applied, including:

* `DEBUG=False`
* Secure `SECRET_KEY`
* HTTPS
* Secure cookies
* Proper `ALLOWED_HOSTS`
* Database security
* Production-grade server configuration
* Proper CORS configuration where required
* Rate limiting/throttling where appropriate

---

# Future Improvements

Potential improvements include:

* API filtering
* Searching
* Ordering
* Pagination
* Improved validation
* Automated API tests
* API documentation with OpenAPI/Swagger
* Docker support
* CI/CD with GitHub Actions
* Production deployment
* Improved error handling
* Performance optimization

---

# Learning Objectives

This project is also used as a practical learning environment for backend development.

The main learning areas include:

* Python backend development
* Django fundamentals
* Django ORM
* SQL and relational databases
* Django REST Framework
* Serializers
* ViewSets
* REST API design
* JWT authentication
* Permissions and authorization
* Testing
* Git and GitHub
* Backend project structure
* API security
* Deployment concepts

---

# Author

**Richard Were**

BSc Computer Science
Maseno University, Kenya

GitHub:
https://github.com/Richwere

---

# License

This project is intended primarily for learning and development purposes.

A formal open-source license can be added when the project is ready for public distribution.
