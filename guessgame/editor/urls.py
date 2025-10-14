from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_editor, name='main_page_m'),
    path('login/', views.show_login, name='login_m'),
    path('logout/', views.logout_view, name="logout_m"),
    path('add_quiz/', views.add_quiz, name="add_quiz"),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name="delete_quiz"),
    path('add_question/<int:quiz_id>/', views.add_question, name="add_question"),
    path('view_questions/<int:quiz_id>/', views.view_questions, name="view_question"),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('<int:quiz_id>/edit_question/<int:question_id>/', views.edit_question, name="edit_question"),
]