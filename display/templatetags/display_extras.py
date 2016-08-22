from django import template

register = template.Library()

@register.filter
def convert(value):
    """
    A template filter to convert integers into a template-friendly representation.

    Args:
        value: The variable passed in from the template

    Returns:
        A character to help a map read as more "maplike". We may eventually change this to return a CSS class or
        something more appropriate for our front-end, rather than the ASCII things we do right now.
    """

    charmap = {
            0: 'block0',  # Undug spaces. Stone, earth, whatever.
            1: 'open',  # Excavated spaces. Generally clear to move through.
    }

    return charmap.get(value, '?')  # There's no exception handling, so return a safe default if not found
