from django.urls import path
from .views import *


urlpatterns = [
    path('forum/<int:id>', forum_page_groupe, name='forum_g'),
    path('forum/<slug:usrname>', forum_page_amis, name='forum_a'),
    path('forum/', forum_page, name='forum'),
    path('forum/<int:id>/<int:pk>', poste_pub, name='forum_p'),
    path('forum/<slug:usrname>/<int:id>', env_message, name='forum_m'),
]
