from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from back_restaurant.config.paginations import DefaultPagination
from .serializers import RestaurantSerializer, RestaurantListSerializer
from .models import Restaurant
from .filters import RestaurantFilter


class RestaurantViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RestaurantFilter
    pagination_class = DefaultPagination
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RestaurantListSerializer
        return super().get_serializer_class()

