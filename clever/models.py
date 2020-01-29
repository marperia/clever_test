from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class TestType(models.Model):
    name = models.CharField
    allow_backward = models.BooleanField(default=True)
    question_time_sec = models.FloatField
    test_time_sec = models.FloatField
    show_questions = models.BooleanField
    one_page_display = models.BooleanField(default=False)


class Test(models.Model):
    name = models.CharField
    rules = models.TextField
    type = models.ForeignKey('TestType', on_delete=models.CASCADE)


class Questions(models.Model):
    text = models.CharField
    answer = models.CharField
    test = models.ForeignKey('Test', )


class Anwers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField
    question_time = models.DateTimeField()
    answer_time = models.DateTimeField()


