import django_filters
from .models import Apartment

class ApartmentFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()
    class Meta:
        model = Apartment
        fields = {
            'apartment_type':['exact'],
            'count_bedroom':['exact'],
            'price':['gt', 'lt'],
        }
