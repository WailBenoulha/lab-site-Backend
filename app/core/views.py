from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterSerializer,AppointementSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Appointements,Message
from rest_framework.decorators import api_view,permission_classes
from .permissions import IsAdmin,IsPatient,IsPremiumPatient
from drf_spectacular.utils import extend_schema


class Register(APIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
# @permission_classes([IsAdmin])
def list_apointements(request):    
    model = Appointements.objects.all()
    serializer = AppointementSerializer(many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)  

@extend_schema(
    request=AppointementSerializer,
    responses=AppointementSerializer,
    description="Create a new appointment request (patients only)"
)

@api_view(['POST'])
@permission_classes([IsPatient])
def request_apointement(request):    
    serializer = AppointementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)    
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

# update the status of apointement request accept or reject 
@api_view(['PATCH'])
# @permission_classes([IsAdmin])
def accept_request(request,pk=None):
    model = Appointements.objects.get(pk=pk)
    if 'status' not in request.data:
        return Response({'error': 'Status field is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AppointementSerializer(model, data={'status': request.data['status']}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)    
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
