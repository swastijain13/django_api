from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import status
from django.http import JsonResponse
from .decorators import require_auth
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import User, MenuItem, Order
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, OrderSerializer
from orders.serializers import MenuItemSerializer


def home_view(request):
    return JsonResponse({"message": "Welcome to Online food ordering application!!"})


@api_view(["POST"])
def signup(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "User created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"status": "error", "message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        refresh["is_admin"] = user.is_admin
        refresh["username"] = user.username

        response = Response(
            {
                "status": "success",
                "username": user.username,
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )

        return response

    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def logout(request):
    try:
        token = request.data["refresh_token"]
        refresh_token = RefreshToken(token)
        refresh_token.blacklist()

        return Response(
            {"status": "success", "message": "Successfully logged out"},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"status": "error", "message": "Invalid token", "details": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@require_auth
def browse_menu(request):
    items = MenuItem.objects.all()
    serializer = MenuItemSerializer(items, many=True)
    return Response(
        {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@require_auth
def order_menu_item(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
        quantity = int(request.data.get("quantity", 1))

        if quantity <= 0:
            return Response(
                {"status": "error", "message": "Invalid number"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_amount = menu_item.price * quantity
        order_data = {
            "user": request.user.id,
            "menu_item": menu_item.id,
            "quantity": quantity,
            "ordered_at": timezone.now(),
            "total_amount": total_amount,
        }

        serializer = OrderSerializer(data=order_data)

        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Order successful",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except MenuItem.DoesNotExist:
        return Response(
            {"status": "error", "message": "Item does not exist!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
@require_auth
def cancel_order(request, pk):
    try:
        order = Order.objects.filter(menu_item_id=pk, user_id=request.user_id).first()

        if not order:
            return Response(
                {"status": "error", "message": "No such order!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        order.delete()

        return Response(
            {
                "status": "success",
                "message": "Order cancelled successfully",
                "data": {
                    "refund_amount": order.total_amount,
                },
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@require_auth
def get_user_orders(request):
    order = Order.objects.filter(user_id=request.user_id)
    serializer = OrderSerializer(order, many=True)
    return Response(
        {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
    )
