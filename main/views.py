from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Profile, Response
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import PostForm, ResponseForm, UserForm, ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .filters import ResponseFilter


# Представление основной страницы - списка объявлений
class PostsList(ListView):
    model = Post
    ordering = '-create_date'
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 6


# Представление страницы с откликами на объявления пользователя
class Activity(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'activity.html'
    context_object_name = 'responses'
    paginate_by = 4

    # фильтрация по объявлениям работает, но не получилось сделать, что бы можно было выбирать
    # только из своих объявлений - показываются все, но при их выборе, естественно,
    # отзывы не автору поста не показываются
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset())
        return context


# Представление одиночного объявления
class PostDetails(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'

    # метод создания отклика на объявление
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        text = request.POST.get('text')
        response = Response(post=post, text=text, user=request.user)
        response.save()
        return redirect('post_details', pk=post.id)

    # Добавляем в контекст отклики на открытое объявление
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.filter(post=self.object)
        return context


# Представление для создания объявления
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('main.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def get_success_url(self):
        post = self.object
        return reverse_lazy('post_details', kwargs={'pk': post.pk})

    # добавление в post запрос user как автора
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        response = super().form_valid(form)
        return response


# Представление для изменения объявления
class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    # метод фиксирует в поле edit_date дату изменения объявления
    def form_valid(self, form):
        post = form.save(commit=False)
        post.edit_date = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('post_details', kwargs={'pk': post.pk})


# Представление для удаления объявления
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_post', )
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


# Представление для изменения отклика
class ResponseEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_response', )
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'

    def get_success_url(self):
        response = self.get_object()
        post = response.post
        return reverse_lazy('post_details', kwargs={'pk': post.pk})

    # уведомляем по почте автора объявления, что пользователь изменил отклик на его объявление
    def form_valid(self, form):
        response = form.save(commit=False)
        subject = f'Пользователь {response.user.username} изменил свое сообщение к Вашему ' \
                  f'объявлению "{response.post.headline}"'

        response = response
        post = response.post
        email = response.post.author.email

        send_mail(
            subject=subject,
            message=render_to_string('mail-response_created_or_changed.html', {'response': response,
                                                                               'post': post}
                                     ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )
        return super().form_valid(form)


# Представление для удаления отклика
class ResponseDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('main.delete_response', )
    model = Response
    template_name = 'response_delete.html'

    def get_success_url(self):
        response = self.get_object()
        post = response.post
        return reverse_lazy('post_details', kwargs={'pk': post.pk})


# Представление для изменения "принятия отклика" автором объявления.
# Отправляется уведомление по почте автору отклика,
# о том что автор объявления принял или отказался от принятия его отклика
@login_required
def response_accept_change(request, pk):
    response = Response.objects.get(id=pk)
    if response.is_accept:
        response.is_accept = False
        subject = f'Автор объявления {response.post.headline} отменил принятие Вашего предложения/'
    else:
        response.is_accept = True
        subject = f'Автор объявления {response.post.headline} принял Ваше предложение.'
    response.save()

    post = response.post
    email = response.user.email
    message = render_to_string('mail-response_is_accepted_changed.html', {'response': response,
                                                                          'post': post}
                               )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )
    return redirect('post_details', pk=response.post.id)


# Представление профиля пользователя
class ProfileView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.get(user__id=self.request.user.id )
        finally:
            return context


# Представление для изменения профиля пользователя
@login_required
def profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    # встраиваем две формы в один шаблон
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
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