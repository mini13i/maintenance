from django.db import models
from datetime import datetime as dt
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

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
        items = Mileages.objects.filter(model__exact=int(car_id)).only("date", "mileage", "amount").order_by('id', 'date')
        item_first = Mileages.objects.filter(model__exact=int(car_id)).only("meter").order_by('id', 'date')[0]
        item_last = Mileages.objects.filter(model__exact=int(car_id)).only("meter").order_by('-id', '-date')[0]
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
        items = Mileages.objects.filter(model__exact=int(car_id)).only("date", "meter", "mileage", "amount").order_by('id','date')
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

    def input_new_refueling(request):
        """給油情報入力画面"""
        cars = Car.objects.all()
        today = dt.now().strftime("%Y年%m月%d日")
        brands = sorted(Mileages.objects.values_list('brand', flat=True).distinct())
        context = {
            'error': "",
            'brand': brands,
            'car': cars,
            'input': {
                'car': "",
                'date': today,
                'meter': "",
                'amount': "",
                'brand': "",
                'price': "",
                'shop': "",
                'comment': "",
            }
        }
        return render(request,
                      "mileage/refueling.html",
                      context)

    def add_refueling(self, request):
        """入力された情報をDBに格納する"""
        error = ""
        item_last = None
        input_date = None
        diff = None
        if int(request.POST.get('car')) <= 0:
            error = "車種を選択してください"
        elif request.POST.get('date') == '':
            error = "日付を選択してください"
        elif request.POST.get('meter') == '':
            error = "ODメーターを入力してください"
        elif request.POST.get('brand') == '':
            error = "ブランドを入力してください"
        elif request.POST.get('amount') == '':
            error = "給油量を入力してください"
        elif request.POST.get('price') == '':
            error = "価格を入力してください"
        if len(error) <= 0:
            item_last = Mileages.objects.filter(model__exact=int(request.POST.get('car'))).only("meter", "date").order_by('-id', '-date')[0]
            input_date = dt.strptime(request.POST.get('date'), "%Y年%m月%d日")
            diff = float(request.POST.get('meter')) - item_last.meter
            if item_last.date > input_date.date():
                error = "日付が前回の給油日より前です"
            if diff <= 0:
                error = "ODメーターが前回の給油時より古いです"
        if len(error) <= 0:
            car = Car.objects.get(pk=int(request.POST.get('car')))
            refueling = Mileages()
            refueling.model = car
            refueling.date = input_date
            refueling.meter = float(request.POST.get('meter'))
            mileage = diff / float(request.POST.get('amount'))
            refueling.mileage = mileage
            refueling.amount = float(request.POST.get('amount'))
            refueling.price = int(request.POST.get('price'))
            refueling.brand = request.POST.get('brand')
            refueling.shop = request.POST.get('shop')
            refueling.comment = request.POST.get('comment')
            #refueling. = 
            refueling.save()
            #return HttpResponseRedirect('/mileage/mileages/%d'%(refueling.id))
            context = {
                'input': {
                    'car': car.model,
                    'date': request.POST.get('date'),
                    'meter': request.POST.get('meter'),
                    'amount': request.POST.get('amount'),
                    'mileage': "%0.2f"%mileage,
                    'price': request.POST.get('price'),
                    'brand': request.POST.get('brand'),
                    'shop': request.POST.get('shop'),
                    'comment': request.POST.get('comment'),
                }
            }
            return render(request,
                          "mileage/result.html",
                          context)
        else:
            cars = Car.objects.all()
            today = dt.now().strftime("%Y年%m月%d日")
            brands = sorted(Mileages.objects.values_list('brand', flat=True).distinct())
            context = {
                'error': error,
                'today': today,
                'brand': brands,
                'car': cars,
                'input': {
                    'car': int(request.POST.get('car')),
                    'date': request.POST.get('date'),
                    'meter': request.POST.get('meter'),
                    'amount': request.POST.get('amount'),
                    'price': request.POST.get('price'),
                    'brand': request.POST.get('brand'),
                    'shop': request.POST.get('shop'),
                    'comment': request.POST.get('comment'),
                }
            }
            return render(request,
                          "mileage/refueling.html",
                          context)
