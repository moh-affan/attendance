from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(list, key):
    return list[key]
