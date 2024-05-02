from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from back_restaurant.config.paginations import DefaultPagination
from .serializers import RestaurantSerializer, RestaurantListSerializer, BulkRestaurantSerializer, StatisticsSerializer
from .models import Restaurant
from .filters import RestaurantFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .services.bulk_csv import BulkRestaurantCSV
from .utils import convert_to_point
from django.db.models import StdDev, Avg


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
        elif self.action == "statistics":
            return StatisticsSerializer
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

    @action(detail=False)
    def statistics(self, request, pk=None, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')
        location = convert_to_point(latitude, longitude)
        radius = serializer.validated_data.get('radius')
        # Calcular el área del círculo
        circle_area = location.buffer(radius)
        queryset = self.get_queryset()
        queryset = queryset.filter(location__within=circle_area)
        data = {
            'count': queryset.count(),
            'avg': round(queryset.aggregate(avg_rating=Avg('rating')).get('avg_rating'), 4),
            'std': round(queryset.aggregate(std_dev_rating=StdDev('rating')).get('std_dev_rating'), 4),
        }
        return Response(data=data, status=status.HTTP_200_OK)
