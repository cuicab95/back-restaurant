import csv
import io
from ..models import Restaurant
from ..serializers import RestaurantSerializer


class BulkRestaurantCSV:

    @classmethod
    def read_csv(cls, csv_file):
        try:
            with io.TextIOWrapper(csv_file, encoding='utf-8') as text_csv_file:
                reader = csv.reader(text_csv_file)
                index = 0
                for row in reader:
                    if index != 0:
                        data = cls.get_data_processed(row)
                        cls.save_or_update_data(data)
                    index += 1
            return
        except Exception as error:
            return {'error': str(error)}

    @classmethod
    def save_or_update_data(cls, data):
        restaurant = Restaurant.objects.filter(external_id=data.get('external_id')).first()
        if restaurant:
            serializer = RestaurantSerializer(instance=restaurant, data=data)
        else:
            serializer = RestaurantSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @classmethod
    def get_data_processed(cls, data):
        (external_id, rating, name, site, email, phone,
         street, city, state, lat, lng) = data
        return {
            'external_id': external_id,
            'rating': rating,
            'name': name,
            'site': cls.clean_string(site),
            'email': cls.clean_string(email),
            'phone': cls.clean_phone(phone),
            'street': street,
            'city': city,
            'state': state,
            'latitude': lat,
            'longitude': lng,
        }

    @classmethod
    def clean_phone(cls, phone):
        phone = phone.strip()
        return phone.replace('-', '').replace('.', '').replace(' ', '')

    @classmethod
    def clean_string(cls, value):
        return value.replace(' ', '')
