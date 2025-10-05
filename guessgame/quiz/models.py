from django.db import models


class SimpleUser(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=64)
    birthdate = models.DateField()

    def __str__(self):
        return self.login