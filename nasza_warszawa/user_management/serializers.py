from rest_framework import serializers
from .models import UM_accounts, UM_sent_messages, UM_session


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UM_accounts
        fields = ('id', 'email', 'password')


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UM_session
        fields = ('UM_account_id', 'session_id')


class SentMessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UM_sent_messages
        fields = ('id', 'UM_account_id', 'message_type', 'message_body_plaintext')