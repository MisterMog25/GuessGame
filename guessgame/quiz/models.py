# from django.db import models
#
#
# class SimpleUser(models.Model):
#     login = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=64)
#     birthdate = models.DateField()
#
#     def __str__(self):
#         return self.login
#
# class Question(models.Model):
#     CATEGORY_CHOICES = [
#         ("math", "Math"),
#         ("chemistry", "Chemistry"),
#         ("english", "English"),
#     ]
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
#     question = models.CharField(max_length=200)
#     first_option = models.CharField(max_length=200)
#     second_option = models.CharField(max_length=200)
#     third_option = models.CharField(max_length=200)
#     fourth_option = models.CharField(max_length=200)
#     correct_options = models.JSONField(default=list)
#
#     def __str__(self):
#         return f"{self.category} - {self.question}"
#
#
# class QuizResult(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     user_login = models.CharField(max_length=200)
#     score = models.IntegerField()
#     categories = models.JSONField(default=list)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user_login}  - {self.categories}"

from django.db import models

class SimpleUser(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=64)
    birthdate = models.DateField()
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.login

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(max_length=200)
    first_option = models.CharField(max_length=200)
    second_option = models.CharField(max_length=200)
    third_option = models.CharField(max_length=200)
    fourth_option = models.CharField(max_length=200)
    correct_options = models.JSONField(default=list)

    def __str__(self):
        return f"{self.quiz.title} - {self.question}"

class QuizResult(models.Model):
    user_login = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_login} - {self.quiz.title} - {self.score}"