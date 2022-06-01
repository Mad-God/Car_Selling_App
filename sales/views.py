from django.shortcuts import render
from .forms import SellCarForm
from django.shortcuts import redirect
from sales.models import SellCarListing

# Create your views here.


def car_listings(request):
    qs = SellCarListing.objects.all()

    return render(request, "sales/car_list.html", {"listings":qs})



def sell(request):
    errors = ""
    if request.method == "POST":
        form = SellCarForm(request.POST,request.FILES or None)
        if form.is_valid():
            listing = form.save(commit=True)
            print(listing)
            return redirect("sales:home")
        else:
            errors_dict = form.errors
            # breakpoint()
            for i,error in errors_dict.items():
                errors += '"' + str(i) + '"'
                errors = errors + " " +error[0]

            print("not valid")
            # breakpoint()
    form = SellCarForm()    
    context = {"form":form}
    if errors != "":
        context["errors"] = errors
    return render(request, "sales/sell.html", context)