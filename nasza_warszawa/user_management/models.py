from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class UM_session(models.Model):
    UM_user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    sesssion_id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(blank=True)


class UM_sent_messages(models.Model):
    UM_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True)
    message_type = models.CharField(max_length=16)
    message_body_plaintext = models.TextField()
    created_at = models.DateTimeField(blank=True)
