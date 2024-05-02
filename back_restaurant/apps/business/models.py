from django.db import models
import uuid
from back_restaurant.apps.general.models import UuidMixin, TimestampMixin, SoftDeleteMixin
from back_restaurant.apps.general.catalogs.business import RatingChoices
from django.contrib.gis.db.models import PointField

# Create your models here.


class Restaurant(UuidMixin, TimestampMixin, SoftDeleteMixin):
    rating = models.IntegerField(choices=RatingChoices)
    name = models.CharField(max_length=150)
    site = models.URLField()
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=100)
    location = PointField()

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"



