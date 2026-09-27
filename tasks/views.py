from django.shortcuts import render
from .models import Task


def dashboard(request):
    tasks = Task.objects.select_related(
        "priority",
        "category",
    ).all()

    return render(
        request,
        "tasks/dashboard.html",
        {"tasks": tasks},
    )