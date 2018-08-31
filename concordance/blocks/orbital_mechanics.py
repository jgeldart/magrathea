from wagtail.core import blocks
from .base import BaseCharacteristicsBlock, STYLE_CHOICES

class OrbitalMechanicsOrbitalCharacteristicsBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/orbital_mechanics_orbital_characteristics_block.html'

class OrbitalMechanicsRotationalCharacteristicsBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/orbital_mechanics_rotational_characteristics_block.html'

class OrbitalMechanicsOrbiterBlock(blocks.StructBlock):
    """
    Shows a grid of the selected objects, with an optional button to open an
    orrery as a modal
    """

    title = blocks.CharBlock()

    style = blocks.ChoiceBlock(choices=STYLE_CHOICES, default='default')

    orbiters = blocks.ListBlock(blocks.PageChooserBlock(target_model=('concordance.PlanetPage',)))

    show_orrery = blocks.BooleanBlock(required=False)

    class Meta:
        template = 'blocks/orbital_mechanics_orbiter_block.html'
