from django.shortcuts import render, redirect
from django.db import transaction
import django
import calendar
from datetime import datetime, date
from .models import Job, Client, Task
from django.shortcuts import get_object_or_404
import json

# Create your views here.


def home(request):
    selected_date = request.GET.get("date")
    print(selected_date)  # DEBUG

    clients = Client.objects.all()

    return render(
        request, "dashboard.html", {"selected_date": selected_date, "clients": clients}
    )


def jobs(request):
    clients_list = list(Client.objects.all())
    tasks_list = list(Task.objects.all())
    jobs_list = list(Job.objects.all())
    if request.method == "POST":
        with transaction.atomic():
            try:
                Job.objects.create(
                    id=request.POST.get("id"),
                    enabled=request.POST.get("enabled"),
                    task_id=request.POST.get("task_id"),
                    client_id=request.POST.get("client_id"),
                    time_to_run=f"{request.POST.get("date")} {request.POST.get("time")}",
                    repeat=request.POST.get("repetition"),
                    last_task_status=request.POST.get("enabled"),
                )
            except django.db.utils.IntegrityError:
                return render(
                    request,
                    "jobs.html",
                    {
                        "clients": clients_list,
                        "tasks": tasks_list,
                        "jobs": jobs_list,
                        "error": "Eine Job unter diesem Namen existiert bereits! Siehe rechts!",
                    },
                )

    clients_list = list(Client.objects.all())
    tasks_list = list(Task.objects.all())
    jobs_list = list(Job.objects.all())
    return render(
        request,
        "jobs.html",
        {"clients": clients_list, "tasks": tasks_list, "jobs": jobs_list},
    )


def tasks(request):
    tasks_list = list(Task.objects.all())
    if request.method == "POST":
        with transaction.atomic():

            try:
                args = request.POST.get("python_args")
                if args == None:
                    args = request.POST.get("cmd_args")
                Task.objects.create(
                    id=request.POST.get("id"),
                    task_type=request.POST.get("job_type"),
                    task_data={
                        "CMD": request.POST.get("cmd_command"),
                        "SHELL_CMD": request.POST.get("shell_command"),
                        "ARGS": [],
                        "PYTHON_FILE": request.POST.get("python_file"),
                        "PYTHON_EXE": request.POST.get("python_exec"),
                    },
                )
            except django.db.utils.IntegrityError:
                return render(
                    request,
                    "tasks.html",
                    {
                        "error": "Eine Task unter diesem Namen existiert bereits! Siehe rechts!",
                        "tasks": tasks_list,
                    },
                )
    tasks_list = list(Task.objects.all())
    return render(request, "tasks.html", {"tasks": tasks_list})


from collections import defaultdict
from datetime import datetime, date
import calendar


def calendar_view(request):

    month_param = request.GET.get("month")

    if month_param:
        year, month = map(int, month_param.split("-"))
    else:
        now = datetime.now()
        year = now.year
        month = now.month

    _, num_days = calendar.monthrange(year, month)
    start_weekday, _ = calendar.monthrange(year, month)

    # Monatsrange bauen
    month_start = datetime(year, month, 1, 0, 0)
    month_end = datetime(year, month, num_days, 23, 59, 59)

    # 🔥 Jobs im Zeitraum holen
    jobs = Job.objects.filter(time_to_run__gte=month_start, time_to_run__lte=month_end)

    # 🔥 nach DATE gruppieren
    jobs_by_date = defaultdict(list)

    for job in jobs:

        job_date = job.time_to_run.date()  # 🔑 WICHTIG

        jobs_by_date[job_date].append(
            {
                "title": job.id,
                "time": job.time_to_run.strftime("%H:%M"),
                "status": ("Aktiv" if job.enabled else "Deaktiviert"),
            }
        )

    # Kalender bauen
    calendar_days = []

    for day in range(1, num_days + 1):

        current_date = date(year, month, day)

        calendar_days.append(
            {
                "day": day,
                "date": current_date,
                "jobs": jobs_by_date.get(current_date, []),
            }
        )

    # Navigation
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1

    return render(
        request,
        "calendar.html",
        {
            "current_year": year,
            "current_month": datetime(year, month, 1).strftime("%B"),
            "calendar_days": calendar_days,
            "start_weekday_range": range(start_weekday),
            "prev_month_url": f"/calendar?month={prev_year}-{prev_month}",
            "next_month_url": f"/calendar?month={next_year}-{next_month}",
        },
    )


def get_next_client_id():
    existing_ids = list(Client.objects.values_list("id", flat=True).order_by("id"))

    expected = 1
    for cid in existing_ids:
        if cid != expected:
            return expected
        expected += 1

    return expected


def client_view(request):
    if request.method == "POST":

        with transaction.atomic():
            next_id = get_next_client_id()

            # doppelte Sicherheit
            while Client.objects.filter(id=next_id).exists():
                next_id += 1

            Client.objects.create(
                id=next_id,
                name=request.POST.get("name"),
                ip=request.POST.get("ip"),
                os=request.POST.get("os"),
            )

        return redirect("/clients")

    print(f"Clients: {Client.objects.all().values_list()}")
    return render(request, "clients.html", {"clients": Client.objects.all()})


def job_detail(request, job_id):
    print(job_id)
    job = Job.objects.get(id=job_id)
    print(job)
    return render(request, "job_detail.html", {"job": job})


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)

    try:
        task_data = task.task_data
        if isinstance(task_data, str):
            task_data = json.loads(task_data)
    except Exception:
        task_data = {"raw": str(task.task_data)}

    return render(request, "task_detail.html", {"task": task, "task_data": task_data})
