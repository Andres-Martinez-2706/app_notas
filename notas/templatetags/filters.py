from django import template
import re

register = template.Library()

@register.filter(name='remove_images')
def remove_images(value):
    return re.sub(r'<img[^>]*>', '', value)
