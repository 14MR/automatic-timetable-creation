from django.conf.urls import url

from users.views import ObtainAuthTokenEmail

urlpatterns = [
    url('login', ObtainAuthTokenEmail.as_view()),
]
