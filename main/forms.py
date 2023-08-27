from django import forms
from .models import Post, Profile, Response
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    # простые проверки до обращения к базе без переопределения метода clean()
    headline = forms.CharField(min_length=3, label='Заголовок')
    text = forms.CharField(min_length=10, label='Текст публикации', widget=forms.Textarea)
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False, 'required': False}))

    class Meta:
        model = Post
        fields = ('headline', 'text', 'category')
        label = {'category': 'Категория'}


class ResponseForm(forms.ModelForm):
    text = forms.CharField(min_length=10, label='Текст комментария', widget=forms.Textarea)
    # is_accept = forms.BooleanField(label='Предложение принято автором:')

    class Meta:
        model = Response
        fields = ('text',)


# class CustomSignupForm(SignupForm):
#     date_of_birth = forms.DateField(required=False)
#     photo = forms.ImageField(required=False)
#
#     class Meta:
#
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
#
#     def custom_signup(self, request, user):
#         profile = Profile(user=user,
#                           date_of_birth=self.cleaned_data['date_of_birth'],
#                           photo=self.cleaned_data['photo']
#                           )
#         profile.save()
#
#     def save(self, request):
#         user = super().save(request)
#         self.custom_signup(request, user)
#         return user

# class CustomSignupForm(SignupForm):
#     email = forms.EmailField(label="Email", required=True)
#     username = forms.CharField(max_length=30, label="Имя пользователя", required=False)
#     last_name = forms.CharField(max_length=30, label="Имя", required=False)
#     last_name = forms.CharField(max_length=30, label="Фамилия", required=False)
#     date_of_birth = forms.DateField(required=False)
#     photo = forms.ImageField(required=False)
#
#     class Meta:
#         model = User
#         fields = ("username",
#                   "first_name",
#                   "last_name",
#                   "email",
#                   "password1",
#                   "password2",)
#
#     def custom_signup(self, request, user):
#         profile = Profile(user=user,
#                           date_of_birth=self.cleaned_data['date_of_birth'],
#                           photo=self.cleaned_data['photo']
#                           )
#         profile.save()
#
#     def save(self, request):
#         user = super(CustomSignupForm, self).save(request)
#         self.custom_signup(request, user)
#         return user

class CustomSignupForm(SignupForm):

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']