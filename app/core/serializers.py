from rest_framework.serializers import ModelSerializer
from .models import CustomUser,Appointements,Message,ImagePrediction
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role if hasattr(user, 'role') else 'user'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra fields to response
        data['role'] = self.user.role if hasattr(self.user, 'role') else 'user'
        return data


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','fullname','email','password','role','date_joined']
        extra_kwargs = {
            'password': {'write_only':True},
            'date_joined': {'read_only':True},
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
        fields = ['status','notification']        
        extra_kwargs = {
            'fullname':{'read_only':True},
            'date':{'read_only':True},
            'time':{'read_only':True},
            'notification':{'read_only':True}
        }

class AppointmentNotification(ModelSerializer):
    class Meta:
        model = Appointements
        fields = ['date','time','notification']        

class MessagePatientSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['name','email','subject','message','reply']
        extra_kwargs = {
            'reply':{'read_only':True}
        }

class MessageAdminSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','user','name','email','subject','message','reply']        
        extra_kwargs = {
            'user':{'read_only':True},
            'name':{'read_only':True},
            'email':{'read_only':True},
            'subject':{'read_only':True},
            'message':{'read_only':True}
        }

class ImagePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePrediction
        fields = ['id', 'image', 'prediction']
        read_only_fields = ['prediction']