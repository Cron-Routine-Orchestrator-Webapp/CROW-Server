from django.shortcuts import render,HttpResponse
import calendar
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, "test.html")


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