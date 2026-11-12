from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
    path('<int:id>/update/', views.update_quantity, name='cart.update'),
    path('<int:id>/remove/', views.remove_quantity, name='cart.remove'),
]