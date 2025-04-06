import pytest
from rest_framework.test import APIClient
from rest_framework import status
from orders.models import Order, User, MenuItem


@pytest.mark.django_db
def test_signup():
    client = APIClient()
    response = client.post(
        "/orders/signup/",
        {"username": "newuser", "email": "new@example.com", "password": "testpass"},
        format="json",
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_login_logout():
    user = User.objects.create_user(username="loginuser", password="loginpass")
    client = APIClient()
    login = client.post(
        "/orders/login/",
        {"username": "loginuser", "password": "loginpass"},
        format="json",
    )
    assert login.status_code == 200

    refresh = login.data["refresh"]
    logout = client.post("/orders/logout/", {"refresh_token": refresh}, format="json")
    assert logout.status_code == 200


@pytest.mark.django_db
def test_user_login_wrong_credentials():
    client = APIClient()

    User.objects.create_user(username="user1", password="testpass123")

    response = client.post(
        "/orders/login/",
        {"username": "user1", "password": "wrongpass"},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["message"] == "Invalid credentials"


@pytest.mark.django_db
def test_order_menu_item():
    user = User.objects.create_user(username="orderuser", password="orderpass")
    item = MenuItem.objects.create(name="Fries", price=50)
    client = APIClient()
    login = client.post(
        "/orders/login/",
        {"username": "orderuser", "password": "orderpass"},
        format="json",
    )
    access_token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = client.post(
        f"/orders/item/{item.id}/order/", {"quantity": 2}, format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_order_non_existing_menu_item():
    client = APIClient()

    user = User.objects.create_user(username="user2", password="pass123")

    login = client.post(
        "/orders/login/", {"username": "user2", "password": "pass123"}, format="json"
    )
    access_token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    response = client.post("/orders/item/999/order/", {"quantity": 2}, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["message"] == "Item does not exist!"


@pytest.mark.django_db
def test_cancel_order():
    client = APIClient()
    user = User.objects.create_user(username="user_test", password="user_test")

    login_response = client.post(
        "/orders/login/",
        {"username": "user_test", "password": "user_test"},
        format="json",
    )
    assert login_response.status_code == 200
    access_token = login_response.data["access"]

    item = MenuItem.objects.create(name="Fries", price=40)

    order = Order.objects.create(
        user=user,
        menu_item=item,
        quantity=1,
        total_amount=item.price,
    )

    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    cancel_response = client.delete(f"/orders/item{item.id}/cancel/")

    assert cancel_response.status_code == 200
    assert cancel_response.data["status"] == "success"
    assert cancel_response.data["message"] == "Order cancelled successfully"
    assert cancel_response.data["data"]["refund_amount"] == item.price


@pytest.mark.django_db
def test_browse_menu():
    MenuItem.objects.create(name="Pasta", price=120)
    client = APIClient()
    response = client.get("/orders/menu/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_user_orders():
    client = APIClient()

    user = User.objects.create_user(username="test_user", password="test_user")

    item1 = MenuItem.objects.create(name="Pizza", price=150)
    item2 = MenuItem.objects.create(name="Pasta", price=120)

    Order.objects.create(user=user, menu_item=item1, quantity=1, total_amount=150)
    Order.objects.create(user=user, menu_item=item2, quantity=2, total_amount=240)

    login_response = client.post(
        "/orders/login/",
        {"username": "test_user", "password": "test_user"},
        format="json",
    )
    assert login_response.status_code == 200
    access_token = login_response.data["access"]

    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    response = client.get("/orders/user_orders/")

    assert response.status_code == 200
    assert response.data["status"] == "success"
    assert len(response.data["data"]) == 2
    menu_item_ids = [item["menu_item"] for item in response.data["data"]]
    assert item1.id in menu_item_ids
    assert item2.id in menu_item_ids
