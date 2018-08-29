from wagtail.core import blocks

STYLE_CHOICES = [
    ('default', 'Default'),
    ('muted', 'Muted'),
    ('primary', 'Primary'),
    ('secondary', 'Secondary'),
]

class StarPhysicalCharacteristicsBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(choices=STYLE_CHOICES)

    class Meta:
        template = 'blocks/star_physical_characteristics_block.html'

class StarOrbitalCharacteristicsBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(choices=STYLE_CHOICES)

    class Meta:
        template = 'blocks/star_orbital_characteristics_block.html'
