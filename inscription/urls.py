from django.urls import path
from .views import all_clients_view, blacklist_client_action, inscription_view, result_view, verify_client_action, verify_clients_view

urlpatterns = [
    path("", inscription_view, name="inscription"),
    path("result/", result_view, name="result"),
    path('verify-clients/', verify_clients_view, name="verify_clients"),
    path('verify-client/<int:client_id>/', verify_client_action, name="verify_client"),
    path('blacklist-client/<int:client_id>/', blacklist_client_action, name="blacklist_client"),
    path("all-clients/", all_clients_view, name="all_clients"),  # <-- new page

]
