from django.conf.urls import url

from users.views import ObtainAuthTokenEmail, SignupApiView

urlpatterns = [
    url('login', ObtainAuthTokenEmail.as_view()),
    url('signup', SignupApiView.as_view())
]
