import pytest
from rest_framework.test import APIClient
from orders.models import User, MenuItem


@pytest.mark.django_db
def test_admin_add_menu_item():
    client = APIClient()

    # created admin
    admin = User.objects.create_user(
        username="admin_user", password="adminpass123", is_admin=True
    )

    # login
    login = client.post(
        "/orders/login/",
        {"username": "admin_user", "password": "adminpass123"},
        format="json",
    )
    assert login.status_code == 200

    access_token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    # add menu item
    response = client.post(
        "/admin_api/items/add/", {"name": "Burger", "price": 80}, format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_admin_update_menu_item():
    admin = User.objects.create_user(
        username="admin2", password="adminpass2", is_admin=True
    )
    item = MenuItem.objects.create(name="Old Item", price=100)
    client = APIClient()
    login = client.post(
        "/orders/login/",
        {"username": "admin2", "password": "adminpass2"},
        format="json",
    )
    access_token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = client.put(
        f"/admin_api/items/{item.id}/",
        {"name": "New Item", "price": 150},
        format="json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_get_users():
    admin = User.objects.create_user(
        username="admin3", password="adminpass3", is_admin=True
    )
    User.objects.create_user(username="user1", password="userpass")
    client = APIClient()
    login = client.post(
        "/orders/login/",
        {"username": "admin3", "password": "adminpass3"},
        format="json",
    )
    access_token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = client.get("/admin_api/users/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_get_orders():
    admin = User.objects.create_user(
        username="admin4", password="adminpass4", is_admin=True
    )
    client = APIClient()
    login = client.post(
        "/orders/login/",
        {"username": "admin4", "password": "adminpass4"},
        format="json",
    )
    access_token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = client.get("/admin_api/orders/")
    assert response.status_code == 200
