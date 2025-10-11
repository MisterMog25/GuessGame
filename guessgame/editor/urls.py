from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_editor, name='main_page_m'),
    path('login/', views.show_login, name='login_m'),
    path('logout/', views.logout_view, name="logout_m")
]