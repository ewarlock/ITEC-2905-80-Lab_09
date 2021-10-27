from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewPlaceForm
from .models import Place

# Create your views here.
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)
        place = form.save() # creating a model object from form
        if form.is_valid(): # validation against DB constraints
            place.save() # save place to DB
            return redirect('place_list') # reload page

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })


def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()

        return redirect('places_visited')

def about(request):
    author = 'Ed'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})