from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework
from rest_framework.pagination import PageNumberPagination
from .serializers import GoodsSerializers
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
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page_index'


class GoodsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializers
    pagination_class = StandardPagination
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    filter_class = GoodsFilter
    ordering_fields = ('shop_price',)
    search_fields = ('name',)

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     goods_serializer = GoodsSerializers(goods, many=True)
    #
    #     res = ResponseJson()
    #     res.setResult(goods_serializer)
    #     return Response(res.response())


