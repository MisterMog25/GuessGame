import os
from hashlib import sha256
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SimpleUser, Question, QuizResult, Quiz
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
    if 'user_id' not in request.session:
        return redirect("login")
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


def choose_quiz(request):
    if 'user_id' not in request.session:
        return redirect("login")

    quizzes = Quiz.objects.all()
    total_questions = Question.objects.count()
    can_mixed = total_questions >= 20

    return render(request, "quiz/main_content/choose_quiz.html", {
        "quizzes": quizzes,
        "can_mixed": can_mixed
    })


def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())

    if len(questions) < 20:
        return redirect('choose_quiz')

    questions = sample(questions, 20)

    request.session['quiz_questions'] = [q.id for q in questions]
    request.session['current_index'] = 0
    request.session['score'] = 0
    request.session['quiz_id'] = quiz.id

    return redirect('show_question', q_number=1)


def show_question(request, q_number):
    question_ids = request.session.get('quiz_questions', [])

    if q_number - 1 >= len(question_ids):
        return redirect('show_results')

    question = get_object_or_404(Question, id=question_ids[q_number - 1])

    if request.method == "POST":
        selected = request.POST.getlist('options')
        correct = [str(i) for i in question.correct_options]

        current_score = request.session.get('score', 0)
        if set(selected) == set(correct):
            current_score += 1

        request.session['score'] = current_score
        request.session['current_index'] = q_number

        print(f"Score saved to session: {request.session['score']}")

        return redirect('show_question', q_number=q_number + 1)

    return render(request, "quiz/main_content/show_question.html", {
        "question": question,
        "q_number": q_number,
        "total_questions": len(question_ids)
    })


def show_results(request):
    user_login = request.session.get("user_login", "Guest")
    score = request.session.get("score", 0)
    quiz_id = request.session.get("quiz_id")
    is_mixed = request.session.get("is_mixed", False)

    if not is_mixed and not quiz_id:
        return redirect('main_menu')

    if is_mixed:
        quiz_title = "Змішана вікторина"
        top_players = []
    else:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz_title = quiz.title

        QuizResult.objects.create(
            user_login=user_login,
            quiz=quiz,
            score=score
        )

        all_results = QuizResult.objects.filter(quiz=quiz)
        user_best = {}

        for result in all_results:
            if result.user_login not in user_best or result.score > user_best[result.user_login].score:
                user_best[result.user_login] = result

        top_players = sorted(user_best.values(), key=lambda x: x.score, reverse=True)[:20]

    request.session.pop('quiz_questions', None)
    request.session.pop('quiz_id', None)
    request.session.pop('score', None)
    request.session.pop('current_index', None)
    request.session.pop('is_mixed', None)

    return render(request, "quiz/main_content/results.html", {
        "score": score,
        "total_questions": 20,
        "top_players": top_players,
        "quiz_title": quiz_title,
        "user_login": user_login,
        "is_mixed": is_mixed
    })


def start_mixed_quiz(request):
    all_questions = list(Question.objects.all())
    selected_questions = sample(all_questions, min(len(all_questions), 20))

    request.session['quiz_questions'] = [q.id for q in selected_questions]
    request.session['current_index'] = 0
    request.session['score'] = 0
    request.session['quiz_id'] = None
    request.session['is_mixed'] = True

    return redirect('show_question', q_number=1)


def show_my_results(request):
    user_login = request.session.get("user_login")

    if not user_login:
        return redirect("login")

    all_quizzes = Quiz.objects.all()

    if request.method == "POST":
        selected_quiz_ids = request.POST.getlist("quizzes")
        if selected_quiz_ids:
            results = QuizResult.objects.filter(
                user_login=user_login,
                quiz_id__in=selected_quiz_ids
            ).select_related('quiz').order_by('-date_taken')
        else:
            results = QuizResult.objects.filter(user_login=user_login).select_related('quiz').order_by('-date_taken')
    else:
        results = QuizResult.objects.filter(user_login=user_login).select_related('quiz').order_by('-date_taken')

    return render(request, "quiz/main_content/show_my_results.html", {
        "all_quizzes": all_quizzes,
        "results": results
    })

