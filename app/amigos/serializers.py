from rest_framework import serializers

from app.usuario.models import Usuario
from .models import CustomNotification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        exclude = ("password",)


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)

    class Meta:
        model = CustomNotification
        fields = "__all__"
