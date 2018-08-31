from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from quantity_field import ureg
Q_ = ureg.Quantity

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

    @property
    def to_orrery(self):
        """
        Create a dict containing the orrery settings.

        TODO: This should be moved to a view.
        """
        return {
            'title': self.title,
            'name': self.slug.replace('-', '_'),
            'mass': self.mass.to("kg").magnitude,
            'radius': self.radius.to("km").magnitude,
            'color': '#ff9932',
            'map': '/static/img/jupitermap.jpg',
            'siderealDay': self.rotational_period.to("second").magnitude,
            'tilt': self.obliquity.to("degree").magnitude,
            'relativeTo': self.orbited_object.slug.replace('-', '_'),
            'orbit': {
                'base': {
                    'a': self.semi_major_axis.to("km").magnitude,
                    'e': float(self.eccentricity),
                    'i': self.inclination.to("degree").magnitude,
                    'l': 0,
                    'lp': self.longitude_of_periapsis.to("degree").magnitude,
                    'o': self.longitude_of_the_ascending_node.to("degree").magnitude
                },
                'day': {
                    'a': 0,
                    'e': 0,
                    'i': 0,
                    'l': 360/self.orbital_period.to("year").magnitude/Q_(1, ureg.year).to("day").magnitude,
                    'lp': 0,
                    'o': 0
                }
            }
        }


    content_panels = ConcordanceEntryMixin.content_panels + PlanetaryBodyMixin.content_panels
