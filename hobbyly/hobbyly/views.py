from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import  DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView 
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from posts.models import Post
from profiles.models import Follow
from django.contrib.auth.decorators import login_required


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            seguidos = Follow.objects.filter(follower=self.request.user.profile).values_list("following__user", flat=True)
            last_posts = Post.objects.filter(user__profile__user__in=seguidos)
        
        else:
            last_posts = Post.objects.all().order_by('-created_at')[:5]
        
        context['last_posts'] = last_posts
        return context 


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f"Bienvenido de nuevo {user.username}")
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.add_message(self.request, messages.ERROR, f"Usuario y/o contraseña no válido")
            return super(LoginView, self).form_invalid(form)


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Sesión cerrada correctamente")

    return HttpResponseRedirect(reverse('home'))


class RegisterView(CreateView):
    template_name = 'core/register.html'
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente")
        return super(RegisterView, self).form_valid(form)


class LegalView(TemplateView):
    template_name = 'core/legal.html'



