from django.db import models


# Create your models here.

class UM_accounts(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.CharField(max_length=128)
    password = models.TextField(max_length=512)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True)


class UM_sent_messages(models.Model):
    UM_account_id = models.ForeignKey(UM_accounts, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True)
    message_type = models.CharField(max_length=16)
    message_body_plaintext = models.TextField()
    created_at = models.DateTimeField()


class UM_session(models.Model):
    UM_account_id = models.OneToOneField(UM_accounts, on_delete=models.CASCADE)
    session_id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
