# from django import template
#
#
# register = template.Library()
#
#
# # Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# # что это именно фильтр для шаблонов, а не простая функция.
# @register.filter()
# def currency(value):
#    """
#    value: значение, к которому нужно применить фильтр
#    """
#    # Возвращаемое функцией значение подставится в шаблон.
#    return f'{value} Р'


from django import template


register = template.Library()

cens = ['Редиска', 'Дурак', 'Плохой']


@register.filter()
def censor(word):
    if isinstance(word, str):
        for i in word.split():
            if i.capitalize() in cens:
                word = word.replace(i, i[0] + '*' * len(i))
    else:
        raise ValueError('custom_filters -> censor -> A string is expected, but a different data type has been entered')
    return word