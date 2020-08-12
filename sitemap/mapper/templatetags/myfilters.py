from django import template

register = template.Library()

@register.filter(name='rangelt1')
def range_value(value):
    return range(value-1)