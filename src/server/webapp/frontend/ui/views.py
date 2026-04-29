from django.shortcuts import render,redirect

import calendar
from datetime import datetime
from .models import Job  
# Create your views here.

def home(request):
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

    return render(request, "test.html", {
        "programs": programs,
        "calendar_days": []  # erstmal leer
    })


    




def calendar_view(request):
    now = datetime.now()

    year = now.year
    month = now.month

    # Wochentag des 1. Tages (0=Montag)
    start_weekday, num_days = calendar.monthrange(year, month)

    context = {
        "current_year": year,
        "current_month": now.strftime("%B"),
        "current_month_number": month,
        "month_days": list(range(1, num_days + 1)),
        "start_weekday_range": range(start_weekday),
        "jobs": None#Job.objects.all()
    }

    return render(request, "calendar.html", context)