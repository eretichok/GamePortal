from django_filters import FilterSet, filters
from .models import Response, CATEGORY_CHOICES, Post
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter, ChoiceFilter

# фильтр по объявлениям (выдает все объявления, не разобрался сам как настроить доп фильтрацию по автору поста
class ResponseFilter(FilterSet):
    post = ModelChoiceFilter(
        empty_label='все объявления',
        field_name='post',
        queryset=Post.objects.all(),
        label='Поиск по объявлению',
        lookup_expr='exact',
    )

    class Meta:
        model = Post
        fields = ['post',]
