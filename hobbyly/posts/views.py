from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post, Comment
from .forms import PostCreateForm, CommentCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import  DetailView
from django.http import   JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    template_name = 'posts/post_create.html'
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Publicación creada correctamente")
        
        return super(PostCreateView,self).form_valid(form)
    

class PostDetailView(DetailView, CreateView):
    template_name = 'posts/post_detail.html'
    model = Post
    context_object_name = 'post'
    form_class = CommentCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        
        return super(PostDetailView,self).form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', args=[self.get_object().pk])
    

@login_required
def liked_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.unlike(request.user)
        return JsonResponse(
            {
                'liked':False,
                'nlikes':post.likes.all().count()
            }
        )
    else:
        post.like(request.user)
        return JsonResponse(
            {
                'liked':True,
                'nlikes':post.likes.all().count()
            }
        )


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_delete.html'  
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[self.object.post.pk])  # redirige al post relacionado

    def test_func(self):
        """Solo el autor del comentario puede eliminarlo"""
        comment = self.get_object()
        return self.request.user == comment.user