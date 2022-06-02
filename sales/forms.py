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
        years = [x for x in range(1950, 2023)]
        self.fields["year"].widget = forms.SelectDateWidget(years=years)
        self.fields["price"] = forms.IntegerField(max_value = 100000, min_value = 1000)


    def save(self, commit=False):
        car_listing = super().save(commit)
        car_listing.owner = self.request.user