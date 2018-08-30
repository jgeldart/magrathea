from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from .base import COMMON_BLOCKS
from .mixins import ConcordanceEntryMixin, PlanetaryBodyMixin
from ..blocks import OrbitalMechanicsOrbitalCharacteristicsBlock, OrbitalMechanicsRotationalCharacteristicsBlock, PlanetaryBodyPhysicalCharacteristicsBlock

class GasPlanetPage(ConcordanceEntryMixin, PlanetaryBodyMixin, Page):
    """
    A gaseous planetary body. Add as a child page to a star so it picks up the orbital
    mechanical properties.
    """
    body = StreamField(COMMON_BLOCKS + [
        ('orbital_characteristics', OrbitalMechanicsOrbitalCharacteristicsBlock()),
        ('rotational_characteristics', OrbitalMechanicsRotationalCharacteristicsBlock()),
        ('physical_characteristics', PlanetaryBodyPhysicalCharacteristicsBlock()),
    ])

    content_panels = ConcordanceEntryMixin.content_panels + PlanetaryBodyMixin.content_panels
