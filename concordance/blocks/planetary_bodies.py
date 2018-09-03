from .base import BaseCharacteristicsBlock

class PlanetaryBodyPhysicalCharacteristicsBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/planetary_body_physical_characteristics_block.html'

class PlanetaryBodySeasonalCharacteristicsBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/planetary_body_seasonal_characteristics_block.html'

class PlanetaryBodySkySimulationBlock(BaseCharacteristicsBlock):
    class Meta:
        template = 'blocks/planetary_body_sky_simulation_block.html'
