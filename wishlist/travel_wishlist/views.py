from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewPlaceForm, TripReviewForm
from .models import Place
from django.contrib.auth.decorators import login_required # built in way of making view only accessible if logged in

from django.contrib import messages # show temporary message to user

# http response forbidden if user tries to change someone else's info
from django.http import HttpResponseForbidden

# Create your views here.

# django will redirect to a signin page if not logged in. need to make that as a route
@login_required # login required for this view. 
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) # creating a model object from form. commit=false - get data but don't save yet
        place.user = request.user
        if form.is_valid(): # validation against DB constraints
            place.save() # save place to DB
            return redirect('place_list') # reload page

    # request object passed to each view function has info on logged in user
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })


@login_required
def place_was_visited(request, place_pk):
    # view decides what we will show user ? a function that gives data and template
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save() 
        else:
            return HttpResponseForbidden

        return redirect('places_visited')


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # does this place belong to the current user?
    if place.user != request.user: 
        return HttpResponseForbidden()

    # is this GET request or POST
    # if POST, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance = place) # new trip review form object from data from http request, data user has sent
        # not shown on page - encapsulates data sent thru form
        # make sure post and files in caps

        if form.is_valid():
            # all required fields filled in, all right types of data
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)  # second argument is shown to user

        return redirect('place_details', place_pk=place_pk)

    # if GET, show place info and form
    else:

        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden


def about(request):
    author = 'Ed'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})