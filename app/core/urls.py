from django.urls import path
from core.views import (Register,
                        ListPendingAppointments,
                        request_apointement,
                        AcceptRefuseRequest,
                        MessagePatient,
                        MessageAdmin,
                        ListUser)

urlpatterns = [
    path('register',Register.as_view(),name='register'),
    path('appointments/', ListPendingAppointments.as_view(), name='list-appointments'),
    path('appointments/request/', request_apointement, name='request-appointment'),
    path('appointments/request/<int:pk>/',AcceptRefuseRequest.as_view(),name='accept-refuse-appointment'),
    path('message/patient/', MessagePatient.as_view(),name='messages-patient'),
    path('message/admin/', MessageAdmin.as_view(),name='messages-admin'),
    path('message/admin/<int:pk>/', MessageAdmin.as_view(),name='messages-admin'),
    path('users/registered/',ListUser.as_view(),name='users')
]