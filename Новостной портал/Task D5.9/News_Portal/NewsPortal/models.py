from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_article_rating = Post.objects.filter(post_author_id=self).aggregate(Sum('post_rating')).get('post_rating__sum')
        author_comments_rating = Comment.objects.filter(comment_author_id=self.user).aggregate(Sum('comment_rating')).get('comment_rating__sum')
        all_comments_rating = Comment.objects.filter(comment_post_id__post_author_id=self).aggregate(Sum('comment_rating')).get('comment_rating__sum')
        self.user_rating = int(author_comments_rating or 0) * 3 + int(all_comments_rating or 0) + int(author_article_rating or 0)
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)


article = 'ART'
news = 'NWS'

TYPES = [(article, 'статья'), (news, 'новость')]


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=64, choices=TYPES)
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=64, unique=True)
    post_text = models.TextField(unique=True)
    post_rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])

    def __str__(self):
        return f'{self.post_title}'

    def like_post(self):
        self.post_rating += 1
        self.save()

    def dislike_post(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[0:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like_comment(self):
        self.comment_rating += 1
        self.save()

    def dislike_comment(self):
        self.comment_rating -= 1
        self.save()
