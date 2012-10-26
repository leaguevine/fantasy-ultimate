from django import template
from django.conf import settings
from django.template import Node, TemplateSyntaxError
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.inclusion_tag('includes/google_analytics.html')
def google_analytics():
    return {'analytics_enabled': settings.ANALYTICS_ENABLED}


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


#
# http://djangosnippets.org/snippets/779/
#
class RangeNode(Node):
    def __init__(self, num, context_name):
        self.num, self.context_name = num, context_name
    def render(self, context):
        context[self.context_name] = range(int(self.num))
        return ""


@register.tag
def num_range(parser, token):
    """
    Takes a number and iterates and returns a range (list) that can be
    iterated through in templates

    Syntax:
    {% num_range 5 as some_range %}

    {% for i in some_range %}
      {{ i }}: Something I want to repeat\n
    {% endfor %}

    Produces:
    0: Something I want to repeat
    1: Something I want to repeat
    2: Something I want to repeat
    3: Something I want to repeat
    4: Something I want to repeat
    """
    try:
        fnctn, num, trash, context_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, "%s takes the syntax %s number_to_iterate\
            as context_variable" % (fnctn, fnctn)
    if not trash == 'as':
        raise TemplateSyntaxError, "%s takes the syntax %s number_to_iterate\
            as context_variable" % (fnctn, fnctn)
    return RangeNode(num, context_name)
