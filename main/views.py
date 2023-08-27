from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Profile, Response
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import PostForm, ResponseForm, UserForm, ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from allauth.account.views import SignupView


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


class ProfileView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.get(user__id=self.request.user.id )
        finally:
            return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'photo']
    template_name = 'profile_edit.html'
    # pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')


# class CustomSignupView(SignupView):
#     form_class = CustomSignupForm
#     template_name = 'custom_signup.html'

# class CustomSignup(SignupView):
#     template_name = 'custom_signup.html'
#     form_class = ProfileForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if 'profile_form' not in context:
#             context['profile_form'] = self.get_profile_form()
#         return context
#
#     def form_valid(self, form):
#         user_form = self.get_user_form()
#         if user_form.is_valid() and form.is_valid():
#             # Обработка валидных форм
#             return self.form_valid(form)
#         else:
#             # Обработка невалидных форм
#             return self.form_invalid(form)
#
#     def get_profile_form(self):
#         return Profile.objects.get(user=self.request.user)


@login_required
def profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile_edit.html', context)