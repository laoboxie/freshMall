from django_filters import rest_framework
from django.db.models import Q

from .models import Goods


class GoodsFilter(rest_framework.FilterSet):
    pricemin = rest_framework.NumberFilter(name="shop_price", lookup_expr='gte')
    pricemax = rest_framework.NumberFilter(name="shop_price", lookup_expr='lte')
    top_category = rest_framework.NumberFilter(method="category_filter")

    def category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']