from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .filters import PostFilter
from .models import Post
from .forms import PostForm
from datetime import datetime
from pprint import pprint


class PostList(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        pprint(context)
        return context


class PostFilterView(ListView):
    model = Post
    ordering = '-post_time_in'
    filterset_class = PostFilter
    context_object_name = 'post_search'
    template_name = 'post_filter.html'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['curr_date'] = self.request.GET.get('post_time_in__gt')
        context['curr_title'] = self.request.GET.get('post_title__icontains')
        pprint(context)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_item.html'
    context_object_name = 'post_item'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'новость'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'статья'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit_create.html'


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit_create.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')
