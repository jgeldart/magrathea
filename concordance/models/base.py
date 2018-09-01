from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from quantity_field import ureg
Q_ = ureg.Quantity

COMMON_BLOCKS = [
    ('heading', blocks.CharBlock(classname="full title", template="blocks/heading_block.html")),
    ('paragraph', blocks.RichTextBlock(template="blocks/rich_text_block.html")),
    ('image', ImageChooserBlock()),
]

GRAVITATIONAL_CONSTANT = Q_('6.67408e-11 * m**3 * kg**-1 * s**-2')
STEFAN_CONSTANT = Q_(5.670367e-8, ureg.watt * ureg.meter**-2 * ureg.kelvin**-4)
