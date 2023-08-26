from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='media/avatar', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Post(models.Model):
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
    CATEGORY_CHOICES = [  # https://www.behance.net/search/images?similarStyleImagesId=311553575   иконки
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

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    headline = models.CharField(max_length=255)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField
    pictures = models.ImageField
    video = models.FileField
    file = models.FileField


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_accept = models.BooleanField(default=False)