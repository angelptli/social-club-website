from django.shortcuts import render
from django.http import HttpResponseRedirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from . import models
from .models import Event, Venue
from .forms import VenueForm


def search_venues(request):
    if request.method == "POST":
        searched = request.POST.get('searched')

        # Allow partial search words for venue searches
        venues = Venue.objects.filter(name__contains=searched)

        return render(request,
            'events/search_venues.html', {
            "searched":searched,
            "venues":venues})

    else:
        return render(request,
            'events/search_venues.html', {
            })


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)

    return render(request,
        'events/show_venue.html', {
        "venue": venue})


def list_venues(request):
    venue_list = Venue.objects.all()

    return render(request,
        'events/venue.html', {
        "venue_list": venue_list})


def add_venue(request):
    # If user filled out form and clicked submit button, they have posted
    # their form. If their form has posted then take the form and pass
    # into VenueForm. Else notify that the form has already been submitted.
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)

        # If input is valid then save to database
        if form.is_valid():
            form.save()

            # Return with submitted true tag
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
        'events/add_venue.html', {
        "form":form,
        "submitted": submitted,
        })


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