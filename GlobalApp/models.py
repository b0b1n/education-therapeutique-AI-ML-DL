from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField, IntegerField, TextField
from django.contrib.auth.models import User , Group

Expert_CHOICES = (
    ("1", "Docteur"),
    ("2", "kine"),
    ("3", "nutritioniste"),

)
Sexe_CHOICES = (
    ("1", "Male"),
    ("2", "Female")
)



class Infermier(models.Model):
    nom = models.CharField(max_length=150,null=True)
    mail = models.EmailField(max_length=100,null=True)
    def __str__(self):
        return self.nom

class Expert(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,null=True)
    type = models.CharField(max_length=20, choices=Expert_CHOICES)
    date_rejoin = models.DateTimeField(auto_now=True)
    sexe = models.CharField(max_length=10, choices=Sexe_CHOICES)
    tel = models.CharField(max_length=100)  
    def __str__(self):
        return f" {self.user.first_name}  {self.user.last_name}"



class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,null=True)
    dateNaissance = models.DateTimeField()
    bio = models.TextField(max_length=500)
    sexe = models.CharField(max_length=10, choices=Sexe_CHOICES)
    tel = models.CharField(max_length=100)
    experts = models.ManyToManyField('Expert')
    amies = models.ManyToManyField('self',blank=True)

    def __str__(self):
        return f" {self.user.first_name} ::  {self.user.last_name}"



class Poste(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    titre = models.CharField(max_length=10000, null=True)
    contenu = models.TextField(max_length=10000)
    #poste est publié par un expert
    publie_par = models.ForeignKey(Expert,on_delete=CASCADE)
    def __str__(self):
        return self.titre
    

class publication(models.Model):
    poste_publie = models.ForeignKey('Poste',on_delete=CASCADE)
    publie_dans = models.ForeignKey('room',on_delete=CASCADE)

class room(models.Model):
    nomGroup =  models.ForeignKey(Group,on_delete=CASCADE,null=True)
    createur = models.ForeignKey('Infermier', on_delete=CASCADE)
    members = models.ManyToManyField(Patient)
    def __str__(self):
        return self.nomGroup.name


class Contact(models.Model):
    nom = models.CharField(max_length=50)
    mail = models.EmailField(max_length=200)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return self.nom     
