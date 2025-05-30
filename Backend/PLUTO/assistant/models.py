from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Interaction(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     user_input = models.TextField()
     ai_requests = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
        return f"{self.user.username}: {self.user_input[:50]}"