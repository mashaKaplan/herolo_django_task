from abc import ABC

from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field='email')
    receiver = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Message
        fields = ('id', 'message', 'subject', 'creation_date', 'sender', 'receiver', 'is_read')
        read_only_fields = ('id',)


class PersonSerializer(serializers.ModelSerializer):
    send_messages = MessageSerializer(many=True)
    received_messages = MessageSerializer(many=True)

    class Meta:
        model = Person
        fields = ('id', 'full_name', 'received_messages', 'send_messages', 'email')
        read_only_fields = ('id',)
