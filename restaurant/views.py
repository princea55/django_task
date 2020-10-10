from django.shortcuts import render, redirect
from django.http import FileResponse
from .forms import AddRestaurant, CreateOwner, LoginUser
from .models import Restaurant, FoodItems, Orders
from django.contrib.auth.models import User
from django.contrib import messages, auth
import io
from reportlab.pdfgen import canvas
from django.db.models import Count, Sum
from django.db import models
from django.db.models import Func
from django.http import JsonResponse
class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


def dashboard(request):
    max_dishes_food_id = Orders.objects.values('FoodItemId').annotate(total=Count('id')).order_by('-total')[0]
    popularFood = FoodItems.objects.get(id = max_dishes_food_id['FoodItemId'])
    totalOrders = Orders.objects.aggregate(total=Count('id'))
    popularity = (max_dishes_food_id['total']*100)//totalOrders['total']
    sales = Orders.objects.annotate(m=Month('orderDate')).values('m').annotate(total=Sum('totalBill')).order_by()
    Dailysales = Orders.objects.values('orderDate').annotate(total=Sum('totalBill'))
    
    labels = []
    data = []
    for entry in sales:
        labels.append(entry['m'])
        data.append(entry['total'])
    context = {
        'foodName':popularFood.foodName,
        'popularity':popularity,
        'labels': labels,
        'data': data,
        'orderDate':Dailysales[0]['orderDate'],
        'TotalDaysales':Dailysales[0]['total']
        
    }
    return render(request, 'dashboard/home.html', context)

def createOwner(request):
    if request.method == 'POST':
        forms = CreateOwner(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            email = forms.cleaned_data['email']
            password = forms.cleaned_data['password1']
            password2 = forms.cleaned_data['password2']
            
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'That username already taken.')
                    return redirect('createOwner')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email already registered.')
                        return redirect('createOwner')
                    else:
                        user = User.objects.create_user(username=username, password=password, email=email)
                        user.save()
                        auth.login(request, user)
                        messages.success(request, 'Now You can check out restaurant')
                        return redirect('dashboard')
            else:
                messages.error(request, 'Both password should be match')
                return redirect('createOwner')
    else:
        forms = CreateOwner()
        return render(request, 'dashboard/createOwner.html', {'forms':forms})
    return render(request, 'dashboard/createOwner.html', {'forms':forms})

def loginOwner(request):
    if request.method == "POST":
        forms = LoginUser(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                context = {
                    "user": user,
                }
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            
            return render(request, 'dashboard/loginOwner.html', {"forms": forms})

    else:
        forms = LoginUser()
        return render(request, 'dashboard/loginOwner.html', {"forms": forms})
    return render(request, 'dashboard/loginOwner.html', {"forms": forms})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out')
        return redirect('dashboard')

def addRestaurant(request):
    if request.method == "POST":
        forms = AddRestaurant(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            city = forms.cleaned_data['city']
            address = forms.cleaned_data['address']
            franchise_name = forms.cleaned_data['franchise_name']
            createRestaurant = Restaurant(ownerId=request.user, name=name, city=city, address=address, franchise_name=franchise_name)
            createRestaurant.save()
            messages.success(request, 'New restaurant created!')
            return redirect('dashboard')
            
    else:
        forms = AddRestaurant()
        return render(request, 'addRestaurant.html', {'forms':forms})
    return render(request, 'addRestaurant.html', {'form':forms})

def listOfRestaurant(request):
    if request.method == "GET":
        restaurant = Restaurant.objects.order_by('name')
        context = {
            'restaurants' : restaurant
        }
        return render(request, 'dashboard/listOfRestaurant.html', context)

def updateRestaurantDetail(request, pk):
    if request.method == "POST":
        restaurantDetail = Restaurant.objects.get(id=pk)
        forms = AddRestaurant(request.POST, instance=restaurantDetail)
        if forms.is_valid():
            forms.save()
            # createRestaurant.save()
            messages.success(request, 'Detail successfully updated!')
            return redirect('dashboard')
    else:
        restaurantDetail = Restaurant.objects.get(id=pk)
        forms = AddRestaurant(instance=restaurantDetail)
        return render(request, 'dashboard/updateRestaurant.html', {'forms':forms})
    return render(request, 'dashboard/updateRestaurant.html', {'form':forms})

def deleteRestaurant(request, pk):
    restaurantDetail = Restaurant.objects.get(id=pk)
    restaurantDetail.delete()
    messages.success(request, 'Data delete successfully!')
    return redirect('dashboard')
                

def listFoodsItems(request):
    if request.method == "GET":
        foods = FoodItems.objects.order_by('foodName')
        context = {
            'fooditems':foods
        }
        return render(request, 'dashboard/listOfFoods.html', context)

def listOfOrders(request):
    if request.method == "GET":

        orders = Orders.objects.all()
        context = {
            'orders':orders
        }
        return render(request, 'dashboard/restaurantOrders.html', context)

def generateInvoice(request, pk):
    foodDetail = Orders.objects.get(id=pk)

    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    pdf.drawString(250, 650, "Your order invoice")

    pdf.drawString(50, 600, "Food Name :")
    pdf.drawString(130, 600, foodDetail.FoodItemId.foodName)

    pdf.drawString(50, 570, "Food Type :")
    pdf.drawString(130, 570, foodDetail.FoodItemId.foodType)

    pdf.drawString(50, 550, "Restaurant name :")
    pdf.drawString(160, 550, foodDetail.restaurantId.name)

    pdf.drawString(50, 520, "Food Price :")
    pdf.drawString(130, 520, foodDetail.FoodItemId.price)

    pdf.drawString(50, 490, "Table NO. :")
    pdf.drawString(130, 490, str(foodDetail.tableNo))

    pdf.drawString(50, 460, "Order Date :")
    pdf.drawString(130, 460, str(foodDetail.orderDate))

    pdf.drawString(50, 430, "Order Time :")
    pdf.drawString(130, 430, str(foodDetail.time))

    pdf.drawString(50, 400, "Total NO of items :")
    pdf.drawString(160, 400, str(foodDetail.noOdItems))

    pdf.drawString(50, 370, "Total Bill :")
    pdf.drawString(130, 370, str(foodDetail.totalBill))

    pdf.showPage()
    pdf.save()
    data.seek(0)
    return FileResponse(data, as_attachment=True, filename='invoice.pdf')


def logoutOwner(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('loginOwner')