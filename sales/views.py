from django.shortcuts import render
from .forms import BuyCarForm, SellCarForm
from django.shortcuts import redirect
from sales.models import CarInfo, CarSaleRecord
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required, car_availability_required, not_own_car
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import redirect, reverse
from .mixins import SuperUserRequired
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
# Create your views here.


def car_listings(request):
    """
    Description:
    shows all the car_info records to the page

    # filtering data: gets the distinct values of years and car_makers over all the car_info records
    # filtering: filters the record based on the given choices
    # statistics: gets the number of records and total valuation for both sold and pending car_info records
    # pagination: paginates the records 5 records at a time

    """

    # filtering data
    years = [x["year"] for x in CarInfo.objects.order_by().values("year").distinct()]
    car_makers = [
        x["make"] for x in CarInfo.objects.order_by().values("make").distinct()
    ]


    

    # for getting the sold cars for admin view
    if request.user.is_superuser:
        car_listing_queryset = CarInfo.objects.all()
    else:
        car_listing_queryset = CarInfo.objects.exclude(status="sold").order_by(
            "-created_at"
        )

    # filtering
    if request.method == "GET":
        car_listing_queryset = car_listing_queryset.filter(
            make__icontains=request.GET.get("car_makers", "")
        )

        year = request.GET.get("years", "")
        if year != "":
            car_listing_queryset = car_listing_queryset.filter(year=year)

    # get pending sales and profit records
    pending_cars_num = CarInfo.objects.filter(status="booked").count()
    pending_commission = (
        CarInfo.objects.filter(status="booked").aggregate(Sum("price"))["price__sum"]
        or 0
    )

    # get finalised sales and profit records
    total_cars_num = CarInfo.objects.filter(status="sold").count()
    total_commission = (
        CarInfo.objects.filter(status="sold").aggregate(Sum("price"))["price__sum"] or 0
    )


    # pagination
    p = Paginator(car_listing_queryset, 5)
    page = request.GET.get("page")
    paginated_car_listing_queryset = p.get_page(page)

    context = {
        "listings": paginated_car_listing_queryset,
        "car_makers": car_makers,
        "years": years,
        "pending_commission": pending_commission,
        "pending_cars_num": pending_cars_num,
        "total_commission": total_commission,
        "total_cars_num": total_cars_num,
    }

    # breakpoint()
    return render(request, "sales/car_list.html", context)

class CarListing(ListView):
    template_name = 'sales/car_list.html'
    context_object_name = "listings"

    def get_queryset(self, **kwargs):

        # getting the initial queryset
        if self.request.user.is_superuser:
            car_listing_queryset = CarInfo.objects.all()
        else:
            car_listing_queryset = CarInfo.objects.exclude(status="sold").order_by(
                "-created_at"
            )


        # filtering
        if self.request.method == "GET":
            car_listing_queryset = car_listing_queryset.filter(
                make__icontains=self.request.GET.get("car_makers", "")
            )

            year = self.request.GET.get("years", "")
            if year != "":
                car_listing_queryset = car_listing_queryset.filter(year=year)

        # pagination
        paginator = Paginator(car_listing_queryset, 10)


        return paginator.get_page(self.request.GET.get("page"))

    def get_context_data(self, **kwargs):
        # filtering data

        
        years = [x["year"] for x in CarInfo.objects.order_by().values("year").distinct()]
        car_makers = [
            x["make"] for x in CarInfo.objects.order_by().values("make").distinct()
        ]

        # get pending sales and profit records
        pending_cars_num = CarInfo.objects.filter(status="booked").count()
        pending_commission = (
            CarInfo.objects.filter(status="booked").aggregate(Sum("price"))["price__sum"]
            or 0
        )

        # get finalised sales and profit records
        total_cars_num = CarInfo.objects.filter(status="sold").count()
        total_commission = (
            CarInfo.objects.filter(status="sold").aggregate(Sum("price"))["price__sum"] or 0
        )
        
        context = super().get_context_data(**kwargs)
        
        context.update({
            "car_makers": car_makers,
            "years": years,
            "pending_commission": pending_commission,
            "pending_cars_num": pending_cars_num,
            "total_commission": total_commission,
            "total_cars_num": total_cars_num,
        })
        return context
          




