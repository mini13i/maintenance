from django.conf.urls import url
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_mileages$', views.get_mileages),
]

router = routers.DefaultRouter()
router.register(r'mileages', views.MileagesViewSet)
