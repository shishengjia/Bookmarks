from django.conf.urls import url
from .views import ImageCreatView, ImageDetailView, ImageLikeView

urlpatterns = [
    url(r'^create/$', ImageCreatView.as_view(), name='create'),
    url(r'^detail/(?P<id>\d+)/$', ImageDetailView.as_view(), name="detail"),
    url(r'^like/$', ImageLikeView.as_view(), name='like'),
]