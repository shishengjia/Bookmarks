from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .settings import MEDIA_ROOT
from users.views import DashBoardView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', DashBoardView.as_view(), name='index'),
    #  配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^image/', include('image.urls', namespace='image')),
]