from django.db import models

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
