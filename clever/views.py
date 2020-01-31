from datetime import datetime

from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect

from clever.forms import AnswerForm
from clever.models import Question, Test, Answer


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
    quest = get_object_or_404(Question, test=test_id, number_in_test=q_num)
    print(quest.id, request.user)
    answer_exists = Answer.objects.filter(question=quest, user=request.user,
                                          ).exclude(text__isnull=True
                                          ).exclude(text__exact='').exists()
    if not answer_exists:
        answer = Answer.objects.create(
            user=request.user,
            question_time=datetime.utcnow(),
            question=quest,
        )
        answer.save()
        form = AnswerForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                # form.
                form.save()
                return redirect(question, test_id=test_id, q_num=q_num + 1)
    else:
        errors.append('Вы уже ответили на этот вопрос, ответ нельзя изменить')

    context = {
        'question': quest,
        'errors': errors,
        'form': form,
        'name': 'Вопрос №' + str(quest.number_in_test),
        'test': test,
        'next_question_id': q_num + 1,
    }
    return render(request, 'question.html', context)
