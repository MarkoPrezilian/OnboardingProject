from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        order_with_respect_to = 'createdAt'

