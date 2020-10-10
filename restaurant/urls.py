from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_reataurant', views.addRestaurant, name='add_restaurant'),
    path('create_owner', views.createOwner, name='createOwner'),
    path('login_owner', views.loginOwner, name='loginOwner'),
    path('restaurant_list', views.listOfRestaurant, name='listOfRestaurant'),
    path('update_restaurant_detail/<int:pk>', views.updateRestaurantDetail, name='updateRestaurantDetail'),
    path('deleteRestaurant/<int:pk>', views.deleteRestaurant, name='deleteRestaurant'),
    path('list_foods_items', views.listFoodsItems, name='listFoodsItems'),
    path('list_Of_Orders', views.listOfOrders, name='listOfOrders'),
    path('generate_invice/<int:pk>', views.generateInvoice, name='generateInvoice'),
    path('logout_owner', views.logoutOwner, name='logoutOwner'),
]