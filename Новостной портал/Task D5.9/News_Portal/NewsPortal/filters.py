from django_filters import FilterSet
from .models import Post
from django.forms import SelectDateWidget


class PostFilter(FilterSet):
    class Meta:
       model = Post
       fields = {
           'post_title': ['icontains'],
           'post_author__user__username': ['exact'],
           'post_time_in': ['gt'],
       }
       widget = SelectDateWidget(
           empty_label=('Choose Day', 'Choose Month', 'Choose Year')
       )