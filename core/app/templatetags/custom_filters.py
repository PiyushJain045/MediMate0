from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Allows dictionary lookup using a variable in a Django template."""
    return dictionary.get(key)
