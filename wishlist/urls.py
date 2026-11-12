from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='wishlist.index'),
    path('<int:id>/toggle/', views.toggle, name='wishlist.toggle'),
    path('clear/', views.clear, name='wishlist.clear'),
]