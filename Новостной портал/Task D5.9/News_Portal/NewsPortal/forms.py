from django import forms
from .models import Post, Category
from django.shortcuts import render
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
           'post_title',
           'post_text',
           'post_author',
           'post_category'
        ]


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

    @login_required
    def subscribe(request, pk):
        user = request.user
        category = Category.objects.get(id=pk)
        category.subscribers.add(user)
        message = "Вы в рассылке категории"
        return render(request, 'subscribe.html', {'category': category, 'message': message})

    @login_required
    def unsubscribe(request, pk):
        user = request.user
        category = Category.objects.get(id=pk)
        category.subscribers.remove(user)
        message = 'Вы отписались от рассылки: '
        return render(request, 'subscribe.html', {'category': category, 'message': message})


# class BaseRegisterForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = ("username",
#                   "first_name",
#                   "last_name",
#                   "email",
#                   "password1",
#                   "password2",)



