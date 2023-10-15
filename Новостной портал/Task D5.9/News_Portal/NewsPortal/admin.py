from django.contrib import admin
from .models import Post, Author, PostCategory, Comment, Category, PostSubscribers
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = [field.name for field in Post._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения
    list_filter = ('post_title', 'post_author', 'post_rating')
    search_fields = ('post_title', 'post_author, post_category__category_name') # тут всё очень похоже на фильтры из запросов в базу

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(PostSubscribers)

