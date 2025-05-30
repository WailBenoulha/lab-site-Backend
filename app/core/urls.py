from django.urls import path
from core.views import (Register,
                        ListPendingAppointments,
                        request_apointement,
                        AcceptRefuseRequest,
                        MessagePatient,
                        MessageAdmin,
                        ListUser,
                        ListAcceptedRequest,
                        ImagePredictionCreateView,
                        UserPdf,
                        PremiumUpgrade)

urlpatterns = [
    path('register',Register.as_view(),name='register'),
    path('appointments/', ListPendingAppointments.as_view(), name='list-appointments'),
    path('appointments/request/', request_apointement, name='request-appointment'),
    path('appointments/request/accepted', ListAcceptedRequest.as_view(), name='accepted-requests'),
    path('appointments/request/<int:pk>/',AcceptRefuseRequest.as_view(),name='accept-refuse-appointment'),
    path('message/patient/', MessagePatient.as_view(),name='messages-patient'),
    path('message/admin/', MessageAdmin.as_view(),name='messages-admin'),
    path('message/admin/<int:pk>/', MessageAdmin.as_view(),name='messages-admin'),
    path('users/registered/',ListUser.as_view(),name='users'),
    path('image/predictor/', ImagePredictionCreateView.as_view(),name='image-predictor'),
    path('image/pdf-report/', UserPdf.as_view(), name='user-prediction-pdf'),
    path('profile/upgrade/', PremiumUpgrade.as_view(), name='upgrade-profile'),
]