from django.shortcuts import render
from .forms import SellCarForm
from django.shortcuts import redirect
from sales.models import CarInfo

# Create your views here.


def car_listings(request):
    return render(request, "sales/car_list2.html", {"listings":CarInfo.objects.all()})



def sell(request):
    if request.method == "POST":
        form = SellCarForm(request.POST,request.FILES or None)
        if form.is_valid():
            form.save(commit=False, user = request.user)
            return redirect("sales:home")
    return render(request, "sales/sell.html", {"form":SellCarForm()})