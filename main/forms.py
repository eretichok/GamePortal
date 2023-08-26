from django import forms
from .models import Post, Profile, Response
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    # простые проверки до обращения к базе без переопределения метода clean()
    headline = forms.CharField(min_length=3, label='Заголовок')
    text = forms.CharField(min_length=10, label='Текст публикации', widget=forms.Textarea)
    # category = forms.ModelChoiceField(
    #     label='Категория',
    #     queryset=Post.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False, 'required': False}))

    class Meta:
        model = Post
        fields = ('headline', 'text', 'category')
        label = {'category': 'Категория'}


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class ResponseForm(forms.ModelForm):
    text = forms.CharField(min_length=10, label='Текст комментария', widget=forms.Textarea)
    is_accept = forms.BooleanField(label='Предложение принято автором:')

    class Meta:
        model = Response
        fields = ('text', 'is_accept')


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user