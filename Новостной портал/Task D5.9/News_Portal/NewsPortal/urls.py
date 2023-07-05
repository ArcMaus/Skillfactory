from django.urls import path
from .views import (
    PostList, PostDetail, PostFilterView, NewsCreate, ArticleCreate,
    NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete, IndexView,
    CategoryList
)
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('profile/', IndexView.as_view(), name='profile'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostFilterView.as_view(), name='post_filter'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    # path('signup/',
    #      BaseRegisterView.as_view(template_name='sign/signup.html'),
    #      name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category_list'),
]

