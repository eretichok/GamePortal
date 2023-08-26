from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Post, Profile, Response
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


# Представление списка публикаций
class PostsList(ListView):
    model = Post
    ordering = '-create_date'
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 6


class ActivityList(ListView):
    model = Post, Response
    ordering = '-date'
    template_name = 'activity.html'
    context_object_name = 'posts', 'response'
    paginate_by = 5


# Представление одиночной публикации
class PostDetails(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'

    # Добавляем в контекст инфу - состоит ли пользователь в группе authors
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request)
        # context['responses'] = self.request.user.groups.filter(name='authors').exists()
        return context


# Представление для создания новости
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('main.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # добавление в post запрос наименование категории, в зависимости от того, с какого url его отправляли - news
    def form_valid(self, form):
        post = form.save(commit=False)
        # post.post_category = 'Новость'
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