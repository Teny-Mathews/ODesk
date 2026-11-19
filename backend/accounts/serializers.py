from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'dob',
            'phone',
            'password',
            'confirm_password',
            'role',
        ]


    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords do not match'})
        validate_password(password)
        return data
    

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'dob',
            'phone',
            'role',
        ]
        read_only_fields = ['id', 'username', 'email', 'role']