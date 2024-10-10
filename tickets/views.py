from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView,TemplateView
from .models import Ticket,Tech
from .forms import TicketForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404



class HomeView(TemplateView):
    template_name = 'tickets/base.html'
@method_decorator(login_required,name="dispatch")
class TicketListView(ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(tech=Tech.objects.get(user=self.request.user))

@method_decorator(login_required,name="dispatch")
class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'


    def get_object(self,queryset=None):
        ticket = super().get_object(queryset)
        if ticket.tech == Tech.objects.get(user=self.request.user):
            return ticket
        else:
            raise Http404("No tienes permiso")



@method_decorator(login_required,name="dispatch")
class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')


    def form_valid(self, form):
        tech_instance = Tech.objects.get(user = self.request.user)
        form.instance.tech = tech_instance
        self.object = form.save()
        response = super().form_valid(form)
        return response

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket_list')