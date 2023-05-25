from django import template

register = template.Library()


@register.filter
def space_separated(value):
    return '{0:,}'.format(value).replace(',', ' ')
