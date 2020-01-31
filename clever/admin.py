from django.contrib import admin

from clever.models import Test, TestType, Question, Answer

admin.site.register(
    [
        Test,
        Answer,
        Question,
        TestType,
    ]
)
