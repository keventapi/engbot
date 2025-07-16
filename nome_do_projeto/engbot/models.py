from django.db import models

# Create your models here.
class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    requests = models.TextField()
    responses = models.TextField()
    
    

class Relatorio(models.Model):
    body = models.TextField()