from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.show_login, name="login"),
    path('register/', views.show_register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.main_menu, name="main_menu"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('start/', views.choose_quiz, name='choose_quiz'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:q_number>/', views.show_question, name='show_question'),
    path('quiz/results/', views.show_results, name='show_results'),
    path('quiz/mixed/start/', views.start_mixed_quiz, name='start_mixed_quiz'),
    path('my_results/', views.show_my_results, name='show_my_results'),
]