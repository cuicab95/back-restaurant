from django_filters.rest_framework import FilterSet
from .models import Restaurant
from django_filters.rest_framework import CharFilter


class RestaurantFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    city = CharFilter(field_name="city", lookup_expr="icontains")
    state = CharFilter(field_name="state", lookup_expr="icontains")

    class Meta:
        model = Restaurant
        fields = [
            "name",
            "city",
            "state",
        ]
