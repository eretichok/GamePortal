from django import forms
from .models import Post, Profile, Response
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


class PostForm(forms.ModelForm):
    # простые проверки до обращения к базе без переопределения метода clean()
    headline = forms.CharField(min_length=3, label='Заголовок')
    text = forms.CharField(min_length=10, label='Текст публикации', widget=CKEditorWidget())
    attachments_file = MultiFileField(label='Файл', min_num=0, max_num=3, max_file_size=1024 * 1024 * 5)
    attachments_video = MultiMediaField(
        label='Аудио/видео',
        min_num=0,
        max_num=3,
        max_file_size=1024 * 1024 * 5,
        media_type='video'  # 'audio', 'video' or 'image'
    )
    attachments_image = MultiImageField(label='Картинка', min_num=0, max_num=3, max_file_size=1024 * 1024 * 5)

    class Meta:
        model = Post
        fields = ('headline', 'text', 'attachments_image', 'attachments_video', 'attachments_file', 'category')
        label = {'category': 'Категория'}


class ResponseForm(forms.ModelForm):
    text = forms.CharField(min_length=10, label='Текст комментария', widget=forms.Textarea)
    # is_accept = forms.BooleanField(label='Предложение принято автором:')

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
