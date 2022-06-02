from django.shortcuts import render
from .forms import SellCarForm
from django.shortcuts import redirect
from sales.models import CarInfo

# Create your views here.


def car_listings(request):
    # if request.method = GET:

    years = CarInfo.objects.order_by().values('years').distinct()
    makes = CarInfo.objects.order_by().values('make').distinct()
    breakpoint()
    return render(request, "sales/car_list.html", {"listings":CarInfo.objects.all(), "makes":makes, "years":years})


def sell(request):

    if request.method == "POST":
        form = SellCarForm(request.POST,request.FILES or None)
        if form.is_valid():
            form.save(commit=False, user = request.user)
            return redirect("sales:home")
    return render(request, "sales/sell.html", {"form":SellCarForm()})