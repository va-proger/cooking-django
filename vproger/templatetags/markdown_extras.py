import markdown
from django import template

register = template.Library()

@register.filter
def markdown_filter(text):
    return markdown.markdown(text, extensions=['extra', 'codehilite', 'toc'])
