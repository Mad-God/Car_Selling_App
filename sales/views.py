from django.shortcuts import render
from .forms import BuyCarForm, SellCarForm
from django.shortcuts import redirect
from sales.models import CarInfo, CarSaleRecord
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required, car_availability_required, not_own_car
from django.core.paginator import Paginator
from django.db.models import Sum


# Create your views here.


def car_listings(request):
    years = [x["year"] for x in CarInfo.objects.order_by().values('year').distinct()]
    car_makers = [x["make"] for x in CarInfo.objects.order_by().values('make').distinct()]
    car_listing_queryset = CarInfo.objects.all().order_by("-created_at")


    if request.method == 'GET':
        car_listing_queryset = car_listing_queryset.filter(make__icontains = request.GET.get('car_makers', ""))
    
        year = request.GET.get('years', "")
        if year != "":
            car_listing_queryset = car_listing_queryset.filter(year = year)
    

    # get pending sales and profit records
    pending_cars = CarSaleRecord.objects.filter(car_listing__sold=True, finalised=False)
    pending_cars_num = pending_cars.count()
    pending_commission = pending_cars.aggregate(Sum("car_listing__price"))['car_listing__price__sum'] or 0


    # get finalised sales and profit records
    sold_cars = CarSaleRecord.objects.filter(finalised=True)
    total_cars_num = sold_cars.count() or 0
    total_commission = sold_cars.aggregate(Sum("car_listing__price"))['car_listing__price__sum'] or 0



    # pagination
    p = Paginator(car_listing_queryset, 5)
    page = request.GET.get("page")
    qs = p.get_page(page)


    context = {"listings":qs, "car_makers":car_makers,
     "years":years, "pending_commission":pending_commission, 
     "pending_cars_num":pending_cars_num, "total_commission":total_commission, 
     "total_cars_num":total_cars_num}


    return render(request, "sales/car_list.html", 
    context
    )


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
@not_own_car
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
    sale_record = car_listing.purchase.first()
    sale_record.delete()
    return redirect("sales:home")


@login_required
@superuser_required
def finalise_sale(request, pk):
    car_listing = CarInfo.objects.get(id=pk)
    sale_record = car_listing.purchase.first()
    sale_record.finalised = True
    sale_record.save()
    return redirect("sales:home")


