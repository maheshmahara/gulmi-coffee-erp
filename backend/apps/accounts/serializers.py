from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserRole


AppUser = get_user_model()


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["id", "code", "username", "full_name", "phone", "role", "active"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["id", "code", "username", "full_name", "phone", "role", "active", "is_staff", "created_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=UserRole.choices)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = AppUser
        fields = ["id", "code", "username", "full_name", "phone", "email", "role", "active", "password"]
        read_only_fields = ["id", "code"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = AppUser(**validated_data)
        if not user.username:
            user.username = validated_data.get("phone") or validated_data.get("email") or validated_data.get("full_name").lower().replace(" ", ".")
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserRole.choices, required=False)

    class Meta:
        model = AppUser
        fields = ["full_name", "phone", "email", "role", "active", "is_staff"]
