from django.shortcuts import render
from django.http import HttpResponse
from .models import Mileages

# Create your views here.
def index(request):
    items = Mileages.objects.order_by('date')
    item_last = Mileages.objects.order_by('-date')[0]
    meter_all_diff = item_last.meter - items[0].meter
    amount_all = 0
    for i in range(1,len(items)-1):
        meter_diff = items[i-1].meter - items[i].meter
        mileage = meter_diff / items[i].amount
        amount_all += items[i].amount
    mileage_average = meter_all_diff / amount_all
    strs = "meter:{0}, amount:{1}, mileage:{2}".format(meter_all_diff, amount_all, mileage_average)
    return HttpResponse(strs)
