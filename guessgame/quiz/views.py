import os
from hashlib import sha256
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SimpleUser, Question, QuizResult
from random import sample


def show_login(request):
    if request.method == "POST":
        entered_login = request.POST.get("login", "")
        entered_password = sha256(request.POST.get("password", "").encode()).hexdigest()

        try:
            user = SimpleUser.objects.get(login=entered_login, password=entered_password)
            request.session['user_id'] = user.id
            request.session['user_login'] = entered_login
            return redirect("main_menu")
        except SimpleUser.DoesNotExist:
            messages.error(request, "Невірний логін або пароль!")

    return render(request, "quiz/log-reg-edit/login.html")


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

    return render(request, "quiz/log-reg-edit/register.html")


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

    return render(request, "quiz/log-reg-edit/edit_profile.html", {"user": user})

def start_quiz(request):
    if request.method == "POST":
        selected_categories = request.POST.getlist("categories")
        if not selected_categories:
            messages.error(request, "Оберіть хоча б одну категорію!")
            return redirect("choose_quiz")

        questions = Question.objects.filter(category__in=selected_categories)
        questions = list(questions)
        questions = sample(questions, min(len(questions), 5))

        request.session['quiz_questions'] = [q.id for q in questions]
        request.session['current_question'] = 0
        request.session['quiz_categories'] = selected_categories
        request.session['score'] = 0

        return redirect("show_question", q_number=1)

    return render(request, "quiz/main_content/start_new_quiz.html")

def show_question(request, q_number):
    quiz_questions = request.session.get('quiz_questions', [])
    if not quiz_questions:
        return redirect("choose_quiz")

    if q_number > len(quiz_questions):
        return redirect("show_results")

    question_id = quiz_questions[q_number - 1]
    question = Question.objects.get(id=question_id)

    if request.method == "POST":
        selected_options = request.POST.getlist("options")
        correct = set(map(str, question.correct_options))
        if set(selected_options) == correct:
            score = request.session.get("score", 0)
            request.session["score"] = score + 1
            print(score)

        request.session['current_question'] = q_number
        return redirect("show_question", q_number=q_number + 1)

    return render(request, "quiz/main_content/show_question.html", {"question": question, "q_number": q_number})

def show_results(request):
    user_login = request.session.get("user_login", "None")
    score = request.session.get("score", 0)
    categories = request.session.get("quiz_categories", [])

    QuizResult.objects.create(
        user_login=user_login,
        score=score,
        categories=categories
    )

    all_results = QuizResult.objects.all()

    top_players = []
    user_best_scores = {}
    for result in all_results:
        if set(result.categories) == set(categories):
            key = result.user_login
            if key not in user_best_scores or result.score > user_best_scores[key].score:
                user_best_scores[key] = result

    top_players = sorted(user_best_scores.values(), key=lambda x: x.score, reverse=True)[:20]

    return render(request, "quiz/main_content/results.html", {"score": score, "top_players": top_players, "user_login": user_login, "categories": categories})

def show_my_results(request):
    user_login = request.session.get("user_login")
    results = QuizResult.objects.filter(user_login=user_login)

    selected_categories = []
    if request.method == "POST":
        selected_categories = request.POST.getlist("categories")
        if selected_categories:
            filtered_results = []
            for result in results:
                if any(cat in result.categories for cat in selected_categories):
                    filtered_results.append(result)

            results = sorted(filtered_results, key=lambda x: x.score, reverse=True)
        else:
            results = []
    else:
        results = []

    return render(request, "quiz/main_content/show_my_results.html", {"results": results, "selected_categories": selected_categories})