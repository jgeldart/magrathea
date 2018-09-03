from django.db import models
from django.forms import widgets

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from modelcluster.fields import ParentalKey

from quantity_field import ureg
from quantity_field.fields import MultiQuantityField
Q_ = ureg.Quantity

from .base import COMMON_BLOCKS
from .mixins import ConcordanceEntryMixin, PlanetaryBodyMixin
from ..blocks import OrbitalMechanicsOrbitalCharacteristicsBlock, OrbitalMechanicsRotationalCharacteristicsBlock, PlanetaryBodyPhysicalCharacteristicsBlock, PlanetaryBodySeasonalCharacteristicsBlock, PlanetaryBodySkySimulationBlock

AVOGADRO_CONSTANT = Q_(6.022140857e23, ureg.mol**-1)
GAS_CONSTANT = Q_(8.3144598, ureg.joule * ureg.mol**-1 * ureg.kelvin**-1)

import math

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

class PercentageField(models.FloatField):
    widget = widgets.TextInput(attrs={"class": "percentInput"})

    def to_python(self, value):
        val = super(PercentageField, self).to_python(value)
        if is_number(val):
            return val*100
        return val

    def prepare_value(self, value):
        val = super(PercentageField, self).prepare_value(value)
        if is_number(val) and not isinstance(val, str):
            return str((float(val)/100))
        return val

@register_snippet
class AtmosphericGas(models.Model):
    """
    A gas that can live in the atmosphere of a planet or moon.

    Some examples:

    | Name                      | Molar weight (kg/mol) | Refractive index      |
    |---------------------------|-----------------------|-----------------------|
    | Atomic Hydrogen           | 0.00100794            | N/A                   |
    | Molecular Hydrogen        | 0.00201588            | 1.000132              |
    | Helium                    | 0.0040026             | 1.000035              |
    | Atomic Nitrogen           | 0.0140067             | N/A                   |
    | Atomic Oxygen             | 0.015999              | N/A                   |
    | Methane                   | 0.01604               | 1.00043650            |
    | Ammonia                   | 0.017031              | 1.00037375            |
    | Water Vapour              | 0.01801528            | 1.000256              |
    | Neon                      | 0.0201797             | 1.000067              |
    | Molecular Nitrogen        | 0.0280134             | 1.000298              |
    | Carbon Monoxide           | 0.02801               | 1.000338              |
    | Nitric Oxide              | 0.03001               | 1.000297              |
    | Molecular Oxygen          | 0.031988              | 1.000271              |
    | Methanol                  | 0.0320419             | 1.000586              |
    | Hydrogen Sulphide         | 0.0341                | 1.000634              |
    | Hydrochloric Acid         | 0.0364609             | 1.000447              |
    | Fluorine                  | 0.0379968             | N/A                   |
    | Argon                     | 0.039948              | 1.000281              |
    | Carbon Dioxide            | 0.04401               | 1.000449              |
    | Nitrous Oxide             | 0.044013              | 1.000516              |
    | Nitrogen Dioxide          | 0.0460055             | 1.449                 |
    | Ethanol                   | 0.0460684             | 1.000878              |
    | Ozone                     | 0.048                 | 1.00052               |
    | Acetone                   | 0.0580791             | 1.001090              |
    | Sulphur Dioxide           | 0.064066              | 1.000686              |
    | Chlorine                  | 0.070906              | 1.000773              |
    | Pentane                   | 0.0721488             | 1.001711              |
    | Ethyl Ether               | 0.0741216             | 1.001533              |
    | Carbon Disulphide         | 0.0761407             | 1.001481              |
    | Benzene                   | 0.0781118             | 1.001762              |
    | Sulphur Trioxide          | 0.080066              | N/A                   |
    | Krypton                   | 0.083798              | 1.000427              |
    | Chloroform                | 0.1193776             | 1.001450              |
    | Xenon                     | 0.131293              | 1.000702              |
    | Sulphur Hexafluoride      | 0.1460554             | 1.00072627            |
    | Bromine                   | 0.159808              | 1.001132              |
    """

    name = models.CharField(max_length=160)
    short_name = models.CharField(max_length=32, blank=True)

    molar_weight = MultiQuantityField(units=(ureg.kg*ureg.mol**-1, ureg.g*ureg.mol**-1))

    refractive_index = models.FloatField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('short_name'),
        FieldPanel('molar_weight'),
        FieldPanel('refractive_index'),
    ]

    def __str__(self):
        return self.name

