# 🍽️ Food Ordering API (Django REST + MySQL)

This is a backend API for a food ordering system. It supports **user authentication**, **admin menu management**, **order placement**, and **role-based access control** using JWT.

---

##  Features

- JWT Authentication (`djangorestframework-simplejwt`)
- Role-based Access: `admin` and `user`
- Menu management (CRUD for admins)
- Users can browse menu, order food, cancel order, and view order history
- Admin can view all orders
- MySQL database integration
- Pytest testing & coverage
- PEP8-compliant code with `black` & `pylint`

---

##  Setup Locally

```bash
git clone https://github.com/swastijain13/food_ordering_api.git
cd food_ordering_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure .env file
create a .env file at the root:
```
SECRET_KEY=your_django_secret_key
DEBUG=True

#database
NAME = your_database_name
DB_USER = your_mysql_username
PASSWORD = your_mysql_password
HOST = localhost
PORT = 3306
```


### Mysql Setup
```
CREATE DATABASE food_ordering;
```


### Run Migrations and Start Server
```
 python manage.py makemigrations
 python manage.py migrate
 python manage.py createsuperuser
```

### Run the server
```
 python manage.py runserver
```

Visit: http://127.0.0.1:8000
Admin Panel: http://127.0.0.1:8000/admin

## **API Endpoints**
### **Authentication Endpoints**
#### **Sign Up (Direct URL Access)**
Open in browser:
```
http://127.0.0.1:8000/orders/signup/
```
Use POST method with:
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```
#### **Login (Direct URL Access)**
Open in browser:
```
http://127.0.0.1:8000/orders/login/
```
Use POST method with:
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```
**Response:**
```json
{
  "status": "success",
  "username": "user.username",
  "message": "Login successful",
  "access": "<ACCESS_TOKEN>",
  "refresh": "<REFRESH_TOKEN>"
}
```

#### API Token
```
http://127.0.0.1:8000/api/token
```
Use POST method with:
```json
{
 "username" : "username"
 "password" : "password"
}
```
**Response**
```json
{
  "refresh_token" : "refresh_token",
  "access_token" : "access_token"
}
```

#### **Logout**

##### open in browser**:
```
http://localhost:8000/orders/logout/
```
Use POST method with:
```json
{
  "refresh_token": "<REFRESH_TOKEN>"
}
```
**Response:**
```json
{
  "status" : "success"
  "message": "Successfully logged out",
}
```

### **User Endpoints** *(JWT Authentication Required)*
#### **View menu**
```
curl -X GET http://127.0.0.1:8000/orders/menu/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
#### **Order an item**
```
curl -X POST http://127.0.0.1:8000/orders/item/<menu_item_id>/order/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
  -d '{
      "quantity" : <enter quantity>
      }'
```
**Response:**
```json
{
  "status" : "success"
  "message": "Order successful",
  "data" : {
    "user":"user_id",
    "menu_item" : "menu_item_id",
    "quantity":"quantity",
    "ordered_at":"time",
    "total_amount":"total_amount"
  }
}
```

---
### **Admin Endpoints** *(Admin + JWT Authentication Required)*
#### **Add an item in menu**
Run Curl command in terminal
```
curl -X POST http://127.0.0.1:8000/admin_api/items/add/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
  -d '{
      "name" : "item_name"
      "price" : <enter price>
      }'
```

#### **Update a menu item**
```
curl -X PUT http://127.0.0.1:8000/admin_api/items/<item_id>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
  -d '{
      "name" : "item_name"
      "price" : <enter price>
      }'

```
#### **Delete an item**
```
curl -X DELETE http://127.0.0.1:8000/admin_api/items/<item_id>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
  
```
#### **View all users**
```
curl -X DELETE http://127.0.0.1:8000/admin_api/users/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
#### **View all orders**
```
curl -X DELETE http://127.0.0.1:8000/admin_api/orders/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
---

## **Code Quality & Linting**
### **Run Pylint to Check Code Quality**
```sh
pylint adoption
```
---
## **Testing & Coverage**
### **Run Tests with Pytest**
```sh
pytest
```

#### **Endpoints covered**
```
/orders/signup/                 -> signup a user
/orders/login/                  -> login a user
/orders/logout/                 -> logout a user
/orders/item/<int:pk>/order/    -> order an item
/orders/item/<int:pk>/cancel/   -> cancel order
/menu/                          -> browse menu
/orders/user_orders/            -> get all user orders

/admin_api/items/add/           -> admin can add an item in menu
/admin_api/items/<int:pk>/      -> admin can see item details and update, delete it
/admin_api/users/               -> admin can see all users
/admin_api/orders/              -> admin can see all orders
```
### **Check Test Coverage**
```sh
pytest --cov=adoption --cov-report=term-missing
```
### **Generate HTML Coverage Report**
```sh
pytest --cov=adoption --cov-report=html
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```
### **Enforce Minimum Coverage (Fail if <80%)**
```sh
pytest --cov=adoption --cov-fail-under=80
```
---
