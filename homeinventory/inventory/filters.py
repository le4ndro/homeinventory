import django_filters as filters

from homeinventory.inventory.models import Item


class ItemFilter(filters.FilterSet):
    model = filters.CharFilter(lookup_expr='icontains')
    make = filters.CharFilter(lookup_expr='icontains')
    purchased_from = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Item
        fields = [
                    'make',
                    'model',
                    'id_number',
                    'purchased_from',
                    'category',
                    'location'
                ]
