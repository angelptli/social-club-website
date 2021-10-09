from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from . import models
from .models import Event


def all_events(request):
    event_list = Event.objects.all()

    return render(request,
        'events/event_list.html', {
        "event_list": event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Angel"
    month = month.capitalize()

    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get current year
    now = datetime.now()
    current_year = now.year

    # Get current time
    time = now.strftime('%I:%M %p')

    return render(request,
        'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
        })