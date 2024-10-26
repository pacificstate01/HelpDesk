from django.urls import path
from .views import TicketListView,TicketDetailView,TicketCreateView,StatusUpdateView


urlpatterns = [
    path('list/',TicketListView.as_view(),name='ticket_list'),
    path('detail/<int:pk>',TicketDetailView.as_view(),name='ticket_detail'),
    path('tickets/create',TicketCreateView.as_view(),name='ticket_create'),
    path('tickets/update/<int:pk>',StatusUpdateView.as_view(),name='ticket_update'),
]
