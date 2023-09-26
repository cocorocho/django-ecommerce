from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def check_user(self, cleaned_data: dict):
        user = authenticate(
            email=cleaned_data["email"],
            password=cleaned_data["password"]
        )

        if not user:
            raise serializers.ValidationError(_("Invalid credentials"))
        
        return user
