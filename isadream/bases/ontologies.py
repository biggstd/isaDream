"""
#################
IDREAM Ontologies
#################

Contains all the ontology definitions used in the IDREAM
database project.
"""

from isatools.model import (
    OntologySource,
    OntologyAnnotation,
    Source,
)

# --------------------ONTOLOGY SOURCES--------------------#
# These are the 'top-level' definitions.

nmr = OntologySource()
nmr.name = 'Nuclear Magnetic Resonance'
nmr.file = 'http://goldbook.iupac.org/html/C/C01036.html'
nmr.description = (
    'The fractional variation of the resonance frequency of a '
    'nucleus in nuclear magnetic resonance (NMR) spectroscopy '
    'in consequence of its magnetic environment.'
)

amount_conc = OntologySource()
amount_conc.name = 'Amount Concentration'
amount_conc.file = 'https://goldbook.iupac.org/html/A/A00295.html'
amount_conc.description = (
    'Amount of a constituent divided by the volume of the mixture. '
    'Also called amount-of-substance concentration, substance '
    'concentration (in clinical chemistry) and in older literature '
    'molarity. For entities B it is often denoted by [B]. The common '
    'unit is mole per cubic decimetre (mol dm −3) or mole per '
    'litre(mol L −1) sometimes denoted by M.'
)

intrinsic_prop = OntologySource()

extrinsic_prop = OntologySource()


# --------------------ONTOLOGY ANNOTATIONS---------------- #
# These are the 'mid-level' definitions.

ppm = OntologyAnnotation()

Al_27_nmr = OntologyAnnotation()

molarity = OntologyAnnotation()

material_purity = OntologyAnnotation()


# --------------------MATERIAL SOURCES----------------#
# These are the 'top-level' definitions of materials.

Al_metal = Source()

NaOH = Source()

KOH = Source()

LiOH = Source()
