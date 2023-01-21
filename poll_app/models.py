from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    
    option_1_votes = models.IntegerField(default=0)
    option_2_votes = models.IntegerField(default=0)
    option_3_votes = models.IntegerField(default=0)
    option_4_votes = models.IntegerField(default=0)
    
    date = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return self.question