from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='receiver')

    def __str__(self):
        return self.subject


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    send_messages = models.ManyToManyField(Message, blank=True, related_name='send_messages')
    received_messages = models.ManyToManyField(Message, blank=True, related_name='received_messages')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name
