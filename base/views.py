from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from base.serializers import LogoutSerializer, RegisterSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/
    Create a new user account.  Disabled when REGISTRATION_OPEN=false in .env.
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/v1/auth/me/  — profile of the currently authenticated user.
    PATCH /api/v1/auth/me/  — update mutable profile fields (currently: web_base_url).
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Blacklists the presented refresh token so it can no longer be used to
    obtain new access tokens, even though it hasn't naturally expired yet.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError as e:
            raise ValidationError({"refresh": str(e)})

        return Response(status=status.HTTP_205_RESET_CONTENT)
