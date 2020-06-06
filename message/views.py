from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(methods=['POST'], detail=True)
    def create_message(self, request, *args, **kwargs):
        user = self.get_object()
        subject = request.data['subject']
        message = request.data['message']
        try:
            receiver = Person.objects.get(email=request.data['receiver'])
            new_message = Message.objects.create(subject=subject, message=message, sender=user, receiver=receiver)
            new_message.save()
            serializer = MessageSerializer(new_message)
            user.send_messages.add(new_message)
            user.save()
            receiver.received_messages.add(new_message)
            receiver.save()
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response({'message': 'Receiver does not exist', 'status': status.HTTP_404_NOT_FOUND})

    @action(methods=['PATCH'], detail=True)
    def read_message(self, request, *args, **kwargs):
        user = self.get_object()
        message_id = int(request.data['message_id'])
        for message in user.received_messages.all():
            if message.pk == message_id:
                try:
                    message_to_read = Message.objects.get(id=message_id)
                    message_to_read.is_read = True
                    message_to_read.save()
                    serializer = MessageSerializer(message_to_read)
                    user.save()
                    return Response(serializer.data)
                except Message.DoesNotExist:
                    return Response({'message': 'Message does not exist', 'status': status.HTTP_404_NOT_FOUND})

            else:
                return Response({'message': 'User does not have the message', 'status': status.HTTP_400_BAD_REQUEST})

    @action(methods=['GET'], detail=True)
    def get_unread_messages(self, request, *args, **kwargs):
        user = self.get_object()
        user_unread_received_messages = user.received_messages.filter(is_read=False)
        serializer = MessageSerializer(user_unread_received_messages, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def get_all_messages(self, request, *args, **kwargs):
        user = self.get_object()
        send_messages = user.send_messages.all()
        received_messages = user.received_messages.all()
        send_serializer = MessageSerializer(send_messages, many=True)
        received_serializer = MessageSerializer(received_messages, many=True)
        return Response({'send': send_serializer.data, 'received': received_serializer.data})

    @action(methods=['POST'], detail=True)
    def delete_message(self, request, *args, **kwargs):
        user = self.get_object()
        message_id_to_remove = int(request.data['message_id'])
        send_messages = user.send_messages.all()
        received_messages = user.received_messages.all()
        self._remove_message_from_list(send_messages, message_id_to_remove)
        self._remove_message_from_list(received_messages, message_id_to_remove)

        return Response({'message': 'message is removed successfully', 'status': status.HTTP_204_NO_CONTENT})

    def _remove_message_from_list(self, messages, message_id_to_remove):
        for message in messages:
            if message.pk == message_id_to_remove:
                message = Message.objects.get(pk=message_id_to_remove)
                message.delete()