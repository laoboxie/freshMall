from django_filters import rest_framework

from .models import Goods


class GoodsFilter(rest_framework.FilterSet):
    min_price = rest_framework.NumberFilter(name="shop_price", lookup_expr='gte')
    max_price = rest_framework.NumberFilter(name="shop_price", lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price']