from django.shortcuts import render
from django.http import HttpResponse
from .models import Mileages

# Create your views here.
def index(request):
    items = Mileages.objects.order_by('date')
    item_last = Mileages.objects.order_by('-date')[0]
    meter_diff = item_last.meter - items[0].meter
    amount_all = 0
    for i in range(0,len(items)-1):
        amount_all += items[i].amount
    mileage = meter_diff/amount_all
    strs = "meter:{0}, amount:{1}, mileage:{2}".format(meter_diff, amount_all, mileage)
    return HttpResponse(strs)
