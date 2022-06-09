from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_superuser(self, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(password, **other_fields)

    def create_user(self, password, **other_fields):

        other_fields.setdefault("is_staff", False)
        other_fields.setdefault("is_superuser", False)
        other_fields.setdefault("is_active", True)

        user = self.model(**other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=40, unique=True)
    name = models.CharField("first name", max_length=50)
    mobile = models.BigIntegerField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name", "mobile"]


class CarInfo(models.Model):

    condition_choices = (
        ("Poor", "poor"),
        ("Fair", "fair"),
        ("Good", "good"),
        ("Excellent", "excellent"),
    )

    status_choices = (
        ("available", "available"),
        ("booked", "booked"),
        ("sold", "sold"),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    make = models.CharField(max_length=50)
    model_name = models.CharField(max_length=20)
    condition = models.CharField(choices=condition_choices, max_length=90)
    picture = models.ImageField(blank=True, null=True, upload_to="blog/")
    price = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=status_choices, max_length=90, default="available"
    )
    commission_rate = models.IntegerField(default=5)
    commission = models.IntegerField(default=0)

    def __str__(self):
        return (
            self.model_name + " by: " + str(self.make) + "- " + str(self.owner.username)
        )


class CarSaleRecord(models.Model):
    car_listing = models.ForeignKey(
        CarInfo, on_delete=models.CASCADE, related_name="purchase"
    )
    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    denied = models.BooleanField(default=False)

    def __str__(self):
        return str(self.car_listing) + "sold to: " + self.name