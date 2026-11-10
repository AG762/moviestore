from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie

#ensure no duplicates later
#should it be a toggle or separate delete from wishlist button
def index(request):
    movies_in_wishlist = []
    wishlist = request.session.get('wishlist', [])
    #movie_ids = request.s
    #movie_ids = list(wishlist.keys())
    if (wishlist != []):
        movies_in_wishlist = Movie.objects.filter(id__in=wishlist)
    template_data = {}
    template_data['title'] = 'Wishlist'
    template_data['movies_in_wishlist'] = movies_in_wishlist
    return render(request, 'wishlist/index.html',
        {'template_data': template_data})

def clear(request):
    request.session['wishlist'] = []
    return redirect('wishlist.index')
#might delete later


def toggle(request, id):
    get_object_or_404(Movie, id=id)
    wishlist = request.session.get('wishlist', [])
    temp = []
    if isinstance(wishlist, dict) :
        temp = [(m) for m in wishlist.keys()]
        wishlist = temp
    if id in wishlist:
        wishlist.remove(id)
    else:
        wishlist.append(id)
    request.session['wishlist'] = wishlist
    return redirect('wishlist.index')