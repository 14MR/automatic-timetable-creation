from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from users.views import ObtainAuthTokenEmail, SignupApiView, ProfileApiView, GroupViewSet

group_router = routers.DefaultRouter()
group_router.register(r"groups", GroupViewSet, basename="group")
urlpatterns = [
    url("login", ObtainAuthTokenEmail.as_view(), name="users-login"),
    url("signup", SignupApiView.as_view(), name="users-signup"),
    url("profile", ProfileApiView.as_view(), name="users-profile"),
    url(r"^", include(group_router.urls), name="group"),
    # url('', GroupViewSet.as_view({'get': 'list'}))
]
