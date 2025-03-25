from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import App, UserTask

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2' , 'role', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = "__all__"

class UserTaskSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source="app.name", read_only=True)
    points = serializers.CharField(source="app.points", read_only=True)


    class Meta:
        model = UserTask
        fields = ['id', 'user_id', 'app_id', 'app_name', 'completed', 'screenshot','points']








