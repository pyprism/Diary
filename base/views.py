from rest_framework import generics, permissions

from base.serializers import RegisterSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/
    Create a new user account.  Disabled when REGISTRATION_OPEN=false in .env.
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    """
    GET /api/v1/auth/me/
    Return the profile of the currently authenticated user.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
