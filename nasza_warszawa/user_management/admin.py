from django.contrib import admin
from .models import UM_session, UM_sent_messages

# Register your models here.
admin.site.register(UM_session)
admin.site.register(UM_sent_messages)