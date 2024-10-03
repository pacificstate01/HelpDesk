from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView,TemplateView
from .models import Ticket
from .forms import TicketForm
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'tickets/base.html'

class TicketListView(ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket_list')