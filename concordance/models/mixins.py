from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, RichTextFieldPanel, FieldRowPanel
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel

from quantity_field import ureg
from quantity_field.fields import MultiQuantityField
Q_ = ureg.Quantity

from .base import COMMON_BLOCKS, GRAVITATIONAL_CONSTANT

import math

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
