from django.db import models
from django.utils import timezone as timezone


# Create your models here.
class ForgotLog(models.Model):
    username = models.CharField ( max_length=200 )
    date = models.DateTimeField(default= timezone.now)
    token = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = 'Forgot Token'
        verbose_name_plural = 'Forgot Tokens'