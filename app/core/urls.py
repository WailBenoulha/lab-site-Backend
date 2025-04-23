from django.urls import path
from core.views import Register,list_apointements,request_apointement,accept_request

urlpatterns = [
    path('register',Register.as_view(),name='register'),
    path('appointments/', list_apointements, name='list-appointments'),
    path('appointments/request/', request_apointement, name='request-appointment'),
    path('appointments/accept/<int:pk>/', accept_request, name='accept-appointment'),
]