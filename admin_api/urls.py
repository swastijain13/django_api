from django.urls import path
from .views import get_users, get_orders, add_item, item_detail

urlpatterns = [
    path("items/add/", add_item, name="add_item"),
    path("items/<int:pk>/", item_detail, name="item_detail"),
    path("users/", get_users, name="get_users"),
    path("orders/", get_orders, name="get_orders"),
]
