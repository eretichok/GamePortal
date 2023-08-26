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
    template_name = 'default.html'
    context_object_name = 'posts'
    paginate_by = 5