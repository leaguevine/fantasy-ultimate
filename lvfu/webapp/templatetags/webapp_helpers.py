from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def fix_json(value):
    """
    Does a simple fix for including tags in JSON.
    Not really robust, but it fixes the one problem that causes a major break
    (including a </script> tag in a description) with limited possibility that
    we would end up corrupting the JSON.
    """
    return value.replace("</", "&lt;/")
