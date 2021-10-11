from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from . import models
from .models import Event, Venue
from .forms import VenueForm, EventForm


# Generate Text File Venue List
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # Designate the model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    # Loop through and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n'
                     f'{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')

    # lines = ["This is line 1\n",
    #          "This is line 3\n",
    #          "This is line 4\n",]
    # # Write to text file

    response.writelines(lines)

    return response



def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()

    return redirect('list-events')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    
    return redirect('list-venues')


def add_event(request):
    # If user filled out form and clicked submit button, they have posted
    # their form. If their form has posted then take the form and pass
    # into VenueForm. Else notify that the form has already been submitted.
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)

        # If input is valid then save to database
        if form.is_valid():
            form.save()

            # Return with submitted true tag
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
        'events/add_event.html', {
        "form":form,
        "submitted": submitted,
        })


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)

    if form.is_valid():
        form.save()

        return redirect('list-venues')

    return render(request,
        'events/update_venue.html', {
        "venue": venue,
        "form":form,
        })


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()

        return redirect('list-events')

    return render(request,
        'events/update_event.html', {
        "event": event,
        "form":form,
        })


def search_venues(request):
    if request.method == "POST":
        searched = request.POST.get('searched')

        # Allow partial search words for venue searches
        venues = Venue.objects.filter(name__contains=searched)

        return render(request,
            'events/search_venues.html', {
            "searched":searched,
            "venues":venues
            })

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
    # Order by name. Order randomly by using '?'.
    venue_list = Venue.objects.all().order_by('name')

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
    event_list = Event.objects.all().order_by('event_date')

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