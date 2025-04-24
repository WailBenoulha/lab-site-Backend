from rest_framework.serializers import ModelSerializer
from .models import CustomUser,Appointements,Message
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['fullname','email','password']
        extra_kwargs = {
            'password': {'write_only':True},
            'role':{'read_only':True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # hash password
        return super().create(validated_data)

class AppointementSerializer(ModelSerializer):
    class Meta:
        model = Appointements
        fields = ['id','fullname','date','time']
        extra_kwargs = {
            'status': {'read_only':True}
        }

class AppointementStatusSerializer(ModelSerializer):
    class Meta:
        model = Appointements
        fields = ['status']        
        extra_kwargs = {
            'fullname':{'read_only':True},
            'date':{'read_only':True},
            'time':{'read_only':True}
        }