from django.db import models


class SimpleUser(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=64)
    birthdate = models.DateField()

    def __str__(self):
        return self.login

class Math(models.Model):
    id = models.IntegerField("№", primary_key=True)
    question = models.CharField(max_length=100)
    first_option = models.CharField(max_length=100)
    second_option = models.CharField(max_length=100)
    third_option = models.CharField(max_length=100)
    fourth_option = models.CharField(max_length=100)

class Chemistry(models.Model):
    id = models.IntegerField("№", primary_key=True)
    question = models.CharField(max_length=100)
    first_option = models.CharField(max_length=100)
    second_option = models.CharField(max_length=100)
    third_option = models.CharField(max_length=100)
    fourth_option = models.CharField(max_length=100)

class English(models.Model):
    id = models.IntegerField("№", primary_key=True)
    question = models.CharField(max_length=100)
    first_option = models.CharField(max_length=100)
    second_option = models.CharField(max_length=100)
    third_option = models.CharField(max_length=100)
    fourth_option = models.CharField(max_length=100)