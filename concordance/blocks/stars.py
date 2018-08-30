from .base import BaseCharacteristicsBlock

class StarPhysicalCharacteristicsBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/star_physical_characteristics_block.html'

class StarOrbitalCharacteristicsBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/star_orbital_characteristics_block.html'
