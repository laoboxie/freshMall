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
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
import xadmin


from goods.views import GoodsView

router = routers.SimpleRouter()
#配置goods的url
router.register(r'goods', GoodsView, base_name="goods")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^media/(.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    # apps
    url(r'', include(router.urls)),
    # api文档
    path('docs/', include_docs_urls(title='生鲜电商')),
    path('api-auth/', include('rest_framework.urls')),

]




