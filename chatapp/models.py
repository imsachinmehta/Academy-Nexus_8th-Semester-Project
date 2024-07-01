from django.db import models
from portal.models import User
# Create your models here.
class Room(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200,blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.name
    

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
    def __str__(self):
        return self.content

class PersonalMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
    def __str__(self):
        return self.sender.username + " to " + self.receiver.username + " : " + self.content