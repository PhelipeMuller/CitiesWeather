
from django.conf.urls import url
from .views import CityListView, CityView

urlpatterns = [
    url(r'^cities/?$', CityListView.as_view(), name='cities'),
    url(r'^city/(?P<name>\w{0,30})/?$', CityView.as_view(), name='city'),
]
