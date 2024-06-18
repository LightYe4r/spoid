from rest_framework import serializers
from .models import *
class CpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cpu
        fields = '__all__'

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'

class CoolerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooler
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class PowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Power
        fields = '__all__'

class MainBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBoard
        fields = '__all__'

class GpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gpu
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAlarm
        fields = '__all__'

class ComponentAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentAlarm
        fields = '__all__'
