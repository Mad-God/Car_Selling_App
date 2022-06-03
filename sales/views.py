from django.shortcuts import render
from .forms import BuyCarForm, SellCarForm
from django.shortcuts import redirect
from sales.models import CarInfo
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required, car_availability_required
# Create your views here.


def car_listings(request):
    years = [x["year"] for x in CarInfo.objects.order_by().values('year').distinct()]
    car_makers = [x["make"] for x in CarInfo.objects.order_by().values('make').distinct()]
    car_listing_queryset = CarInfo.objects.all()

    if request.method == 'GET':
        car_listing_queryset = car_listing_queryset.filter(make__icontains = request.GET.get('car_makers', ""))
    
        year = request.GET.get('years', "")
        if year != "":
            car_listing_queryset = car_listing_queryset.filter(year = year)
        
    return render(request, "sales/car_list.html", {"listings":car_listing_queryset, "car_makers":car_makers, "years":years})


@login_required
def sell_car(request):
    if request.method == "POST":
        form = SellCarForm(request.POST,request.FILES or None)
        if form.is_valid():
            form.save(commit=False, user = request.user)
            return redirect("sales:home")
    return render(request, "sales/sell.html", {"form":SellCarForm()})

@login_required
@car_availability_required
def buy_car(request, pk):
    car_listing = CarInfo.objects.get(id=pk)
    if request.method == "POST":
        form = BuyCarForm(request.POST)
        if form.is_valid():
            form.save(commit=False, car_listing=car_listing)
            # ssend mail here
            return redirect("sales:home")
    return render(request, "sales/buy.html", {"form":BuyCarForm(mobile=request.user.mobile, name=request.user.username), "car_listing":car_listing})


@login_required
@superuser_required
def make_available(request, pk):
    car_listing = CarInfo.objects.get(id=pk)
    car_listing.sold=False
    car_listing.save()
    return redirect("sales:home")