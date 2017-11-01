from django.conf.urls import url
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_mileages/(?P<car_id>[0-9]+)$', views.get_mileages),
    url(r'^update_mileages/(?P<car_id>[0-9]+)$', views.update_mileages),
    url(r'^add$', views.input_new_refueling),
]

router = routers.DefaultRouter()
router.register(r'mileages', views.MileagesViewSet)
router.register(r'car', views.CarViewSet)
urlpatterns += router.urls
