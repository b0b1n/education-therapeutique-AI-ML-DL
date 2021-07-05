from django.db import models
from GlobalApp.models import *
# Create your models here.

class est_membre_de(models.Model):
    pat = models.ForeignKey(Patient,on_delete=models.CASCADE)
    grp = models.ForeignKey(room,on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.pat.user.first_name} membre dans   {self.grp.nomGroup}"

class a_comme_contact(models.Model): 
    util_connecte = models.ForeignKey(Patient, on_delete = models.CASCADE)    
    son_contact = models.ForeignKey(User, on_delete = models.CASCADE)   

    def __str__(self):
        return f"{self.util_connecte} ' et ' {self.son_contact}"


class message(models.Model):
    connection = models.ForeignKey(a_comme_contact, on_delete = models.CASCADE, null=True)    
    connecte_a_contact = models.BooleanField(default=True, null=True)
    msg = models.TextField(max_length=5000)  
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.connection.util_connecte} ' et ' {self.connection.son_contact}"

