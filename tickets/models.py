from django.db import models

class Ticket(models.Model):
    title = models.CharField(max_length=200,verbose_name='Titulo')
    description = models.TextField(verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Fecha creacion')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Fecha modificacion')


    def __str__(self) -> str:
        return self.title
    