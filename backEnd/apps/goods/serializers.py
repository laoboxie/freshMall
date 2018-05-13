from rest_framework import serializers

from .models import Goods, GoodsCategory


class GoodsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsSerializers(serializers.ModelSerializer):
    category = GoodsCategorySerializers()
    class Meta:
        model = Goods
        fields = ("id", "name", "category", "shop_price")

