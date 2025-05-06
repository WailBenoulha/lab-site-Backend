from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('patient','Patient'),
        ('premium_patient','Premium_Patient'),
    )
    fullname = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=100,choices=ROLE_CHOICES,default='patient')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Appointements(models.Model):
    STATUS_CHOICES = [
        ('accepted','Accepted'),
        ('pending','Pending'),
        ('rejected','Rejected')
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)        
    fullname = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=200,
        choices=STATUS_CHOICES,
        default='pending'
    )
    notification = models.CharField(null=True,blank=True)

    def __str__(self):
        return f"{self.fullname} - {self.date} - {self.time}"

class Message(models.Model):   
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE) 
    name = models.CharField(max_length=200) 
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(null=True)

    def __str__(self):
        return f'{self.name} - {self.user} - {self.subject}'   
    
import os
import joblib
import numpy as np
from PIL import Image
from django.conf import settings
from django.db import models
import tensorflow as tf

class ImagePrediction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='image_predictions')
    image = models.ImageField(upload_to='uploads/')
    prediction = models.CharField(max_length=50, blank=True, editable=False)
    datetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save image first
        self.prediction = self.make_prediction()
        super().save(update_fields=['prediction'])

    def make_prediction(self):
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'lab_model.h5')
        model = tf.keras.models.load_model(model_path)

        image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
        img = Image.open(image_path).resize((150, 150)).convert("RGB")  # use RGB if model was trained on 3 channels

        img_array = np.array(img) / 255.0  # Normalize as in training
        img_array = img_array.reshape((1, 150, 150, 3))  # Shape: (1, 150, 150, 3)

        pred = model.predict(img_array)[0][0]  # Binary prediction

        return "Normal" if pred > 0.5 else "Anormal"