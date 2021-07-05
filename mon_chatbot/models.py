from django.contrib.auth.models import User
from django.db import models
from GlobalApp.models import Patient
# Create your models here.

class Temp_Message(models.Model) :
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    to = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) :
        return f" {self.user.user.last_name} __ {self.to.last_name}"