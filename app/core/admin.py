from django.contrib import admin
from .models import CustomUser,Appointements,Message

admin.site.register(CustomUser)
admin.site.register(Appointements)
admin.site.register(Message)