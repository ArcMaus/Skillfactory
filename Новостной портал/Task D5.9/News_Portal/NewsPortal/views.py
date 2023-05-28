from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime
from pprint import pprint


class PostList(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['news_counter'] = None
        pprint(context)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_item.html'
    context_object_name = 'post_item'
