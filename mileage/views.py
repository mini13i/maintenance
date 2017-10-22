from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.template import loader
from rest_framework import viewsets, filters
from .models import Mileages, Car
from .serializer import MileagesSerializer, CarSerializer
from datetime import datetime as dt
from datetime import date
import django_filters

# Create your views here.
def index(request):
    cars = Car.objects.all()
    context = {'car':cars}
    return render(request, 'mileage/index.html', context)

# Create your views here.
def get_list(request, car_id):
    items = Mileages.objects.filter(model__exact=car_id).order_by('date')
    item_last = Mileages.objects.filter(model__exact=car_id).order_by('-date')[0]
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
        'result': strs,
        'dates' : dates,
        'mileage' : mileage,
        'diff' : diff,
        'amount' : amount,
    }
    return JsonResponse(context)


def get_mileages(request, car_id):
    print("%s"%car_id)
    items = Mileages.objects.filter(model__exact=int(car_id)).only("date", "meter", "mileage", "amount").order_by('date')
    print(items)
    item_last = Mileages.objects.filter(model__exact=int(car_id)).only("date", "meter").order_by('-date')[0]
    current_year = int(dt.now().strftime("%Y"))
    meter_all_diff = item_last.meter - items[0].meter
    amount_all = 0
    mileages = []
    dates = []
    years = []
    mileages_year = []
    dates_year = []
    last_year = int(items[0].date.strftime("%Y"))
    print("%d"%last_year)
    for i in range(1,len(items)-1):
        date_strs = items[i].date.strftime("%Y/%m/%d").split("/")
        if int(date_strs[0]) > last_year:
            if len(mileages_year) > 0:
                years.append(date_strs[0])
                mileages.append(mileages_year)
                dates.append(dates_year)
            last_year = int(date_strs[0])
            mileages_year = []
            dates_year = []
        date_strs[0] = str(current_year)
        items[i].date = "-".join(date_strs) + " 00:00:00"
        #x = float(date_str[1]) + float(date_str[2])/31.0)
        dates_year.append(items[i].date)
        meter_diff = items[i].meter - items[i-1].meter
        mileages_year.append(meter_diff / items[i].amount)
        amount_all += items[i].amount
    if len(mileages_year) > 0:
        years.append(date_strs[0])
        mileages.append(mileages_year)
        dates.append(dates_year)
    mileage_average = meter_all_diff / amount_all
    context = {
        'dates' : dates,
        'mileages' : mileages,
        'average' : mileage_average,
        'years' : years,
    }
    return JsonResponse(context)

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class MileagesViewSet(viewsets.ModelViewSet):
    queryset = Mileages.objects.all()
    serializer_class = MileagesSerializer
