"""backEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views import static
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import xadmin


from goods.views import GoodsView, GoodsCategoryView
from users.views import SmsCodeViewset, UserRegViewset
router = routers.SimpleRouter()
#配置goods的url
router.register(r'goods', GoodsView, base_name="goods")
router.register(r'categorys', GoodsCategoryView, base_name="category")
router.register(r'smscode', SmsCodeViewset, base_name="smscode")
router.register(r'users', UserRegViewset, base_name="users")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^media/(.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    # apps
    url(r'', include(router.urls)),
    # api文档
    path('docs/', include_docs_urls(title='生鲜电商')),
    path('api-auth/', include('rest_framework.urls')),
    # drf自带token
    url(r'^api-token-auth/', views.obtain_auth_token),
    # drf-jwt的token
    url(r'^login/', obtain_jwt_token),

]




