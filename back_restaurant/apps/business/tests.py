from back_restaurant.config.tests import ConfigAPITest
from rest_framework import status
from .models import Restaurant


class RestaurantTestCase(ConfigAPITest):
    def setUp(self):
        self.user = self.create_user()
        self.path = "/business/restaurant/"
        self.authenticate(self.user)
        self.test_restaurant_create()

    def test_restaurants_list(self):
        response = self.client.get(f"{self.path}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statistics_list(self):
        latitude = 19.4394962074356
        longitude = -99.1264430870515
        radius = 600
        response = self.client.get(f"{self.path}statistics/?latitude={latitude}&longitude={longitude}&radius={radius}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_delete(self):
        restaurant = Restaurant.objects.first()
        response = self.client.delete(f"{self.path}{restaurant.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_restaurant_update(self):
        restaurant = Restaurant.objects.first()
        data_request = {
            "rating": 0,
            "name": "Restaurante Demo editado",
            "site": "http://demo-editado.com/",
            "email": "test-3@example.com",
            "phone": "123467865",
            "street": "Calle Test",
            "city": "Mérida",
            "state": "Yucatán",
            "latitude": 19.4341320322948,
            "longitude": 99.1326235608364
        }
        response = self.client.patch(f"{self.path}{restaurant.id}/", data=data_request)
        self.assertNotEqual(response.data["name"], restaurant.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_create(self):
        data_request = {
            "rating": 0,
            "name": "Restaurante 3",
            "site": "http://demo.com/",
            "email": "test-2@example.com",
            "phone": "123467865",
            "street": "Calle benito",
            "city": "merida",
            "state": "yucatan",
            "latitude": 19.4400570537131,
            "longitude": -99.1270470974249
        }

        response = self.client.post(f"{self.path}", data=data_request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
