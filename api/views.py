from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import RegisterSerializer, TaskSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/register/ - create a new user and return a token."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "message": "User registered successfully.",
                "username": user.username,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    """POST /api/logout/ - delete the user's token."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)


class TaskViewSet(viewsets.ModelViewSet):
    """Full CRUD for tasks. A user can only see and change their own tasks."""

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
