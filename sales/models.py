from django.db import models
from django.utils.text import slugify   
from django.db.models.signals import pre_save
# Create your models here.


class CarCompany(models.Model):
    name = models.CharField(max_length = 100)



class SellCarListing(models.Model):

    condition_choices = (
        ('Poor', 'pur'),
        ("Fair","fer"),
        ("Good","gud"),
        ("Excellent","exl"),
    )

    owner_name = models.CharField(max_length=100)
    owner_mobile = models.BigIntegerField()

    # make = models.ForeignKey(CarCompany, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model_name = models.CharField(max_length=20)
    condition = models.CharField(choices = condition_choices,max_length= 90)
    picture = models.ImageField(blank=True, null=True, upload_to = "blog/")
    price = models.IntegerField()
    year = models.DateField()

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.model_name + " by: "+ str(self.make) +"- "+ str(self.owner_name)



class CarSaleRecord(models.Model):
    listing = models.ForeignKey(SellCarListing, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()




def create_listing_slug(instance, new_slug = None):
    slug = slugify(instance.make + " " +instance.model_name)
    if new_slug is not None:
        slug = new_slug
    qs = SellCarListing.objects.filter(slug = slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s"%(slug, qs.first().id)
        return create_listing_slug(instance, new_slug = new_slug)
    return slug

def pre_listing_created_signal(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_listing_slug(instance)
  

# post_save.connect(post_blog_created_signal, sender = Listing)
pre_save.connect(pre_listing_created_signal, sender = SellCarListing)
# pre_save.connect(pre_category_created_signal, sender = Category)