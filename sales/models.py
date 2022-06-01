from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length = 100)



class Listing(models.Model):

    condition_choices = (
        ('Poor', 'pur'),
        ("Fair","fer"),
        ("Good","gud"),
        ("Excellent","exl"),
    )

    owner_name = models.CharField(max_length=100)
    owner_mobile = models.BigIntegerField()

    make = models.ForeignKey(Company, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=20)
    condition = models.CharField(choices = condition_choices,max_length= 100)
    picture = models.ImageField(blank=True, null=True, upload_to = "blog/")
    price = models.IntegerField()
    year = models.DateField()



class Sale(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name ="sales")

    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
