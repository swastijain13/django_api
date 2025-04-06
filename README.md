# 🍽️ Food Ordering API (Django REST + MySQL)

This is a backend API for a food ordering system. It supports **user authentication**, **admin menu management**, **order placement**, and **role-based access control** using JWT.

---

## 🚀 Features

- JWT Authentication (`djangorestframework-simplejwt`)
- Role-based Access: `admin` and `user`
- Menu management (CRUD for admins)
- Users can browse menu, order food, cancel order, and view order history
- Admin can view all orders
- MySQL database integration
- Pytest testing & coverage
- PEP8-compliant code with `black` & `pylint`

---

## 🛠️ Setup Locally

```bash
git clone https://github.com/swastijain13/food_ordering_api.git
cd food_ordering_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

✅ Configure .env file
create a .env file at the root:

SECRET_KEY=your_django_secret_key
DEBUG=True

# Database
NAME = your_database_name
DB_USER = your_mysql_username
PASSWORD = your_mysql_password
HOST = localhost
PORT = 3306


# Mysql Setup
CREATE DATABASE food_ordering;


# Run Migrations and Start Server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver