from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel

from quantity_field import ureg
from quantity_field.fields import MultiQuantityField
Q_ = ureg.Quantity

from .base import COMMON_BLOCKS
from .planetary_bodies import GasPlanetPage
from .mixins import ConcordanceEntryMixin
from ..blocks import StarPhysicalCharacteristicsBlock, StarOrbitalCharacteristicsBlock, OrbitalMechanicsOrbiterBlock

import math

class StarPage(ConcordanceEntryMixin, Page):
    """
    A star is born. Most of the properties for the star are derived from its
    mass.

    Note, we currently assume habitable systems we want to create have a single
    star in them. Bodies that orbit are created under the star as subpages.
    """

    body = StreamField(COMMON_BLOCKS + [
        ('physical_characteristics', StarPhysicalCharacteristicsBlock()),
        ('orbital_characteristics', StarOrbitalCharacteristicsBlock()),
        ('orbiters', OrbitalMechanicsOrbiterBlock()),
    ])
    mass = MultiQuantityField(units=(ureg.solar_mass, ureg.kilogram))

    @property
    def radius(self):
        return Q_('1 solar_radius / solar_mass**0.8') * self.mass ** 0.8

    @property
    def luminosity(self):
        return Q_('1 solar_luminosity / solar_mass**3.5') * self.mass ** 3.5

    @property
    def stellar_lifetime(self):
        return Q_('1 solar_lifetime / solar_mass**-2.5') * self.mass ** -2.5

    @property
    def surface_temperature(self):
        return Q_('1 solar_surface_temperature * solar_radius**0.5 / solar_luminosity**0.25') * (self.luminosity/self.radius**2)**0.25

    @property
    def spectral_class(self):
        def spectral_subclass(mass, class_max, class_min):
            return str(round(10* (1 - (mass-class_min)/(class_max-class_min)), 1))
        solar_masses = self.mass.to('solar_mass').magnitude
        if solar_masses >= 16:
            return 'O'
        elif solar_masses >= 2.1:
            return 'B' + spectral_subclass(solar_masses, 16, 2.1)
        elif solar_masses >=1.4:
            return 'A' + spectral_subclass(solar_masses, 2.1, 1.4)
        elif solar_masses >= 1.04:
            return 'F' + spectral_subclass(solar_masses, 1.4, 1.04)
        elif solar_masses >= 0.8:
            return 'G' + spectral_subclass(solar_masses, 1.04, 0.8)
        elif solar_masses >= 0.45:
            return 'K' + spectral_subclass(solar_masses, 0.8, 0.45)
        elif solar_masses >= 0.08:
            return 'M' + spectral_subclass(solar_masses, 0.45, 0.08)
        else:
            return 'L'

    @property
    def habitable_zone_inner(self):
        return Q_('1 au / solar_luminosity**0.5') * (self.luminosity / 1.1)**0.5

    @property
    def habitable_zone_outer(self):
        return Q_('1 au / solar_luminosity**0.5') * (self.luminosity / 0.53)**0.5

    @property
    def system_boundary_inner(self):
        return Q_('0.1 au / solar_mass') * self.mass

    @property
    def system_boundary_outer(self):
        return Q_('40 au / solar_mass') * self.mass

    @property
    def frost_line(self):
        return Q_('4.85 au / solar_luminosity**0.5') * self.luminosity**0.5

    @property
    def schwarzchild_radius(self):
        return Q_('1 solar_radius / solar_mass') * self.mass * 2.95

    @property
    def white_dwarf_radius(self):
        return Q_('1 solar_radius / solar_mass**-0.333333') * self.mass**-0.333333

    @property
    def colour(self):
        """
        Converts from K to RGB, algorithm courtesy of
        http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/

        Code from https://gist.github.com/petrklus/b1f427accdf7438606a6
        """
        colour_temperature = self.surface_temperature.to("kelvin").magnitude

        #range check
        if colour_temperature < 1000:
            colour_temperature = 1000
        elif colour_temperature > 40000:
            colour_temperature = 40000

        tmp_internal = colour_temperature / 100.0

        # red
        if tmp_internal <= 66:
            red = 255
        else:
            tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
            if tmp_red < 0:
                red = 0
            elif tmp_red > 255:
                red = 255
            else:
                red = tmp_red

        # green
        if tmp_internal <=66:
            tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
            if tmp_green < 0:
                green = 0
            elif tmp_green > 255:
                green = 255
            else:
                green = tmp_green
        else:
            tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
            if tmp_green < 0:
                green = 0
            elif tmp_green > 255:
                green = 255
            else:
                green = tmp_green

        # blue
        if tmp_internal >=66:
            blue = 255
        elif tmp_internal <= 19:
            blue = 0
        else:
            tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
            if tmp_blue < 0:
                blue = 0
            elif tmp_blue > 255:
                blue = 255
            else:
                blue = tmp_blue

        return red, green, blue

    @property
    def to_orrery(self):
        """
        Create a dict containing the orrery settings.

        TODO: This should be moved to a view.
        """
        r,g,b = self.colour
        return {
            'title': self.title,
            'name': self.slug.replace('-', '_'),
            'mass': self.mass.to(ureg.kg).magnitude,
            'radius': self.radius.to(ureg.km).magnitude,
            'color': '#{0}{1}{2}'.format(format(int(r), '02x'),format(int(g), '02x'), format(int(b), '02x')),
            # 'map': '/static/img/sunmap.jpg',
            'k': 0.01720209895,
        }

    @property
    def to_orrery_scenario(self):
        child_planets = self.get_descendants().type(GasPlanetPage).all()
        scenario_objects = [self.to_orrery] + [ p.specific.to_orrery for p in child_planets ]
        bodies = {}
        for p in scenario_objects:
            bodies[p['name']] = p

        return {
            'name': '{0}-star-system'.format(self.slug).replace('-', '_'),
            'title': '{0} star system'.format(self.title),
            'bodies': bodies,
            'secondsPerTick': {
                'min': 60,
                'max': 3600 * 15,
                'initial': 3600
            },
            'defaultGuiSettings': {
                'playing': False,
                'planetScale': 10
            },
            'help':''
        }

    content_panels = ConcordanceEntryMixin.content_panels + [
        FieldPanel('mass'),
    ]
