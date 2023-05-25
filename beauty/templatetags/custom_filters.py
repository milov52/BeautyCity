from django import template

register = template.Library()


@register.filter
def space_separated(value):
    return '{0:,}'.format(value).replace(',', ' ')


@register.filter
def shorten_name(value):
    return f'{value[:1]}.'
