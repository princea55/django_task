from django.contrib import admin

# Register your models here.
from .models import Restaurant, Orders, FoodItems

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id','ownerId', 'name', 'city','franchise_name')
    list_display_links = ('id', 'name')
    list_filter = ('city', 'franchise_name')
    search_fields = ('name',)
    list_per_page = 25

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id','FoodItemId','restaurantId', 'totalBill', 'noOdItems', 'orderDate','time', 'tableNo')
    list_display_links = ('id',)
    list_filter = ('tableNo','orderDate')
    search_fields = ('orderDate',)
    list_per_page = 50

class FooItemsAdmin(admin.ModelAdmin):
    list_display = ('id','restaurantId', 'foodName', 'price','foodType', 'noOfVariety')
    list_display_links = ('id',)
    list_filter = ('foodType',)
    search_fields = ('foodName',)
    list_per_page = 25

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(FoodItems, FooItemsAdmin)