

import forum.urls
from sentimentanalysis.views import *
import mon_chatbot.urls
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from accounts.views import *
from mon_chatbot.views import *
from quizes.views import *
from GlobalApp.views import *

from django.views.static import serve
from django.conf.urls.static import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('',include('accounts.urls',namespace='accounts')),
    path('', include(forum.urls), name='forum'),
    path('', include(mon_chatbot.urls), name='chatbot'),
    path('quize/', QuizListView.as_view(), name='main-view'),
    path('quize/<pk>/', quiz_view, name='quiz-view'),
    path('quize/<pk>/save/', save_quiz_view, name='save-view'),
    path('quize/<pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('analyser/<id>',AnalyseData, name = 'AnalyseData'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)