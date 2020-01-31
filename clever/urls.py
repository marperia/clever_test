from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('test/<int:pk>/', views.test, name='test'),
    path('question/<int:test_id>/<int:q_num>/', views.question, name='question'),
]