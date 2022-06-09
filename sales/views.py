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
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect, reverse
from .mixins import CarAvailabilityRequiredMixin, NotOwnCarMixin, SuperUserRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class CarListing(ListView):
    """
    Description:
    shows all the car_info records to the page

    # filtering data: gets the distinct values of years and car_makers over all the car_info records
    # filtering: filters the record based on the given choices
    # statistics: gets the number of records and total valuation for both sold and pending car_info records
    # pagination: paginates the records 5 records at a time

    """

    template_name = "sales/car_list.html"
    context_object_name = "listings"

    def get_queryset(self, **kwargs):

        # getting the initial queryset
        if self.request.user.is_superuser:
            car_listing_queryset = CarInfo.objects.all().order_by("-created_at")

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
        # data for filtering
        years = [
            x["year"] for x in CarInfo.objects.order_by().values("year").distinct()
        ]
        car_makers = [
            x["make"] for x in CarInfo.objects.order_by().values("make").distinct()
        ]

        # get pending sales and profit records
        pending_cars_num = CarInfo.objects.filter(status="booked").count()
        pending_commission = (
            CarInfo.objects.filter(status="booked").aggregate(Sum("price"))[
                "price__sum"
            ]
            or 0
        )

        # get finalised sales and profit records
        total_cars_num = CarInfo.objects.filter(status="sold").count()
        total_commission = (
            CarInfo.objects.filter(status="sold").aggregate(Sum("price"))["price__sum"]
            or 0
        )

        context = super().get_context_data(**kwargs)

        context.update(
            {
                "car_makers": car_makers,
                "years": years,
                "pending_commission": pending_commission,
                "pending_cars_num": pending_cars_num,
                "total_commission": total_commission,
                "total_cars_num": total_cars_num,
            }
        )
        return context


class SellCar(LoginRequiredMixin, CreateView):
    """
    Description: shows the form and submits the data for creating a car_info record
    passes the current user to forms save methods to be referenced by the new car_info record
    """

    template_name = "sales/sell.html"
    form_class = SellCarForm

    def get_success_url(self):
        return reverse("sales:home")

    def form_valid(self, form):
        form.save(commit=False, user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class MakeAvailable(SuperUserRequiredMixin, View):
    """
    Description:
    sets the car_info record's status as "available" so that new reuqests can be made on this car_info record
    and the sale_record record as denied
    """

    def dispatch(
        self,
        *args,
        **kwargs,
    ):
        """
        Here, we are using try-except because we need to call the super().dispatch() method so that the
        SuperUserRequiredMixin is executed, but in case the test passes then the value returned makes the
        dispatch method give an error.

        So, if we get an error, then, we come to the normal functionality of this view, else we
        return whatever is returned by the failed SuperUserRequiredMixin.
        """

        try:
            return super().dispatch(self, args, kwargs)
        except:
            CarInfo.objects.filter(id=self.kwargs["pk"]).update(status="available")
            CarSaleRecord.objects.filter(car_listing__id=self.kwargs["pk"]).update(
                denied=True
            )
            return redirect("sales:home")


class FinaliseSale(SuperUserRequiredMixin, View):
    """
    sets the car_info record's status as sold so that no new requests can be made for it and
    the profits can be added to the site for admin.
    """

    def dispatch(
        self,
        *args,
        **kwargs,
    ):
        try:
            return super().dispatch(self, args, kwargs)
        except:
            CarInfo.objects.filter(id=self.kwargs["pk"]).update(status="sold")
            return redirect("sales:home")


class BuyCar(CarAvailabilityRequiredMixin, CreateView):
    """
    Description:
    Used for BuyCar functionality. Takes name and number of interested party, creates a new car_sales_record
    using this data, and then saves the current car_info record's reference on this newly created object.

    Note:
    Not using update() on the car_listing object because we need it on saving the form as well
    so that we can reference it on the new car_sales_record object
    """

    template_name = "sales/buy.html"
    form_class = BuyCarForm

    def get_success_url(self):
        return reverse("sales:home")

    def form_valid(self, form):
        form.save(commit=False, car_listing=CarInfo.objects.get(id=self.kwargs["pk"]))
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "form": BuyCarForm(
                    mobile=self.request.user.mobile, name=self.request.user.username
                ),
                "car_listing": CarInfo.objects.get(id=self.kwargs["pk"]),
            }
        )
        return context
