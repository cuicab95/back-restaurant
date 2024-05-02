from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from back_restaurant.config.paginations import DefaultPagination
from .serializers import RestaurantSerializer, RestaurantListSerializer, BulkRestaurantSerializer
from .models import Restaurant
from .filters import RestaurantFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .services.bulk_csv import BulkRestaurantCSV


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
        elif self.action == "bulk_csv_restaurant":
            return BulkRestaurantSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def bulk_csv_restaurant(self, request, pk=None, **kwargs):
        try:
            serializer = self.get_serializer(data=request.FILES)
            serializer.is_valid(raise_exception=True)
            csv_file = serializer.validated_data.get('csv_file')
            data = BulkRestaurantCSV.read_csv(csv_file)
            return Response(data=data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
