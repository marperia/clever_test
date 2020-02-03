from time import time
from datetime import datetime

from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect

from clever.forms import AnswerForm
from clever.models import Question, Test, Answer, TestType


def home(request):
    tests = Test.objects.all()
    context = {
        'name': 'Главная',
        'tests': tests,
    }
    return render(request, 'index.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(request, username=username, password=raw_password)
        login(request, user)

        return redirect('profile')

    context = {
        'name': 'Регистрация',
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


@login_required
def profile(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if request.method == 'POST':
        form.user = request.user
        form.data = request.POST
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    context = {
        'name': 'Профиль',
        'form': form,
    }
    return render(request, 'registration/profile.html', context)


@login_required
def test(request, pk):
    my_test = get_object_or_404(Test, pk=pk)
    context = {
        'name': my_test.name,
        'test': my_test,
    }
    return render(request, 'test.html', context)


@login_required
def question(request, test_id, q_num):
    form = None
    errors = []
    time_left = 0
    quest_time = 0
    quest = get_object_or_404(Question, test=test_id, number_in_test=q_num)
    answer_exists = Answer.objects.filter(question=quest, user=request.user,
                                          ).exclude(text__isnull=True
                                          ).exclude(text__exact='').exists()
    if not answer_exists:
        test = Test.objects.get(pk=test_id)
        test_config = TestType.objects.filter(name=test.type.name).first()

        if test_config.question_time_sec != 0:
            quest_time = test_config.question_time_sec

        if test_config.test_time_sec != 0:
            time_left = int(time()) - test_config.test_time_sec

        answer_tuple = Answer.objects.get_or_create(
            user=request.user,
            question_id=quest.id,
        )
        answer = answer_tuple[0]
        form = AnswerForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                answer.answer_time = datetime.utcnow()
                answer.text = request.POST['text']
                answer.save()
                return redirect(question, test_id=test_id, q_num=q_num + 1)
        if not answer_tuple[1]:
            answer.save()
    else:
        errors.append('Вы уже ответили на этот вопрос, ответ нельзя изменить')

    context = {
        'question': quest,
        'errors': errors,
        'form': form,
        'time_left': time_left,
        'quest_time': quest_time,
        'name': 'Вопрос №' + str(quest.number_in_test),
        'next_question_id': q_num + 1,
    }
    return render(request, 'question.html', context)
