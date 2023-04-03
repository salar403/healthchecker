from django.urls import path
from monitoring import views

urlpatterns = [
    path("endpoint/add/", views.AddEndpoint.as_view(), name="add_endpoint"),
    path("endpoint/list/", views.ListEndpoints.as_view(), name="list_endpoints"),
    path("endpoint/delete/", views.DeleteEndpoint.as_view(), name="delete_endpoint"),
    path("healthstate/live/", views.LiveStates.as_view(), name="live_healthstates"),
    path("healthstate/historical/", views.HistoricalStates.as_view(), name="historical_healthstates"),
]

    