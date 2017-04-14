from django.conf.urls import url,include
from .views import LoginView, LogoutView, RegisterView, UserListView, UserDetailView, UserFollowView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^list/$', UserListView.as_view(), name='list'),
    # Make sure that you place this pattern before the user_detail URL pattern.
    # Otherwise, any requests to /users/follow/ will match the regular expression of
    # the user_detail pattern and it will be executed instead. Remember that in every
    # HTTP request Django checks the requested URL against each pattern in order of
    # appearance and stops at the first match.
    url(r'^follow/$', UserFollowView.as_view(), name='follow'),
    url(r'^(?P<username>[-\w]+)/$', UserDetailView.as_view(), name='detail'),

]