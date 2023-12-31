from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# два дополнительных связанных с user поля для профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='media/avatar', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

TANK = "TA"
HEALER = "HE"
DAMAGEDEALER = "DD"
TRADER = "TR"
GUILDMASTER = "GM"
QUESTGIVER = "QG"
BLACKSMITH = "BS"
TANNER = "TN"
ZELEVAR = "ZE"
SPELLMASTER = "SM"
CATEGORY_CHOICES = [  # https://www.behance.net/search/images?similarStyleImagesId=311553575 иконки
    (TANK, "Танки"),
    (HEALER, "Хилы"),
    (DAMAGEDEALER, "ДД"),
    (TRADER, "Торговцы"),
    (GUILDMASTER, "Гилдмастеры"),
    (QUESTGIVER, "Квестгиверы"),
    (BLACKSMITH, "Кузнецы"),
    (TANNER, "Кожевники"),
    (ZELEVAR, "Зельевары"),
    (SPELLMASTER, "Мастера заклинаний"),
]


# модель объявления
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    headline = models.CharField(max_length=255)
    text = RichTextUploadingField('Text', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.headline


# модель отклика на объявление
class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_accept = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})