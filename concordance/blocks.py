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

class OrbitalMechanicsOrbitalCharacteristicsBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(choices=STYLE_CHOICES)

    class Meta:
        template = 'blocks/orbital_mechanics_orbital_characteristics_block.html'

class OrbitalMechanicsRotationalCharacteristicsBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(choices=STYLE_CHOICES)

    class Meta:
        template = 'blocks/orbital_mechanics_rotational_characteristics_block.html'

class PlanetaryBodyPhysicalCharacteristicsBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(choices=STYLE_CHOICES)

    class Meta:
        template = 'blocks/planetary_body_physical_characteristics_block.html'
