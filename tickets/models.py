from django.db import models
from django.contrib.auth.models import User


class Tech(models.Model):
    name= models.CharField(max_length=200)
    last_name= models.CharField(max_length=200)
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=1)
    avatar = models.ImageField(null=True, blank=True,upload_to="techs")
    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'



class History(models.Model):
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Created at")
    
    def __str__(self) -> str:
        return self.description

class Status(models.Model):
    name= models.CharField(max_length=200,verbose_name="Status")

    def __str__(self) -> str:
        return self.name

def get_default_status_id():
    status,created = Status.objects.get_or_create(name="Open")
    return status.id

class Ticket(models.Model):
    title = models.CharField(max_length=200,verbose_name='Titulo')
    description = models.TextField(verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Fecha creacion')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Fecha modificacion')
    tech = models.ForeignKey(Tech,null=True,blank=True,on_delete=models.RESTRICT)
    history = models.ManyToManyField(History)
    status = models.ForeignKey(Status,null=True,blank=True,on_delete=models.RESTRICT,default=get_default_status_id)

    def __str__(self) -> str:
        return self.title