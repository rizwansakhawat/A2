from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    name = models.CharField(max_length=100, null=False)
    swift_code = models.CharField(max_length=100, null=False)
    inst_num = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=100, null=False)
    owner = models.ForeignKey(User , on_delete=models.CASCADE , related_name='banks')

    def __str__(self):
        return self.name


class Branch(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100, null=False)
    transit_num = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    email = models.EmailField(default='admin@enigmatix.io')
    capacity = models.PositiveIntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True )

    def __str__(self):
        return self.name
