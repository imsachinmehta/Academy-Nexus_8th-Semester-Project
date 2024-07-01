from django import template 

register = template.Library()

@register.filter(name='filename')
def filename(value):
    return value.split('/')[-1]