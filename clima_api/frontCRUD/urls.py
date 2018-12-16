
from django.urls import path
from .views import list_cities, search_city, update_city, delete_city

urlpatterns = [
    path('', list_cities, name='List_of_Cities'),
    path('new', search_city, name='Search_City'),
    path('update/<int:id>', update_city, name='Update_City'),
    path('delete/<int:id>', delete_city, name='Delete_City')
]
