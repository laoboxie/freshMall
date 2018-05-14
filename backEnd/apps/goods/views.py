from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework
from rest_framework.pagination import PageNumberPagination
from .serializers import GoodsSerializers, GoodsCategorySerializers2
from .models import Goods, GoodsCategory
from .filters import GoodsFilter
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import json


# Create your views here.
class ResponseJson():
    def __init__(self):
        self.res = {
            'success': True,
            'message': '',
            'result': {},
        }

    def setSuccess(self, boolType):
        self.res['success'] = boolType

    def setMessage(self, msg):
        self.res['message'] = msg

    def setResult(self, ser):
        self.res['result'] = ser.data

    def response(self):
        return self.res


class StandardPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


class GoodsView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializers
    pagination_class = StandardPagination
    filter_class = GoodsFilter
    # django-filter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    ordering_fields = ('shop_price', 'sold_num', 'add_time')
    search_fields = ('name', 'goods_desc', 'goods_brief')

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     goods_serializer = GoodsSerializers(goods, many=True)
    #
    #     res = ResponseJson()
    #     res.setResult(goods_serializer)
    #     return Response(res.response())


class GoodsCategoryView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializers2





