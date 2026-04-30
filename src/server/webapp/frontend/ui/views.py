from django.shortcuts import render,redirect

import calendar
from datetime import datetime,date
from .models import Job,Client 
# Create your views here.

def dashboard(request):
    print("POST angekommen")
    if request.method == "POST":
        print("If abfrage bestanden")
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        time = request.POST.get("time")
        status = request.POST.get("status")

        # 👉 in DB speichern
        Job.objects.create(
            title=title,
            description=description,
            date=date,
            time=time,
            status=status,
        )

        return redirect("dashboard")  # verhindert doppelte submits

    programs = Job.objects.all()

    return render(request, "dashboard.html", {
        "programs": programs,
        "calendar_days": []  # erstmal leer
    })

def home(request):
    selected_date = request.GET.get("date")
    print(selected_date)  # DEBUG




    clients = Client.objects.all()

    return render(request, "dashboard.html", {
        "selected_date": selected_date,
        "clients": clients
    })
    





def calendar_view(request):
    now = datetime.now()
    year = now.year
    month = now.month

    start_weekday, num_days = calendar.monthrange(year, month)

    calendar_days = []

    for day in range(1, num_days + 1):
        current_date = date(year, month, day)

        calendar_days.append({
            "day": day,
            "date": current_date,
            "jobs": []  # später: deine DB Jobs filtern
        })

    context = {
        "current_year": year,
        "current_month": now.strftime("%B"),
        "calendar_days": calendar_days,
        "start_weekday_range": range(start_weekday),
    }

    return render(request, "calendar.html", context)