from .base import BaseCharacteristicsBlock

class OrbitalMechanicsOrbitalCharacteristicsBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/orbital_mechanics_orbital_characteristics_block.html'

class OrbitalMechanicsRotationalCharacteristicsBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/orbital_mechanics_rotational_characteristics_block.html'
