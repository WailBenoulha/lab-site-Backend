from django.urls import path
from core.views import Register,ListPendingAppointments,request_apointement,AcceptRefuseRequest

urlpatterns = [
    path('register',Register.as_view(),name='register'),
    path('appointments/', ListPendingAppointments.as_view(), name='list-appointments'),
    path('appointments/request/', request_apointement, name='request-appointment'),
    path('appointments/request/<int:pk>/',AcceptRefuseRequest.as_view(),name='accept-refuse-appointment')
]