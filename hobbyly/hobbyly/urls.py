
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import HomeView, LoginView, RegisterView, LegalView, logout_view
from profiles.views import ProfileDetailView, ProfileUpdateView, ProfileListView
from django.conf.urls.static import static  
from posts.views import PostCreateView, PostDetailView, liked_post, CommentDeleteView
from contact.views import ContactFormView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', RegisterView.as_view(), name='register'),
    path('perfil/miembros/', ProfileListView.as_view(), name='profile_list'),
    path('perfil/<pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('perfil/actualizar/<pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('posts/crear', PostCreateView.as_view(), name='post_create'),
    path('posts/<pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/like/<pk>/', liked_post, name='liked_post'),
    path('comentario/<pk>/eliminar/', CommentDeleteView.as_view(), name='delete_comment'),
    path('contacto/', ContactFormView.as_view(), name='contact'),
    path('legal/', LegalView.as_view(), name='legal'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
