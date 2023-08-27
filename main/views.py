from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Profile, Response
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import PostForm, ResponseForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin


# Представление списка публикаций
class PostsList(ListView):
    model = Post
    ordering = '-create_date'
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 6


class UserActivity(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-create_date'
    template_name = 'user_activity.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_responses = Response.objects.filter(user=self.request.user)
        context['posts_with_user_responses'] = Post.objects.filter(id__in=user_responses.values('post__id'))
        return context


# Представление одиночной публикации
class PostDetails(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        text = request.POST.get('text')
        response = Response(post=post, text=text, user=request.user)
        response.save()
        post.responses_sum += 1
        return redirect('post_details', pk=post.id)

    # Добавляем в контекст инфу - состоит ли пользователь в группе authors
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.filter(post=self.object)
        return context


# Представление для создания новости
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('main.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def get_success_url(self):
        post = self.object
        return reverse_lazy('post_details', kwargs={'pk': post.pk})

    # добавление в post запрос наименование категории, в зависимости от того, с какого url его отправляли - news
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


# Представление для изменения поста
class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление для удаления поста.
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_post', )
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


# Представление для изменения поста
class ResponseEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_response', )
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'

    def get_success_url(self):
        response = self.get_object()
        post = response.post
        return reverse_lazy('post_details', kwargs={'pk': post.pk})


# Представление для удаления поста.
class ResponseDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_response', )
    model = Response
    template_name = 'response_delete.html'

    def get_success_url(self):
        response = self.get_object()
        post = response.post
        return reverse_lazy('post_details', kwargs={'pk': post.pk})


@login_required
def response_accept_change(request, pk):
    response = Response.objects.get(id=pk)
    if response.is_accept:
        response.is_accept = False
    else:
        response.is_accept = True
    response.save()
    return redirect('post_details', pk=response.post.id)


# @login_required
# def response_refuse(request, pk):
#     response = Response.objects.get(id=pk)
#     response.is_accept = False
#     response.save()
#     return redirect('post_details', pk=response.post.id)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user__id=self.request.user.id)
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'photo']
    template_name = 'profile_edit.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')