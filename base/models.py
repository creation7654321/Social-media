from django.db import models
from django.contrib.auth.models import User


# Create your models here.




class Post(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(null=True, default=None, upload_to='images/', max_length=250)


    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title







