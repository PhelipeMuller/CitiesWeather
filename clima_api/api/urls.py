
from django.conf.urls import url
from .views import CityListView

urlpatterns = [
    url(r'^cities/?$', CityListView.as_view(), name='cities'),
]
