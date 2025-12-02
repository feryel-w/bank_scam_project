from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    # Only apply if it's a BoundField
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css})
    return field  # return as-is if not a form field
