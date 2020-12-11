from django import template
register = template.Library()


@register.filter
def get_object_class_name(obj):
    return obj.__class__.__name__
