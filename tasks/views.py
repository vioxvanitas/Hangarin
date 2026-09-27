from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import Task


@login_required
def dashboard(request):
    tasks = list(Task.objects.select_related(
        "priority",
        "category",
    ))
    current_time = timezone.now()
    pending_count = sum(task.status == "Pending" for task in tasks)
    in_progress_count = sum(task.status == "In Progress" for task in tasks)
    overdue_count = sum(
        task.deadline is not None
        and task.deadline < current_time
        and task.status != "Completed"
        for task in tasks
    )

    return render(
        request,
        "tasks/dashboard.html",
        {
            "tasks": tasks,
            "current_time": current_time,
            "pending_count": pending_count,
            "in_progress_count": in_progress_count,
            "overdue_count": overdue_count,
        },
    )