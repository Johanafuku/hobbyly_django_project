from django.urls import reverse_lazy, reverse
from django.views.generic import  DetailView, UpdateView, ListView, FormView
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import  HttpResponseRedirect
from .forms import ProfileFollow
from .models import Follow


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView, FormView):
    model = UserProfile
    template_name = "profiles/profile_detail.html"
    context_object_name = 'profile'
    form_class = ProfileFollow

    def get_initial(self):
        self.initial['profile_pk'] = self.get_object().pk
        return super().get_initial()

    def form_valid(self, form):
        profile_pk = form.cleaned_data.get("profile_pk")
        action = form.cleaned_data.get("action")
        following = UserProfile.objects.get(pk=profile_pk)

        if Follow.objects.filter(
                follower=self.request.user.profile,
                following=following
            ).count():
            Follow.objects.filter(
                follower=self.request.user.profile,
                following=following
            ).delete()
            messages.add_message(self.request, messages.SUCCESS, f"Ya no sigues a {following.user.username}")
        else:
            Follow.objects.get_or_create(
                follower=self.request.user.profile,
                following=following
            )
            messages.add_message(self.request, messages.SUCCESS, f"Ahora sigues a {following.user.username}")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile_detail', args=[self.get_object().pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #comprobar si seguimos al usuario
        following = Follow.objects.filter(follower=self.request.user.profile, following=self.get_object()).exists()
        context['following'] = following

        return context


class ProfileListView(ListView):
    model = UserProfile
    template_name = "profiles/profile_list.html"
    context_object_name = 'profiles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserProfile.objects.all().order_by('user__username').exclude(user=self.request.user)
        return UserProfile.objects.all().order_by('user__username')


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "profiles/profile_update.html"
    context_object_name = 'profile'
    fields = ['profile_picture','bio','birth_date']

    def dispatch(self, request, *args, **kwargs):
        user_profile =  self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Cambios actualizados correctamente")
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile_detail', args=[self.object.pk])


