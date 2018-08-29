from django import template

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
