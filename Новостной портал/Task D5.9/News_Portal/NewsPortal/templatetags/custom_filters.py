from django import template
import re


register = template.Library()


@register.filter()
def censor_text(post_text):
    bad_words = ['Редиска', 'Хрен', 'Петрушка']

    for word in bad_words:
        pattern = re.compile(word, re.IGNORECASE)
        post_text = pattern.sub('*' * len(word[1:]), post_text)

    return post_text