@login_required
def sell_car(request):
    """
    Description: shows the form and submits the data for creating a car_info record
    passes the current user to forms save methods to be referenced by the new car_info record
    """
    if request.method == "POST":
        form = SellCarForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save(commit=False, user=request.user)
            return redirect("sales:home")
    return render(request, "sales/sell.html", {"form": SellCarForm()})

class SellCar(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    template_name = 'sales/sell.html'
    form_class = SellCarForm
    def get_success_url(self):
        return reverse('sales:home')
    
    def form_valid(self, form):
        form.save(commit=False, user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())






@login_required
@superuser_required
def make_available(request, pk):
    """
    Description:
    sets the car_info record's status as "available" so that new reuqests can be made on this car_info record
    and the sale_record record as denied
    """
    CarInfo.objects.filter(id=pk).update(status="available")
    CarSaleRecord.objects.filter(car_listing__id=pk).update(denied=True)
    return redirect("sales:home")

class MakeAvailable(View):
    def dispatch(self, *args, **kwargs,):
        """
        Description:
        sets the car_info record's status as "available" so that new reuqests can be made on this car_info record
        and the sale_record record as denied
        """
        breakpoint()
        CarInfo.objects.filter(id=self.kwargs["pk"]).update(status="available")
        CarSaleRecord.objects.filter(car_listing__id=self.kwargs["pk"]).update(denied=True)
        return redirect("sales:home")

    def test_func(self):
        breakpoint()
        return self.request.user.is_superuser

    def handle_no_permission(self):
        breakpoint()
        return HttpResponse("You are not a super user. Please login as one to make cars available")







@login_required
@superuser_required
def finalise_sale(request, pk):
    """
    sets the car_info record's status as sold so that no new requests can be made for it and
     the profits can be added to the site for admin
    """
    CarInfo.objects.filter(id=pk).update(status="sold")
    return redirect("sales:home")

class FinaliseSale(View):
    def dispatch(self, *args, **kwargs,):
        """
        sets the car_info record's status as sold so that no new requests can be made for it and
        the profits can be added to the site for admin
        """
        CarInfo.objects.filter(id=self.kwargs["pk"]).update(status="sold")
        print("in the dispatch method")
        return redirect("sales:home")






@login_required
@car_availability_required
@not_own_car
def buy_car(request, pk):
    """
    Description:
    Used for BuyCar functionality. Takes name and number of interested party, creates a new car_sales_record
    using this data, and then saves the current car_info record's reference on this newly created object.

    Note:
     Not using update() on the car_listing object because we need it on saving the form as well
     so that we can reference it on the new car_sales_record object
    """
    car_listing = CarInfo.objects.get(id=pk)
    if request.method == "POST":
        form = BuyCarForm(request.POST)
        if form.is_valid():
            form.save(commit=False, car_listing=car_listing)
            return redirect("sales:home")
    return render(
        request,
        "sales/buy.html",
        {
            "form": BuyCarForm(mobile=request.user.mobile, name=request.user.username),
            "car_listing": car_listing,
        },
    )

class BuyCar(UpdateView):
    """
        Description:
        Used for BuyCar functionality. Takes name and number of interested party, creates a new car_sales_record
        using this data, and then saves the current car_info record's reference on this newly created object.

        Note:
        Not using update() on the car_listing object because we need it on saving the form as well
        so that we can reference it on the new car_sales_record object
    """
    template_name = 'sales/buy.html'
    form_class = BuyCarForm

    def get_success_url(self):
        return reverse('sales:home')

    def get_queryset(self):
        queryset =CarInfo.objects.filter(id=self.kwargs['pk'])
        return queryset
    
    def form_valid(self, form):
        form.save(commit=False, car_listing=CarInfo.objects.get(id=self.kwargs['pk']))
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "form": BuyCarForm(mobile=self.request.user.mobile, name=self.request.user.username),
            "car_listing": CarInfo.objects.get(id=self.kwargs["pk"]),
        })
        return context


