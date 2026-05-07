from django.shortcuts import render,redirect
from django.db import transaction
import calendar
from datetime import datetime,date
from .models import Job,Client 
# Create your views here.




def home(request):
    selected_date = request.GET.get("date")
    print(selected_date)  # DEBUG




    clients = Client.objects.all()

    return render(request, "dashboard.html", {
        "selected_date": selected_date,
        "clients": clients
    })
    


def jobs(request):
    return render(request,"jobs.html",{
        "clients": Client.objects.all()
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

        with transaction.atomic():  # 👈 WICHTIG
            next_id = get_next_client_id()

            # doppelte Sicherheit
            while Client.objects.filter(id=next_id).exists():
                next_id += 1

            Client.objects.create(
                id=next_id,
                name=request.POST.get("name"),
                ip=request.POST.get("ip"),
                os=request.POST.get("os")
            )

        return redirect("/clients")

    print(f"Clients: {Client.objects.all().values_list()}")
    return render(request, "clients.html", {
        "clients": Client.objects.all()
    })