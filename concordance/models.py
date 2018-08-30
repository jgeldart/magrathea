from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, PageChooserPanel, RichTextFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image

from quantity_field import ureg
from quantity_field.fields import MultiQuantityField
Q_ = ureg.Quantity

from .blocks import StarPhysicalCharacteristicsBlock, StarOrbitalCharacteristicsBlock, OrbitalMechanicsOrbitalCharacteristicsBlock, OrbitalMechanicsRotationalCharacteristicsBlock, PlanetaryBodyPhysicalCharacteristicsBlock

import math

COMMON_BLOCKS = [
    ('heading', blocks.CharBlock(classname="full title")),
    ('paragraph', blocks.RichTextBlock(template="blocks/rich_text_block.html")),
    ('image', ImageChooserBlock()),
]

class ConcordanceEntryMixin(models.Model):
    """
    A mixin for any page that should have common concordance fields.
    """

    subtitle = models.TextField(blank=True)

    lead = RichTextField(blank=True)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField(COMMON_BLOCKS)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        ImageChooserPanel('hero_image'),
        RichTextFieldPanel('lead'),
        StreamFieldPanel('body'),
    ]

    class Meta:
        abstract = True

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

    content_panels = ConcordanceEntryMixin.content_panels + [
        FieldPanel('mass'),
    ]

GRAVITATIONAL_CONSTANT = Q_('6.67408e-11 * m**3 * kg**-1 * s**-2')

class OrbitalMechanicsMixin(models.Model):
    """
    A mixin for anything that orbits something else (e.g. a planet or a moon).

    This mixin assumes its direct parent has mass.
    """

    semi_major_axis = MultiQuantityField(units=(ureg.au, ureg.km))
    eccentricity = models.DecimalField(max_digits=5, decimal_places=5)
    inclination = MultiQuantityField(units=(ureg.degree, ureg.radian))
    longitude_of_the_ascending_node = MultiQuantityField(units=(ureg.degree, ureg.radian))
    argument_of_periapsis = MultiQuantityField(units=(ureg.degree, ureg.radian))

    # Local motion
    rotational_period = MultiQuantityField(units=(ureg.hour, ureg.day))
    obliquity = MultiQuantityField(units=(ureg.degree, ureg.radian))
    precessional_period = MultiQuantityField(units=(ureg.year,))

    @property
    def orbited_object(self):
        return self.get_parent().specific

    @property
    def periapsis(self):
        return self.semi_major_axis * (1 - float(self.eccentricity))

    @property
    def apoapsis(self):
        return self.semi_major_axis * (1+ float(self.eccentricity))

    @property
    def orbital_period(self):
        return (((4 * math.pi**2) / (GRAVITATIONAL_CONSTANT * self.orbited_object.mass)) * self.semi_major_axis**3)**0.5

    @property
    def day_length(self):
        return self.rotational_period

    @property
    def local_days_in_year(self):
        return self.orbital_period / self.rotational_period

    @property
    def tropics(self):
        return self.obliquity

    @property
    def polar_circles(self):
        return Q_('90 degree') - self.obliquity

    content_panels = [
        FieldRowPanel([
            FieldPanel('semi_major_axis'),
            FieldPanel('eccentricity'),
        ]),
        FieldRowPanel([
            FieldPanel('inclination'),
            FieldPanel('longitude_of_the_ascending_node'),
            FieldPanel('argument_of_periapsis'),
        ]),
        FieldRowPanel([
            FieldPanel('rotational_period'),
            FieldPanel('obliquity'),
            FieldPanel('precessional_period'),
        ]),
    ]

    class Meta:
        abstract = True

class PlanetaryBodyMixin(OrbitalMechanicsMixin):
    """
    A mixin for planetary bodies, with properties like density and gravity.

    Note: moons are a form of planetary body too!
    """

    mass = MultiQuantityField(units=(ureg.earth_mass, ureg.jovian_mass, ureg.kilogram))
    radius = MultiQuantityField(units=(ureg.earth_radius, ureg.jovian_radius, ureg.km, ureg.mile, ureg.m))

    @property
    def mass_is_jovian(self):
        return self.mass.to("jovian_mass").magnitude > 0.1

    @property
    def mass_is_terran(self):
        return self.mass.to("earth_mass").magnitude > 0.001

    @property
    def radius_is_jovian(self):
        return self.radius.to("jovian_radius").magnitude > 0.1

    @property
    def radius_is_terran(self):
        return self.radius.to("earth_radius").magnitude > 0.001

    @property
    def surface_gravity(self):
        return GRAVITATIONAL_CONSTANT * self.mass / self.radius**2

    @property
    def density(self):
        return self.mass / ((4/3) * math.pi * self.radius**3)

    @property
    def escape_velocity(self):
        return (2 * GRAVITATIONAL_CONSTANT * self.mass / self.radius)**0.5

    @property
    def mean_surface_temperature(self):
        return self.orbited_object.luminosity**0.25 / self.semi_major_axis**2

    @property
    def solar_constant(self):
        return self.orbited_object.luminosity / self.semi_major_axis ** 2

    content_panels = [
        FieldRowPanel([
            FieldPanel('mass'),
            FieldPanel('radius'),
        ]),
    ] + OrbitalMechanicsMixin.content_panels

    class Meta:
        abstract = True

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
