import os
from hashlib import sha256
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SimpleUser


def show_login(request):
    if request.method == "POST":
        entered_login = request.POST.get("login", "")
        entered_password = sha256(request.POST.get("password", "").encode()).hexdigest()

        try:
            user = SimpleUser.objects.get(login=entered_login, password=entered_password)
            request.session['user_id'] = user.id
            return redirect("main_menu")
        except SimpleUser.DoesNotExist:
            messages.error(request, "Невірний логін або пароль!")

    return render(request, "quiz/login.html")


def show_register(request):
    if request.method == "POST":
        login_input = request.POST.get("login", "")
        password_input = request.POST.get("password", "")
        birthdate_input = request.POST.get("birthdate", "")

        password_hash = sha256(password_input.encode()).hexdigest()

        if SimpleUser.objects.filter(login=login_input).exists():
            messages.error(request, "Такий логін уже існує!")
            return redirect("register")

        SimpleUser.objects.create(
            login=login_input,
            password=password_hash,
            birthdate=birthdate_input
        )
        messages.success(request, "Реєстрація успішна! Тепер увійдіть.")
        return redirect("login")

    return render(request, "quiz/register.html")


def main_menu(request):
    if 'user_id' not in request.session:
        return redirect("login")

    user = SimpleUser.objects.get(id=request.session['user_id'])
    return render(request, "quiz/main_menu.html", {"user": user})


def logout_view(request):
    request.session.flush()
    return redirect("login")

def edit_profile(request):
    user = SimpleUser.objects.get(id=request.session['user_id'])

    if request.method == "POST":
        new_password = request.POST.get("password", "")
        new_birthdate = request.POST.get("birthdate", "")

        if new_password:
            user.password = sha256(new_password.encode()).hexdigest()

        if new_birthdate:
            user.birthdate = new_birthdate

        user.save()
        messages.success(request, "Ваші дані успішно оновлено!")
        return redirect("main_menu")

    return render(request, "quiz/edit_profile.html", {"user": user})

