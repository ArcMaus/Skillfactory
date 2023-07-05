from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
# from .forms import BaseRegisterForm
from django.urls import reverse_lazy
from .filters import PostFilter
from .models import Post, Category, User
from .forms import PostForm
from datetime import datetime
from pprint import pprint
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'новость'
        html_content = render_to_string('message.html', {'post': post})

        msg = EmailMultiAlternatives(
            subject=post.post_title,
            body=post.post_text[:50],
            from_email='arczed@yandex.ru',
            to=Category.subscribers
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'article_edit_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'статья'
        html_content = render_to_string('message.html', {'post': post})

        msg = EmailMultiAlternatives(
            subject=post.post_title,
            body=post.post_text[:50],
            from_email='arczed@yandex.ru',
            to=Category.subscribers
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit_create.html'


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
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


# class BaseRegisterView(CreateView):
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class CategoryList(ListView):
    model = Post
    ordering = '-post_time_in'
    context_object_name = 'post'
    template_name = 'post_category.html'
    paginate_by = 10

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-post_time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_subscribers"] = self.request.user not in self.post_category.subscribers.all()
        context['category'] = self.post_category
        return context
