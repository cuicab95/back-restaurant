from django.contrib.gis.geos import Point


def convert_to_point(latitude, longitude):
    point = Point(longitude, latitude)
    return point
