from django import forms
from django.contrib.auth.models import User
from profiles.models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name','username', 'email', 'password']

    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        user.save()

        UserProfile.objects.create(user=user)

        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput())


    