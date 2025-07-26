from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages

class ContactFormView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Tu mensaje fue enviado correctamente.")
        return super().form_valid(form)
