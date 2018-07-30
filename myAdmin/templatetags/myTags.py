from django import template

register = template.Library()

@register.simple_tag
def mul(x, y):
    a = x * y
    a = float(a)
    return '%.2f' % a
