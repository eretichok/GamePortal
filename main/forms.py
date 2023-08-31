from django import forms
from .models import Post, Profile, Response
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django_ckeditor_5.widgets import CKEditor5Widget


class PostForm(forms.ModelForm):
    # простые проверки до обращения к базе без переопределения метода clean()
    headline = forms.CharField(min_length=3, label='Заголовок')
    # text = forms.CharField(min_length=10, label='Текст публикации', widget=CKEditor5Widget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['text'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['text'].required = True
        # self.fields["text"].required = False

    class Meta:
        model = Post
        fields = ('headline', 'text', 'category')
        label = {'category': 'Категория'}
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }


class ResponseForm(forms.ModelForm):
    text = forms.CharField(min_length=10, label='Текст комментария', widget=forms.Textarea)

    class Meta:
        model = Response
        fields = ('text',)


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
