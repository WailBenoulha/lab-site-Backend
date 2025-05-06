from django.contrib import admin
from .models import CustomUser,Appointements,Message,ImagePrediction

admin.site.register(CustomUser)
admin.site.register(Appointements)
admin.site.register(Message)
admin.site.register(ImagePrediction)