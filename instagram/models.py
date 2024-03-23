from django.db import models

# Create your models here.

class Userprofile(models.Model):
    username = models.TextField(null=False,blank=False)
    businessCartegory = models.TextField(null=False,blank=False)
    businessBio = models.TextField(null=False,blank=False)
    businessObjective = models.TextField(null=False,blank=False)
    businessGoal = models.TextField(null=False,blank=False)
    location = models.TextField(null=False,blank=False)

    def __str__(self):
        return f"{self.username}"