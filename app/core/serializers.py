from rest_framework.serializers import ModelSerializer
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['fullname','email']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # hash password
        return super().create(validated_data)      