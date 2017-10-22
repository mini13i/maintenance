# coding: utf-8
from rest_framework import serializers
from .models import Mileages, Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "model",
            "purchase",
        )

class MileagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mileages
        fields = (
            'date',
            'meter',
            'mileage',
            'amount',
            'price',
            'brand',
            'shop',
            'comment',
            'create_at',
            'last_update',
        )
