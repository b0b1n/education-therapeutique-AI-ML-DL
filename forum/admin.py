from forum.models import est_membre_de
from django.contrib import admin
from .models import est_membre_de, a_comme_contact, message

# Register your models here.

admin.site.register(est_membre_de)
admin.site.register(a_comme_contact)
admin.site.register(message)