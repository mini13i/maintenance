from datetime import datetime as dt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import viewsets
from .models import Mileages, Car
from .serializer import MileagesSerializer, CarSerializer
from django.contrib.auth.decorators import login_required

# 
def index(request):
    cars = Car.objects.all()
    context = {'car':cars}
    return render(request, 'mileage/index.html', context)

def get_mileages(request, car_id):
    return Mileages.get_mileages(request, car_id)

@login_required(login_url="/login/")
def update_mileages(request, car_id):
    return Mileages.update_mileages(request, car_id)

@login_required(login_url="/login/")
def input_new_refueling(request):
    return Mileages.input_new_refueling(request)

@login_required(login_url="/login/")
def add_refueling(request):
    m = Mileages()
    return m.add_refueling(request)

# 給油情報をリストで出力
def get_list(request, car_id):
    items = Mileages.objects.filter(model__exact=int(car_id)).order_by('date')
    item_last = Mileages.objects.filter(model__exact=int(car_id)).order_by('-date')[0]
    meter_all_diff = item_last.meter - items[0].meter
    amount_all = 0
    mileages = []
    diff = []
    dates = []
    amount = []
    for i in range(1,len(items)-1):
        dates.append(items[i].date)
        meter_diff = items[i].meter - items[i-1].meter
        diff.append(meter_diff)
        amount.append(items[i].amount)
        mileage.append(meter_diff / items[i].amount)
        amount_all += items[i].amount
    mileage_average = meter_all_diff / amount_all
    strs = "meter:{0}, amount:{1}, mileage:{2}".format(meter_all_diff, amount_all, mileage_average)
    context = {
        'dates' : dates,
        'mileage' : mileage,
        'diff' : diff,
        'amount' : amount,
    }
    return JsonResponse(context)

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class MileagesViewSet(viewsets.ModelViewSet):
    queryset = Mileages.objects.all()
    serializer_class = MileagesSerializer
