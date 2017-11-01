from django.db import models
from datetime import datetime as dt
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

class Car(models.Model):
    model = models.CharField(max_length=100)
    purchase = models.DateField()

    def __str__(self):
        return self.model

# Create your models here.
class Mileages(models.Model):
    model = models.ForeignKey(Car)
    date = models.DateField()
    meter = models.FloatField()
    mileage = models.FloatField(default=0)
    amount = models.FloatField()
    price = models.PositiveSmallIntegerField()
    brand = models.CharField(max_length=100)
    shop = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['mileage']),
            models.Index(fields=['shop']),
        ]

    def __str__(self):
        return "{0} {1}".format(self.date.strftime("%Y/%m/%d"), self.meter)
        
    list_display = (date, meter)

    def get_mileages(request, car_id):
        """
        燃費をJSON形式で渡す
        """
        items = Mileages.objects.filter(model__exact=int(car_id)).only("date", "mileage", "amount").order_by('date')
        item_first = Mileages.objects.filter(model__exact=int(car_id)).only("meter").order_by('date')[0]
        item_last = Mileages.objects.filter(model__exact=int(car_id)).only("meter").order_by('-date')[0]
        current_year = int(dt.now().strftime("%Y"))
        meter_all_diff = item_last.meter - item_first.meter # 総走行距離
        amount_all = 0 # 総給油量
        mileages = []  # 各年の燃費
        dates = []     # 各年の給油日
        years = []     # 各年の年
        mileages_year = [] # その年の燃費
        dates_year = []    # その年の給油日
        last_year = int(items[0].date.strftime("%Y"))
        for i in range(1,len(items)):
            date_strs = items[i].date.strftime("%Y/%m/%d").split("/")
            # 年が変わったら過去1年分をリストに加える
            if int(date_strs[0]) > last_year:
                if len(mileages_year) > 0:
                    years.append(str(last_year))
                    mileages.append(mileages_year)
                    dates.append(dates_year)
                last_year = int(date_strs[0])
                mileages_year = []
                dates_year = []
            # 同じ年で揃える
            date_strs[0] = str(current_year)
            items[i].date = "-".join(date_strs) + " 00:00:00"
            dates_year.append(items[i].date)
            mileages_year.append(items[i].mileage)
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
            'current' : str(current_year),
        }
        return JsonResponse(context)

#    @method_decorator(login_required)
    def update_mileages(request, car_id):
        items = Mileages.objects.filter(model__exact=int(car_id)).only("date", "meter", "mileage", "amount").order_by('date')
        for i in range(1,len(items)):
            #print(items[i].date)
            meter_diff = items[i].meter - items[i-1].meter
            update_item = Mileages.objects.get(pk=items[i].id)
            update_item.mileage = meter_diff / items[i].amount
            update_item.save()
        context = {
            'Done' : True,
        }
        return JsonResponse(context)
