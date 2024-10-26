from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView,TemplateView
from django.views.generic.edit import FormMixin
from .models import Ticket, Status, Tech
from .forms import TicketForm,HistoryForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404,JsonResponse



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
class TicketDetailView(FormMixin,DetailView):
    model = Ticket
    form_class = HistoryForm
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'


    def get_object(self,queryset=None):
        ticket = super().get_object(queryset)
        if ticket.tech == Tech.objects.get(user=self.request.user):
            return ticket
        else:
            raise Http404("No tienes permiso")

    def get_context_data(self,**kwargs):
        context = super(TicketDetailView,self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        history = form.save(commit = False)
        history.save()
        self.object.history.add(history)
        return super(TicketDetailView,self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket_detail',kwargs = {'pk':self.object.pk})




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
        if self.request.headers.get('X-Requested-With')=='XMLHttpRequest':
            data = {
                'status': 'success',
                'message': 'The ticket was closed successfully.'
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        # Este método se llama si el formulario enviado no es válido.
        
        # Comprueba si la petición es una solicitud AJAX.
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si es una solicitud AJAX, prepara la respuesta JSON con los errores.
            data = {
                'status': 'error',
                'message': 'El formulario contiene errores.',
                'errors': form.errors.as_json()  # Convierte los errores del formulario a JSON.
            }
            # Devuelve una respuesta JSON con el estado de error y los mensajes correspondientes.
            return JsonResponse(data, status=400)
        else:
            # Si no es una solicitud AJAX, sigue el flujo normal de mostrar el formulario con errores.
            return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class StatusUpdateView(UpdateView):
    # Indica el modelo que se va a actualizar.
    model = Ticket
    # URL a la que se redirige al usuario después de una actualización exitosa.
    success_url = reverse_lazy('ticket_list')
    # Especifica los campos del formulario que se van a incluir en la vista.
    fields = ['status']

    # Obtiene el objeto que se está actualizando.
    def get_object(self, queryset=None):
        # Obtiene el objeto del modelo Ticket utilizando la implementación base.
        ticket = super().get_object(queryset)
        # Actualiza el estado del ticket al estado 'Cerrado'.
        ticket.status = Status.objects.get(name='Closed')
        # Guarda el cambio en la base de datos.
        ticket.save()
        # Retorna el objeto ticket actualizado.
        return ticket
    
    # Se llama si los datos del formulario son válidos.
    def form_valid(self, form):
        # Guarda el objeto form y actualiza self.object con el objeto guardado.
        self.object = form.save()
        
        # Verifica si la petición es AJAX.
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Prepara los datos para la respuesta JSON.
            data = {
                'status': 'success',
                'message': 'El ticket se ha cerrado con éxito.'
            }
            # Envía una respuesta JSON con los datos.
            return JsonResponse(data)
        else:
            # Si no es una petición AJAX, continúa con el comportamiento normal.
            return super().form_valid(form)
        
    # Se llama si los datos del formulario no son válidos.
    def form_invalid(self, form):
        # Verifica si la petición es AJAX.
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Prepara los datos del error para la respuesta JSON.
            data = {
                'status': 'error',
                'message': 'Error al cerrar ticket.',
                'errors': form.errors.as_json()  # Convierte los errores del formulario a JSON.
            }
            # Envía una respuesta JSON con los datos de error.
            return JsonResponse(data, status=400)
        else:
            # Si no es una petición AJAX, continúa con el comportamiento normal de error.
            return super().form_invalid(form)