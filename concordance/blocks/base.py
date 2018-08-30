from wagtail.core import blocks

STYLE_CHOICES = [
    ('default', 'Default'),
    ('muted', 'Muted'),
    ('primary', 'Primary'),
    ('secondary', 'Secondary'),
]

class BaseCharacteristicsBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(choices=STYLE_CHOICES, default='default')
