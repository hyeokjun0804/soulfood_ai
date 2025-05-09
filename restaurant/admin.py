from django.contrib import admin
from restaurant.models import Category, Province, City, District, Town, Village, Restaurant
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
    list_filter = ['name']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
    list_filter = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        'restaurant_name', 'latitude', 'longitude', 'jibun_address', 'phone_number',
        'weekday_hours', 'weekend_hours', 'free_parking', 'baby_chair', 'pet_friendly',
        'restaurant_image', 'category', 'province', 'city', 'district', 'town', 'village'
    ]
    search_fields = ['restaurant_name']
    list_filter = ['restaurant_name']
