from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage


class GoodsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializers1(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializers(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializers2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializers1(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image", )


class GoodsSerializers(serializers.ModelSerializer):
    category = GoodsCategorySerializers()
    images = GoodsImagesSerializers(many=True)

    class Meta:
        model = Goods
        fields = "__all__"

