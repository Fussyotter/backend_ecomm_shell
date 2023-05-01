from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email',
                  'street_address', 'city', 'state', 'zip_code']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            street_address=validated_data['street_address'],
            city=validated_data['city'],
            state=validated_data['state'],
            zip_code=validated_data['zip_code']
        )
        return user
