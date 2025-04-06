from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    home_view,
    signup,
    login,
    logout,
    order_menu_item,
    cancel_order,
    get_user_orders,
    browse_menu,
)

urlpatterns = [
    path("", home_view),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("item/<int:pk>/order/", order_menu_item, name="order_menu_item"),
    path("item<int:pk>/cancel/", cancel_order, name="cancel_order"),
    path("menu/", browse_menu, name="browse_menu"),
    path("user_orders/", get_user_orders, name="get_user_orders"),
]
