from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from quantity_field import ureg
from quantity_field.fields import MultiQuantityField
Q_ = ureg.Quantity

COMMON_BLOCKS = [
    ('heading', blocks.CharBlock(classname="full title")),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
]

class ConcordanceEntryMixin(models.Model):
    """
    A mixin for any page that should have common concordance fields.
    """

    body = StreamField(COMMON_BLOCKS)

    content_panels = Page.content_panels + [
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

    content_panels = ConcordanceEntryMixin.content_panels + [
        FieldPanel('mass'),
    ]
