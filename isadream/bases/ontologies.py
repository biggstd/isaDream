"""
#################
IDREAM Ontologies
#################

Contains all the ontology definitions used in the IDREAM
database project.
"""

from isatools.model import *

# --------------------ONTOLOGY SOURCES--------------------#
# These are the 'top-level' definitions.

nmr = OntologySource(name='Nuclear Magnetic Resonance')
nmr.file = 'http://goldbook.iupac.org/html/C/C01036.html'
nmr.description = (
    'The fractional variation of the resonance frequency of a '
    'nucleus in nuclear magnetic resonance (NMR) spectroscopy '
    'in consequence of its magnetic environment.'
)

amount_conc = OntologySource(name='Amount Concentration')
amount_conc.file = 'https://goldbook.iupac.org/html/A/A00295.html'
amount_conc.description = (
    'Amount of a constituent divided by the volume of the mixture. '
    'Also called amount-of-substance concentration, substance '
    'concentration (in clinical chemistry) and in older literature '
    'molarity. For entities B it is often denoted by [B]. The common '
    'unit is mole per cubic decimetre (mol dm −3) or mole per '
    'litre(mol L −1) sometimes denoted by M.'
)

intrinsic_properties = OntologySource(
    name='Intrinsic Material Property',
    description=(
        'Propertiy of a material that are independent of '
        'other context and other things.'))

extrinsic_properties = OntologySource(
    name='Extrinsic Material Property',
    description='Property of a material that is dependent '
    'on context and relationships.')


# --------------------ONTOLOGY ANNOTATIONS---------------- #
# These are the 'mid-level' definitions.

ppm = OntologyAnnotation(term_source=nmr)
ppm.term = "ppm"

al_27_nmr = OntologyAnnotation(term_source=nmr)
al_27_nmr.term = "27 Al NMR"

molarity = OntologyAnnotation(term_source=extrinsic_properties)
molarity.term = "Molarity"

material_purity = OntologyAnnotation(term_source=extrinsic_properties)
material_purity.term = "Material Purity"

percent_material_purity = OntologyAnnotation(
    term_source=extrinsic_properties)
percent_material_purity.term = 'Percent by Weight Purity'

degrees_celsius = OntologyAnnotation(term_source=extrinsic_properties)
degrees_celsius.term = "Temperature in degrees celsius"

# Define ontology annotations for use in drop-downs.
# These definitions should allow for...
# TOOD: Can these be more directly linked to samples?
hydroxide = OntologyAnnotation(term='Hydroxide')
aluminum = OntologyAnnotation(term='Aluminum')
sodium = OntologyAnnotation(term='Sodium')
caesium = OntologyAnnotation(term='Caesium')


# --------------------MATERIAL SOURCES----------------#
# These are the 'top-level' definitions of materials.

al_wire = Source()
al_wire.name = 'Aluminum Wire'

sodium_hydroxide = Source(name='Sodium Hydroxide')
potassium_hydroxide = Source(name='Potassium Hydroxide')
lithium_hydroxide = Source(name='Lithium Hydroxide')
caesium_hydroxide = Source(name='Caesium Hydroxide')
caesium_chloride = Source(name='Caesium Chloride')
