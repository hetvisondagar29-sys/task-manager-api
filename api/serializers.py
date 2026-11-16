from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        # create_user() hashes the password for us
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "is_completed", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
