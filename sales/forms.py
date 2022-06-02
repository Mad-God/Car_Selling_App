from django import forms
from .models import CarInfo, CarSaleRecord
from django.contrib.auth.models import User
from datetime import datetime

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
