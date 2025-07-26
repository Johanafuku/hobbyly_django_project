from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name='Imagen de perfil')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Biografía')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    followers = models.ManyToManyField('self',symmetrical=False, related_name='following', through='Follow')

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


    def follow(self, profile):
        follow, creado = Follow.objects.get_or_create(follower=self, following=profile)
        return creado

    def unfollow(self, profile):
        if Follow.objects.filter(follower=self, following=profile).count():
            Follow.objects.filter(follower=self, following=profile).delete()
            return True
        return False


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower_set', verbose_name="¿quién me sigue o de quien soy seguidor?")
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following_set', verbose_name="¿a quién sigo?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="¿desde cuándo lo sigue?")

    class Meta:
        unique_together = ("follower","following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
    class Meta:
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'