from django.shortcuts import render
from .forms import SellCarForm
from django.shortcuts import redirect
from sales.models import CarInfo

# Create your views here.


def car_listings(request):

    years = [x["year"] for x in CarInfo.objects.order_by().values('year').distinct()]
    car_makers = [x["make"] for x in CarInfo.objects.order_by().values('make').distinct()]

    car_listing_queryset = CarInfo.objects.all()
    if request.method == 'GET':
        listing_filtered_by_year = CarInfo.objects.none()
        listing_filtered_by_make = CarInfo.objects.none()
        flag = 0
        if request.GET["years"] != "":
            flag = 1
            year = request.GET["years"]
            listing_filtered_by_year = car_listing_queryset.filter(year=year)
        if request.GET["car_makers"] != "":
            flag = 1
            maker = request.GET["car_makers"]
            listing_filtered_by_make = car_listing_queryset.filter(make=maker)
        if flag:
            car_listing_queryset = listing_filtered_by_make.union(listing_filtered_by_year)
            
    return render(request, "sales/car_list.html", {"listings":car_listing_queryset, "car_makers":car_makers, "years":years})


def sell(request):

    if request.method == "POST":
        form = SellCarForm(request.POST,request.FILES or None)
        if form.is_valid():
            form.save(commit=False, user = request.user)
            return redirect("sales:home")
    return render(request, "sales/sell.html", {"form":SellCarForm()})