from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import (RegisterSerializer,
                          AppointementSerializer,
                          AppointementStatusSerializer,
                          MessagePatientSerializer,
                          MessageAdminSerializer,
                          AppointmentNotification,
                          CustomTokenObtainPairSerializer,
                          ImagePredictionSerializer,
                          UpgradeSerializer)
from rest_framework.response import Response
from rest_framework import status
from .models import Appointements,Message,CustomUser,ImagePrediction
from rest_framework.decorators import api_view,permission_classes
from .permissions import IsAdmin,IsPatient,IsPremiumPatient,IsPatientOrPremiumPatient
from drf_spectacular.utils import extend_schema
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.http import FileResponse
from .models import ImagePrediction
from utils.pdf_generator import generate_user_predictions_pdf
import io

# The user can login
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# The patient can create an account
class Register(APIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# The Admin could see the list of registered patients
class ListUser(APIView):
    serializer_class = RegisterSerializer
    permission_classes =[IsAdmin]

    def get(self,request):
        instance = CustomUser.objects.filter(Q(role='patient') | Q(role='premium_patient'))
        serializer = RegisterSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


# The Admin Can see the panding Request of taking Appointments
class ListPendingAppointments(APIView):
    serializer_class = AppointementSerializer
    permission_classes = [IsAdmin]
    
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
@permission_classes([IsPatientOrPremiumPatient])
def request_apointement(request):    
    serializer = AppointementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# The Admin can accept or refuse the patient appointments by updating the status of request

class AcceptRefuseRequest(APIView):
    serializer_class = AppointementStatusSerializer
    permission_classes = [IsAdmin]

    def patch(self,request,pk=None):
        instance = Appointements.objects.get(pk=pk)
        serializer = AppointementStatusSerializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            new_status = serializer.validated_data.get('status')
            
            if new_status == 'accepted':
                serializer.save(notification='Your request of appointment are accepted! see you soon!')
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            
            elif new_status == 'rejected':
                instance.delete()
                return Response({'deleted': 'The request has been rejected and deleted.'}, status=status.HTTP_200_OK)
            
            return Response({'error': 'Invalid status value.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListAcceptedRequest(APIView):
    serializer_class = AppointmentNotification
    permission_classes = [IsPatientOrPremiumPatient]

    def get(self,request):
        instance = Appointements.objects.filter(user=request.user, status='accepted')
        serializer = AppointmentNotification(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class MessagePatient(APIView):   
    serializer_class = MessagePatientSerializer
    permission_classes = [IsPatientOrPremiumPatient] 

    # The patient can see their messages
    def get(self,request):
        instance = Message.objects.filter(user=request.user)
        serializer = MessagePatientSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # the patient send messages to Admin
    def post(self,request):
        serializer = MessagePatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class MessageAdmin(APIView):
    serializer_class = MessageAdminSerializer
    permission_classes = [IsAdmin] 

    # The Admin can see the new messages that he didnt reply yet
    def get(self,request):
        instance = Message.objects.filter(reply__isnull=True)
        serializer = MessageAdminSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # The admin can reply at the messages of patients by updating the reply field from null to a reply message
    def patch(self,request,pk=None):
        instance = Message.objects.get(pk=pk)
        serializer = MessageAdminSerializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# The Patient can see the result of his Xray photo
class ImagePredictionCreateView(generics.CreateAPIView):
    queryset = ImagePrediction.objects.all()
    serializer_class = ImagePredictionSerializer
    permission_classes = [IsPatientOrPremiumPatient]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# The premium patient can download all his prediction results
class UserPdf(APIView):
    permission_classes = [IsPremiumPatient]

    def get(self, request):
        predictions = ImagePrediction.objects.filter(user=request.user).order_by('-datetime')
        if not predictions.exists():
            return FileResponse(io.BytesIO(b"No predictions found"), content_type='application/pdf', filename="empty.pdf")

        pdf_buffer = generate_user_predictions_pdf(predictions, request.user.email)
        return FileResponse(pdf_buffer, as_attachment=True, filename="your_predictions.pdf")

# The patient can upgrade his profile to premium patient by updating role
class PremiumUpgrade(APIView):
    serializer_class = UpgradeSerializer
    permission_classes = [IsPatient]

    def patch(self,request,pk=None):
        instance = request.user
        serializer = UpgradeSerializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(role='premium_patient')
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)