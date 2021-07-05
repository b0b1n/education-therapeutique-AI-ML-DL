from django.urls import path
from .views import *
app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('profil/', profile_view, name='profile'),
    path('info/<id>',my_info, name='my_info'),
    path('amis/<id>',amis, name='amis'),
    path('experts/<id>',experts, name='experts'),
    path('groupes/<id>',groupes, name='groupes'),
]