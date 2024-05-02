from django import template

register = template.Library()

@register.filter(name='custom_get')
def custom_get(dictionary, key):
    return dictionary.get(str(key))
