from django.shortcuts import render
from .forms import SellCarForm
from django.shortcuts import redirect
from sales.models import SellCarListing

# Create your views here.


def car_listings(request):
    qs = SellCarListing.objects.all()

    return render(request, "sales/car_list.html", {"listings":qs})



def sell(request):
    if request.method == "POST":
        form = SellCarForm(request.POST,request.FILES or None)
        if form.is_valid():
            listing = form.save(commit=True)
            print(listing)
            return redirect("sales:home")
        else:
            print("not valid")
            # breakpoint()
    form = SellCarForm()
    return render(request, "sales/sell.html", {"form":form})