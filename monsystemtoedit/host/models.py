from django.db import models


# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Members(models.Model):
    name = models.CharField(max_length=40)
    host = models.CharField(max_length=255)
    #program_id = models.IntegerField
    #cores = models.IntegerField(default=1)
    cpu_usage = models.IntegerField()
    #status = models.CharField
    #memory_usage = models.FloatField
    #n_threads = models.IntegerField

    def __str__(self) -> str:
        return self.name

class all_users_data(models.Model):
    program_name = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    host = models.CharField(max_length=255)
    program_id = models.CharField(max_length=255)
    cores = models.IntegerField(default=1)
    cpu_usage = models.FloatField()
    status = models.CharField(max_length=255)
    memory_usage = models.FloatField()
    data = models.DateTimeField(auto_now=True)
    banch_id = models.IntegerField()



    def __str__(self) -> str:
        return self.name


class agents(models.Model):
    username = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    owner_surname = models.CharField(max_length=255)
    id = models.IntegerField
    password = models.CharField(max_length=15)
    
    def __str__(self) -> str:
        return self.username
