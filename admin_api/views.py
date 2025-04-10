from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt
from rest_framework import status
from orders.models import User, MenuItem, Order
from orders.serializers import UserSerializer, MenuItemSerializer, OrderSerializer
from orders.decorators import require_auth


@api_view(["GET"])
@require_auth
def get_users(request):
    if not request.is_admin:
        return Response(
            {
                "status": "error",
                "message": "Unauthorized admin",
                "is_admin": request.is_admin,
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = UserSerializer(User.objects.all(), many=True)
    return Response(
        {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@require_auth
def get_orders(request):
    if not request.is_admin:
        return Response(
            {"status": "error", "message": "Unauthorised Admin!"},
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = OrderSerializer(Order.objects.all(), many=True)
    return Response(
        {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["GET", "POST"])
@require_auth
def add_item(request):
    if not request.is_admin:
        return Response(
            {"status": "error", "message": "Unauthorised Admin!"},
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"status": "success", "message": "Item added", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {"status": "error", "message": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET", "PUT", "DELETE"])
@require_auth
def item_detail(request, pk):
    if not request.is_admin:
        return Response(
            {"status": "error", "message": "Unauthorised Admin!!"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(
            {"status": "error", "message": "item not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        # item = MenuItem.objects.get(pk=pk)
        serializer = MenuItemSerializer(item)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    if request.method == "PUT":
        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Item updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif request.method == "DELETE":
        item.delete()
        return Response(
            {"status": "success", "message": "Item deleted successfully"},
            status=status.HTTP_200_OK,
        )
