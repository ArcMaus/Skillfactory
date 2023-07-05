from django.contrib import admin
from .models import Post, Author, PostCategory, Comment, Category, PostSubscribers

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(PostSubscribers)
