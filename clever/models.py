from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class TestType(models.Model):
    name = models.CharField(max_length=50)
    question_time_sec = models.FloatField(null=True)
    test_time_sec = models.FloatField(null=True)
    allow_backward = models.BooleanField(default=True)
    show_unanswered_questions = models.BooleanField(default=False)
    one_page_display = models.BooleanField(default=False)


class Test(models.Model):
    name = models.CharField(max_length=50)
    rules = models.TextField()
    type = models.ForeignKey('TestType', on_delete=models.CASCADE)


class Question(models.Model):
    text = models.CharField(max_length=100)
    number_in_test = models.IntegerField(default=1)
    test = models.ForeignKey('Test', on_delete=models.PROTECT)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=50)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)
    question_time = models.DateTimeField(default=datetime.utcnow)
    answer_time = models.DateTimeField(null=True)
