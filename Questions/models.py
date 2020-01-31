from django.db import models
from django.utils import timezone as timezone
from django.conf import settings


# Create your models here.

class QuestionCategory(models.Model):
    category = models.CharField(default="", max_length=100)

    def __str__(self):
        return self.category
        
    class Meta:
        verbose_name = 'Question Category'
        verbose_name_plural = 'Question Categories' 

class Questions(models.Model):
    question = models.TextField(default="")
    slug = models.CharField(max_length=255, unique=True)
    time = models.DateTimeField( default= timezone.now )
    author = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            on_delete= models.DO_NOTHING
                        )    
    category = models.ForeignKey(
                            QuestionCategory,
                            on_delete= models.DO_NOTHING
                        )
    upvote = models.IntegerField(default=0)
    upvoters = models.TextField(default="", null=True, blank=True)
    anonymous = models.BooleanField (default= False)
#    upvoter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoters', null=True, blank=True, default= "admin")    
    
    def __str__(self):
        return str(self.id)+": "+self.question
        
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions' 


class Answers(models.Model):
    question = models.ForeignKey(
                            Questions,
                            on_delete= models.CASCADE
                        )
    answer = models.TextField()
    author = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            on_delete= models.DO_NOTHING
                        )
    time = models.DateTimeField( default= timezone.now )
    upvote = models.IntegerField(default=0)
    upvoters = models.TextField(default="", null=True, blank=True)
    anonymous = models.BooleanField (default= False)

    def __str__(self):
        return str(self.id)+": "+self.answer

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers' 