class AtmosphericComponent(Orderable, models.Model):

    planetary_body = ParentalKey('concordance.PlanetPage', on_delete=models.CASCADE, related_name='atmospheric_components')
    atmospheric_gas = models.ForeignKey('concordance.AtmosphericGas', on_delete=models.CASCADE, related_name='+')

    percentage = models.FloatField()

    @property
    def partial_pressure(self):
        """
        The partial pressure of this gas, as a component of the atmosphere.
        """
        return self.percentage * self.planetary_body.surface_pressure

    class Meta:
        verbose_name = "atmospheric component"
        verbose_name_plural = "atmospheric components"

    panels = [
        FieldRowPanel([
                SnippetChooserPanel('atmospheric_gas'),
                FieldPanel('percentage'),
            ])
    ]

    def __str__(self):
        return self.planetary_body.title + " -> " + self.atmospheric_gas.name + " (" + str(self.percentage * 100) + "%)"

class PlanetPage(ConcordanceEntryMixin, PlanetaryBodyMixin, Page):
    """
    A planetary body. Add as a child page to a star so it picks up the orbital
    mechanical properties.
    """
    body = StreamField(COMMON_BLOCKS + [
        ('orbital_characteristics', OrbitalMechanicsOrbitalCharacteristicsBlock()),
        ('rotational_characteristics', OrbitalMechanicsRotationalCharacteristicsBlock()),
        ('physical_characteristics', PlanetaryBodyPhysicalCharacteristicsBlock()),
        ('seasonal_characteristics', PlanetaryBodySeasonalCharacteristicsBlock()),
        ('sky_simulation', PlanetaryBodySkySimulationBlock()),
    ])

    # Atmospheric modelling
    surface_pressure = MultiQuantityField(default=0, units=(ureg.atm, ureg.pascal, ureg.bar))

    @property
    def refractive_index(self):
        """
        Calculate the refractive index of this atmosphere based on the
        component gasses and their proportions.
        """
        return sum(atmospheric_component.percentage/100 * atmospheric_component.atmospheric_gas.refractive_index for atmospheric_component in self.atmospheric_components.all())

    @property
    def scale_height(self):
        """
        Calculate the scale height for this atmosphere.
        """
        return (GAS_CONSTANT * self.mean_surface_temperature)/(self.atmospheric_weight * self.surface_gravity)

    def atmospheric_density(self, height):
        """
        Give the density of the atmosphere at a given height.
        """
        return (self.atmospheric_pressure(height) * self.atmospheric_weight)/(GAS_CONSTANT * self.mean_surface_temperature)

    def atmospheric_pressure(self, height):
        """
        Give the pressure of the atmosphere at a given height.
        """
        return self.surface_pressure * math.exp(-height/self.scale_height)

    @property
    def atmospheric_depth(self):
        """
        Give a (slightly arbitrary) measure of the depth of the atmosphere.

        This is based on the height at which its pressure is the same as that
        of Earth's at 100km (that pressure, Ps below ~ 6E-6 atm)

        P = P0 * Exp(- h/H)
        h = -H * ln(Ps/P0)
        """
        return -self.scale_height * math.log(Q_(6E-6, ureg.atm) / self.surface_pressure)

    def molecular_number_density(self, height):
        """
        The number of molecules per unit volume at a given height.
        """
        return AVOGADRO_CONSTANT * self.atmospheric_density(height) / self.atmospheric_weight

    @property
    def surface_molecular_number_density(self):
        return self.molecular_number_density(Q_(0, ureg.m))

    def rayleigh_scattering_coefficient(self, wavelength):
        """
        Return the scattering coefficient for a particular wavelength of light,
        based on the physical properties of the atmosphere and assuming one is
        standing at sea level.

        n = refractive_index
        N = molecular number density (units = 1*m**-3)

        (8 * math.pi**3 * (n**2 - 1)**2)/3 * 1/N * 1/wavelength**4
        """
        return 8 * math.pi**3 * (self.refractive_index**2 - 1)**2/3 * 1/self.surface_molecular_number_density * 1/wavelength**4

    @property
    def rayleigh_scattering_coefficients(self):
        """
        Return the scattering coefficients for red (680nm), green (550nm), and
        blue (440nm) light.
        """
        return {
            'red': self.rayleigh_scattering_coefficient(Q_('680 nanometer')),
            'green': self.rayleigh_scattering_coefficient(Q_('550 nanometer')),
            'blue': self.rayleigh_scattering_coefficient(Q_('440 nanometer')),
        }

    @property
    def atmospheric_weight(self):
        """
        The mass of the atmosphere per mole
        """
        return sum(atmospheric_component.percentage/100 * atmospheric_component.atmospheric_gas.molar_weight for atmospheric_component in self.atmospheric_components.all())

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


    content_panels = ConcordanceEntryMixin.content_panels + PlanetaryBodyMixin.content_panels + [
        MultiFieldPanel([
            FieldPanel('surface_pressure'),
            InlinePanel('atmospheric_components', label="Atmospheric composition"),
        ], 'Atmospheric properties') ]
