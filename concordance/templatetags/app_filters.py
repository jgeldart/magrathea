from django import template
from django.utils.html import escapejs
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter('short_quantity')
def short_quantity(value, arg=None):
    spec = '{:~H}'
    if arg is not None:
        spec = '{:' + arg + '~H}'
    return spec.format(value)

@register.filter('quantity_convert')
def quantity_convert(value, arg):
    return value.to(arg)

@register.filter('quantity_magnitude')
def quantity_magnitude(value):
    return value.magnitude

@register.filter('scientific_notation')
def scientific_notation(value, arg=None):
    if arg is None:
        arg = 3
    spec = '{{:.{0}E}}'.format(arg)
    formatted_value = spec.format(value)
    mantissa, exponent = formatted_value.split('E')
    return '{0} × 10<sup>{1}</sup>'.format(mantissa, int(exponent))

@register.filter('json_script')
def json_script(value, arg):
    json_dump = (json.dumps(value))
    return mark_safe('<script id="{0}" type="application/json">{1}</script>'.format(arg, json_dump))

@register.filter('dashreplace')
def dash_replace(value, arg):
    return value.replace('-', arg)

@register.filter('jsondump')
def json_dump(value):
    return mark_safe(json.dumps(value))
