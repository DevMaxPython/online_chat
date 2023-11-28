from django import template

register = template.Library()

@register.filter
def insert_linebreaks(value, chars_per_line=30):
    return '<br>'.join(value[i:i + chars_per_line] for i in range(0, len(value), chars_per_line))
