from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.show_login, name="login"),
    path('register/', views.show_register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.main_menu, name="main_menu"),
    path('edit_profile/', views.edit_profile, name="edit_profile")
]