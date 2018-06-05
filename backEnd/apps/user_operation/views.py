from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


from .models import UserFav
from .serializers import UserFavSerializer
# Create your views here.


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

