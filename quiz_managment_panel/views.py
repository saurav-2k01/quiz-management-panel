from django.shortcuts import  render
from django.http import HttpResponse
from quiz.models import Quiz


def quizes(request):
    quizs = Quiz.objects.all()
    data = {
        "quizs" : quizs
    }
    return render(request, "quizes.html", data)


def quiz(request, key):
    quiz = Quiz.objects.filter(secret_key=key).first()
    questions = quiz.questions.all()
    data = {
        "quiz":quiz,
        "questions":questions
    }
    return render(request, "quiz.html", data)


def home(request):
    return render(request, "index.html")