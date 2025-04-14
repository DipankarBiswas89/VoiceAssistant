from django.db import models

# Create your models here.
class Interaction(models.Model):
     user_input = models.TextField()
     ai_requests = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
        return f"Interaction at {self.created_at}"