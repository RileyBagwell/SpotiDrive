from django.shortcuts import render, redirect
from src.LocationHandler import LocationHandler
import datetime

from src.SpotifyHandler import SpotifyHandler


def home(request):
    if request.method == 'POST':
        return redirect('destination')
    return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})


def destination(request):
    starting_address = request.POST.get('starting_address', '')  # Get the form data
    destination_address = request.POST.get('destination_address', '')
    # You can access the form data here and use it in your 'destination' template
    return render(request, 'destination.html', {'starting_address': starting_address, 'destination_address': destination_address})


def end(request):
    starting_address = request.POST.get('starting_address', '')
    destination_address = request.POST.get('destination_address', '')
    locHandler = LocationHandler()
    spotHandler = SpotifyHandler()
    distance_seconds = locHandler.getDistance(starting_address, destination_address)
    distance_formatted = str(datetime.timedelta(seconds=distance_seconds))
    spotHandler.create_own_playlist()
    spotHandler.add_songs_until_limit(distance_seconds)
    return render(request, 'end.html', {'starting_address': starting_address,
                                        'destination_address': destination_address,
                                        'distance': distance_formatted})
