from django.urls import path
from .views import inscription_view, result_view

urlpatterns = [
    path("", inscription_view, name="inscription"),
    path("result/", result_view, name="result"),
]
