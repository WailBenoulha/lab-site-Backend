from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import (RegisterSerializer,
                          AppointementSerializer,
                          AppointementStatusSerializer)
from rest_framework.response import Response
from rest_framework import status
from .models import Appointements,Message
from rest_framework.decorators import api_view,permission_classes
from .permissions import IsAdmin,IsPatient,IsPremiumPatient
from drf_spectacular.utils import extend_schema

# The patient can create an account
class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAdmin]

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# The Admin Can see the panding Request of taking Appointments
class ListPendingAppointments(APIView):
    serializer_class = AppointementSerializer
    
    def get(self,request):    
        model = Appointements.objects.filter(status='pending')
        serializer = AppointementSerializer(model,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)  

@extend_schema(
    request=AppointementSerializer,
    responses=AppointementSerializer,
    description="Create a new appointment request (patients only)"
)

# The patient can add a request of an appointments

@api_view(['POST'])
@permission_classes([IsPatient])
def request_apointement(request):    
    serializer = AppointementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)    
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


# The Admin can accept or refuse the patient appointments by updating the status of request

class AcceptRefuseRequest(APIView):
    serializer_class = AppointementStatusSerializer
    permission_classes = [IsAdmin]

    def patch(self,request,pk=None):
        instance = Appointements.objects.get(pk=pk)
        serializer = AppointementStatusSerializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
        