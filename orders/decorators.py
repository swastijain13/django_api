from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


def require_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if getattr(request, "_force_auth_check", False):
            return Response(
                {"status": "error", "message": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if (
            hasattr(request, "user")
            and request.user is not None
            and hasattr(request.user, "id")
        ):
            request.user_id = request.user.id
            request.is_admin = getattr(request.user, "is_admin", False)
            return view_func(request, *args, **kwargs)

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"status": "error", "message": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = RefreshToken(refresh_token)
            request.user_id = token["user_id"]
            request.is_admin = token["is_admin"]
            return view_func(request, *args, **kwargs)
        except Exception:
            return Response(
                {"status": "error", "message": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    return wrapper
