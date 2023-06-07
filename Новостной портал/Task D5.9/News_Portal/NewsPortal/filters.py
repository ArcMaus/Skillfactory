from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Author, User
from django.forms import SelectDateWidget


class PostFilter(FilterSet):
    author = ModelChoiceFilter(field_name='post_author', queryset=Author.objects.all(), label='Автор', empty_label='Любой')
    class Meta:
       model = Post
       fields = {
           'post_title': ['icontains'],
           'post_author': ['exact'],
           'post_time_in': ['gt'],
       }
       widget = SelectDateWidget(
           empty_label=('Choose Day', 'Choose Month', 'Choose Year')
       )