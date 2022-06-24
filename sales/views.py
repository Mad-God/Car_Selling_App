from django.shortcuts import render
from .forms import BuyCarForm, SellCarForm
from django.shortcuts import redirect
from sales.models import CarInfo, CarSaleRecord
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required, car_availability_required, not_own_car
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect, reverse
from .mixins import CarAvailabilityRequiredMixin, NotOwnCarMixin, SuperUserRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import test_func, test_func2, test_func3
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from rest_framework.authentication import TokenAuthentication

# -------- DRF imports ---------------
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from sales.serializers import CarInfoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import CarInfo
from .serializers import CarInfoSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from sales.permissions import IsOwnerOrReadOnly

from sales import mixins
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



class BuyCar(CarAvailabilityRequiredMixin, NotOwnCarMixin, CreateView):
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


def celery_view(request):
    # normal apllication of the task
    # test_func2.delay(2,3)

    # linked application
    # x = test_func2.apply_async(kwargs={'a':3, 'b':4}, link=test_func2.si(1,2))

    # subtasked tasks
    x = test_func3.delay(a=1,b=3)
    # breakpoint()
    print(x.get())

    return HttpResponse("Done in the view. Check celery terminal. News.")

@superuser_required
def timed_mail(request):
    if request.method == "GET":
        hour = request.GET.get("hour", -1)
        minute = request.GET.get("minute", -1)
        flag=0
        # breakpoint()
        if flag==1:
            return HttpResponse("mail has been scheduled")
        
        if hour != -1 and minute != -1:
            schedule, created = CrontabSchedule.objects.get_or_create(hour =hour, minute=minute)
            # use unique name for the periodic tasks
            task = PeriodicTask.objects.create(crontab=schedule, name=f"timed_mail_{hour}_{minute}", task="sales.tasks.schedule_mails", args=json.dumps((request.GET.get("subject", "No Subject"), request.GET.get("content", "No Content"))))
            return HttpResponse("mail has been scheduled")
        # else:
        #     return HttpResponse("INvalid form values")
    return render(request,"sales/timed-mail.html", context={})



# ----------------- DRF VIEWS -----------

# --------- Serializer dummy views -----------

@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes((permissions.AllowAny,))
def car_info_list(request):
    """
    List all car listings, or create a new listing.
    """
    if request.method == 'GET':
        snippets = CarInfo.objects.all()
        serializer = CarInfoSerializer(snippets, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

    elif request.method == 'POST':
        breakpoint()
        data = JSONParser().parse(request)
        serializer = CarInfoSerializer(data=data)
        if serializer.is_valid():
            breakpoint()
            serializer.save()
            # return JsonResponse(serializer.data, status=201)
            return Response(serializer.data, status=201)
            # return JsonResponse(serializer.errors, status=400)
        breakpoint()
        return Response(serializer.errors, status=400)



@csrf_exempt
@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes((permissions.AllowAny,))
def car_info_detail(request, pk):

    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = CarInfo.objects.get(pk=pk)
    except CarInfo.DoesNotExist:
        return HttpResponse("asdadsads  ")

    if request.method == 'GET':
        serializer = CarInfoSerializer(snippet)
        return Response(serializer.data)
        # return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CarInfoSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            print("came here\n\n")
            # return Response(serializer.data)
            # breakpoint()
            # return redirect("sales:api-detail",pk=serializer._args[0].id)
            return redirect("sales:api-detail",pk=snippet.id)
            # return JsonResponse(serializer.data)
        return Response(serializer.errors, status=400)
        # return JsonResponse(serializer.errors, status=400)
    elif request.method == 'POST':
        print("in PSOT")
        breakpoint()
        data = JSONParser().parse(request)
        serializer = CarInfoSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            # return JsonResponse(serializer.data)
        return Response(serializer.errors, status=400)
        # return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':

        snippet.delete()
        return HttpResponse(status=204)




# ------------- CLASS BASED API VIEWS ------------------


class CarInfoList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    # permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CarInfoSerializer
    queryset = CarInfo.objects.all()

    # def get(self,*args, **kwargs):
    #     breakpoint()
    #     return super.get(self, args, kwargs)
    # def get(self, request, format=None):
    #     carinfo = CarInfo.objects.all()
    #     serializer = CarInfoSerializer(carinfo, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = CarInfoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CarInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsOwnerOrReadOnly]
    queryset = CarInfo.objects.all()
    serializer_class = CarInfoSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET',"POST"])
@permission_classes([permissions.AllowAny])
def api_root(request, format=None):
    breakpoint()
    return Response({
        'users': reverse('sales:api-list', request=request, format=format),
        # 'snippets': reverse('sales:user-list', request=request, format=format)
    })