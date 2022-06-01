from django import forms
from .models import CarCompany, SellCarListing, CarSaleRecord
from django.contrib.auth.models import User
from datetime import datetime





class SellCarForm(forms.ModelForm):
    class Meta:
        model = SellCarListing
        # fields = ("make", "model", "year", 
        #     "condition", "picture", "price", 
        #     "owner_name", "owner_mobile",
        # )
        fields = "__all__"
        exclude = ("slug",)
    def __init__(self, *args, **kwargs):
        super(SellCarForm, self).__init__(*args, **kwargs)
        years = [x for x in range(1950, 2022)]
        self.fields["year"].widget = forms.SelectDateWidget(years=years)
        self.fields["price"] = forms.IntegerField(max_value = 100000, min_value = 1000)
