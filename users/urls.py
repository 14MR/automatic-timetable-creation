from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from users.views import (
    ObtainAuthTokenEmail,
    SignupApiView,
    ProfileApiView,
    GroupViewSet,
    YearGroupViewSet,
    UserGroupView, UserGroupAdd)

router = routers.DefaultRouter()
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"year_groups", YearGroupViewSet, basename="year_group")

urlpatterns = [
    url("login", ObtainAuthTokenEmail.as_view(), name="users-login"),
    url("signup", SignupApiView.as_view(), name="users-signup"),
    url("profile", ProfileApiView.as_view(), name="users-profile"),
    url(r"^", include(router.urls), name="groups"),
    path('<int:user_id>/groups/<int:group_id>/', UserGroupAdd.as_view(), name='users-add-group'),
    path('<int:user_id>/groups/', UserGroupView.as_view(), name='users-view-group'),
]
