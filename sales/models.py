from django.db import models

# Create your models here.


class SellCarListing(models.Model):

    condition_choices = (
        ('Poor', 'poor'),
        ("Fair","fair"),
        ("Good","good"),
        ("Excellent","excellent"),
    )

    owner_name = models.CharField(max_length=100)
    owner_mobile = models.BigIntegerField()

    make = models.CharField(max_length=50)
    model_name = models.CharField(max_length=20)
    condition = models.CharField(choices = condition_choices,max_length= 90)
    picture = models.ImageField(blank=True, null=True, upload_to = "blog/")
    price = models.IntegerField()
    year = models.DateField()

    sold = models.BooleanField(default = False)

    def __str__(self):
        return self.model_name + " by: "+ str(self.make) +"- "+ str(self.owner_name)



class CarSaleRecord(models.Model):
    listing = models.ForeignKey(SellCarListing, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()