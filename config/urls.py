from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def home(request):
    """Simple welcome page so http://127.0.0.1:8000/ does not show a 404."""
    return JsonResponse(
        {
            "project": "Task Manager API (Django + Django REST Framework)",
            "endpoints": {
                "register": "POST /api/register/",
                "login": "POST /api/login/",
                "logout": "POST /api/logout/",
                "tasks": "GET, POST /api/tasks/",
                "task detail": "GET, PUT, PATCH, DELETE /api/tasks/<id>/",
                "admin panel": "/admin/",
            },
        }
    )


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
