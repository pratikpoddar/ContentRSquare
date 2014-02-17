from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def crsq_unslugify(s):
    return s.title().replace('-',' ')
