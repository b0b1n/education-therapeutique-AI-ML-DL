from django.contrib.auth.models import User
from django.db import models
from GlobalApp.models import Patient
# Create your models here.

class DataSaisi(models.Model) :
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    texte = models.CharField(max_length=10000)
    to = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) :
        return f" {self.user.user.first_name} {self.user.user.last_name}  and {self.to.first_name} {self.to.last_name}"
