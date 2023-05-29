from django import template


register = template.Library()


bad_words = ['Музей', 'Музея', 'Музею', 'Музеем', 'Бензол', 'Бензола', 'Бензолу', 'Бензолом', 'Дзадзики', 'Дзадзики?']


@register.filter()
def censor(word):
    if isinstance(word, str):
        for i in word.split():
            if i.capitalize() in bad_words:
                word = word.replace(i, i[0] + '*' * len(i))
    else:
        raise ValueError('custom_filters -> censor -> A string is expected, but a different data type has been entered')
    return word
