from rest_framework import serializers
from .models import Restaurant
from .utils import convert_to_point


class RestaurantSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    external_id = serializers.UUIDField(required=False)

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "rating",
            "name",
            "site",
            "email",
            "phone",
            "street",
            "city",
            "state",
            "latitude",
            "longitude",
            "external_id",
        )

    def create(self, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        location = convert_to_point(latitude, longitude)
        return Restaurant.objects.create(location=location, **validated_data)

    def update(self, instance, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        location = convert_to_point(latitude, longitude)
        validated_data.update({'location': location})
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RestaurantListSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "rating",
            "name",
            "site",
            "email",
            "phone",
            "street",
            "city",
            "state",
            "latitude",
            "longitude",
            "external_id",
        )


class BulkRestaurantSerializer(serializers.Serializer):
    csv_file = serializers.FileField()


class StatisticsSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.IntegerField()
