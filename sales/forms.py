from django import forms
from .models import CarInfo, CarSaleRecord
from django.contrib.auth.models import User
from django.core.mail import send_mail

class SellCarForm(forms.ModelForm):
    class Meta:
        model = CarInfo

        fields = "__all__"
        exclude = ("owner", "sold",)


    def __init__(self, *args, **kwargs):
        super(SellCarForm, self).__init__(*args, **kwargs)
        self.fields["price"] = forms.IntegerField(max_value = 100000, min_value = 1000)
        self.fields["year"] = forms.IntegerField(min_value = 1000, max_value = 2023)
        self.fields["condition"].choices = [
            ('Poor', 'poor'), ('Fair', 'fair'), ('Good', 'good'), ('Excellent', 'excellent')
        ]


    def save(self, commit=False, *args, **kwargs):
        car_listing = super().save(commit)
        car_listing.owner = kwargs["user"]
        car_listing.save()



class BuyCarForm(forms.ModelForm):
    class Meta():
        model = CarSaleRecord
        exclude = ("car_listing","finalised",)
    
    def save(self, commit=False, *args, **kwargs):
        sale_record = super().save(commit)
        car_listing = kwargs["car_listing"]
        sale_record.car_listing = car_listing
        car_listing.sold = True
        car_listing.save()
        sale_record.save()
        # send mail here
        mail_result = send_mail(
            subject = f'A User has applied for buying the car: {str(car_listing)}',
            message = f'''Customer: {sale_record.name} has requested to buy the car.:{str(car_listing)}
            Your commission will be: $ {sale_record.commission}.
            The buyer is: {sale_record.name} (phone: {sale_record.mobile})
            ''',
            from_email = 'satansin2001@gmail.com',
            recipient_list = ['stmsng2001@gmail.com', 'karan@example.org'],
            fail_silently=False,
            )


    def __init__(self, *args, **kwargs):
        mobile = kwargs.pop("mobile", "")
        name = kwargs.pop("name", "")
        super(BuyCarForm, self).__init__(*args, **kwargs)
        self.fields["mobile"].initial = mobile
        self.fields["name"].initial = name
        