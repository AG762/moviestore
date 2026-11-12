from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    
    '''
    movies and sort them just based on some inputs    
    '''
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    sort = request.GET.get('sort', 'low')
    
    # basic checks
    if min_price.isdigit():
        # keeping anything that is greater or equal to min price
        movies = movies.filter(price__gte=int(min_price))
    if max_price.isdigit():
        # keeping anything that is lower or equal to max price
        movies = movies.filter(price__lte=int(max_price))
    if sort == 'high':
        # hey, reverse this
        movies = movies.order_by('-price', 'id')
    else:
        # normal one
        movies = movies.order_by('price', 'id')
    
        
    
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def compare(request, action=None, id=None):
    ids = request.session.get('compare', [])
    data = {'title': 'Compare Movies'}
    if action == 'add' and id not in ids:
        if len(ids) < 3:
            ids.append(id)
        else:
            data['error'] = 'you cant compare more than 3 movies'
    if action == 'remove':
        ids = []
        for i in ids: 
            if i != id:
                ids.append(i)
    # get list of movie objects with the matching id
    movies = Movie.objects.filter(id__in=ids)
    ms = []
    for m in movies: 
        ms.append(m.id)
    request.session['compare'] = ms
    data['movies'] = movies
    return render(request, 'movies/compare.html', {'template_data':data})
@login_required
@require_POST
def toggle_helpful(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, movie_id=id)
    if review.user_id == request.user.id:
        return redirect("movies.show", id=id)
    if review.helpful_users.filter(id=request.user.id).exists():
        review.helpful_users.remove(request.user)
    else:
        review.helpful_users.add(request.user)
    return redirect("movies.show", id=id)