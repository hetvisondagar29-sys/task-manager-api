from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import LogoutView, RegisterView, TaskViewSet

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
]
