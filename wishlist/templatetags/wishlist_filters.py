from django import template
register = template.Library()
@register.filter(name='get_quantity')
def get_wishlist_quantity(wishlist, movie_id):
    return wishlist[str(movie_id)]