from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patient'

class IsPremiumPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'premium_patient'    

class IsPatientOrPremiumPatient(BasePermission):
    def has_permission(self, request, view):
        return IsPatient().has_permission(request, view) or IsPremiumPatient().has_permission(request, view)