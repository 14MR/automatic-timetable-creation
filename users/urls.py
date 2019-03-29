from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from users.views import (
    ObtainAuthTokenEmail,
    SignupApiView,
    ProfileApiView,
    GroupViewSet,
    YearGroupViewSet,
    UserGroupView)

group_router = routers.DefaultRouter()
group_router.register(r"groups", GroupViewSet, basename="group")

year_group_router = routers.DefaultRouter()
year_group_router.register(r"year_groups", YearGroupViewSet, basename="year_group")

urlpatterns = [
    url("login", ObtainAuthTokenEmail.as_view(), name="users-login"),
    url("signup", SignupApiView.as_view(), name="users-signup"),
    url("profile", ProfileApiView.as_view(), name="users-profile"),
    url(r"^", include(group_router.urls), name="groups"),
    url(r"^", include(year_group_router.urls), name="year_groups"),
    path('<int:user_id>/groups/<int:group_id>/', UserGroupView.as_view()),
]
