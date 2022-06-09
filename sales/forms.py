from django import forms
from .models import CarInfo, CarSaleRecord
from django.core.mail import send_mail


class SellCarForm(forms.ModelForm):
    class Meta:
        model = CarInfo
        fields = "__all__"
        exclude = ("owner", "status", "commission")

    def __init__(self, *args, **kwargs):
        """
        set limits to the year and price fields. Set choices for condition field.
        """
        super(SellCarForm, self).__init__(*args, **kwargs)
        self.fields["price"] = forms.IntegerField(max_value=100000, min_value=1000)
        self.fields["year"] = forms.IntegerField(min_value=1000, max_value=2023)
        self.fields["condition"].choices = [
            ("Poor", "poor"),
            ("Fair", "fair"),
            ("Good", "good"),
            ("Excellent", "excellent"),
        ]
        self.fields["commission_rate"].label = "Commission Rate (in %):"

    def save(self, commit=False, **kwargs):
        """
        sets the current user as the owner for the car_info record. Also sets the commission field
        """
        car_listing = super().save(commit)
        car_listing.owner = kwargs["user"]
        car_listing.commission = car_listing.price * (car_listing.commission_rate / 100)
        car_listing.save()


class BuyCarForm(forms.ModelForm):
    class Meta:
        model = CarSaleRecord
        exclude = ("car_listing", "denied")

    def save(self, commit=False, **kwargs):
        """
        sets the current car_info record's status as booked. sets a reference to the car_info record to the sale_record
        Sends a mail to the admin regarding the new buy request for this listing.
        """
        sale_record = super().save(commit)
        car_listing = kwargs["car_listing"]
        sale_record.car_listing = car_listing
        car_listing.status = "booked"
        car_listing.save()
        sale_record.save()

        # send mail here
        # send_mail(
        #     subject = f'A User has applied for buying the car: {str(car_listing)}',
        #     message = f'''
        #     Customer: {sale_record.name} has requested to buy the car: {str(car_listing.make)} model: {str(car_listing.model_name)} listed by: {str(car_listing.owner.username)} (phone: {str(car_listing.owner.mobile)} ).

        #     The asking price of the listed car is: {str(car_listing.price)}

        #     The buyer is: {sale_record.name} (phone: {sale_record.mobile}).

        #     Your commission will be: $ {car_listing.commission} at the rate of {car_listing.commission_rate}%.

        #     Net transferrable amount to the seller is: ${car_listing.price - car_listing.commission}

        #     ''',
        #     from_email = 'satansin2001@gmail.com',
        #     recipient_list = ['stmsng2001@gmail.com', 'karan@example.org'],
        #     fail_silently=False,
        #     )

    def __init__(self, *args, **kwargs):
        """
        sets the initial value for mobile and name fields
        """
        mobile = kwargs.pop("mobile", "")
        name = kwargs.pop("name", "")
        super(BuyCarForm, self).__init__(*args, **kwargs)
        self.fields["mobile"].initial = mobile
        self.fields["name"].initial = name
