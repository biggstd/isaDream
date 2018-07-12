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
    description=(
        'Property of a material that is dependent '
        'on context and relationships.'))

time = OntologySource(
    name="Measurements on the passage of time."
)

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
percent_material_purity.term = 'Purity Percent by Weight'

temperature = OntologyAnnotation(
    term_source=extrinsic_properties,
    term='Temperature')

degrees_celsius = OntologyAnnotation(term_source=extrinsic_properties)
degrees_celsius.term = "Temperature in degrees celsius"

counter_ion = OntologyAnnotation(term='Counter Ion')

nmr_aquisition = OntologyAnnotation(
    term='NMR Spectra Aquisition',
    term_source=nmr)

nmr_mag_str = OntologyAnnotation(
    term='NMR Magnet Strength',
    term_source=nmr)

nmr_ref_cmpd = OntologyAnnotation(
    term='NMR Reference Compound',
    term_source=nmr)

nmr_aquisition_time = OntologyAnnotation(
    term="NMR Aquisition Time",
    term_source=nmr)

nmr_pulse_width = OntologyAnnotation(
    term="NMR Pulse Width",
    term_source=nmr)

nmr_number_of_scans = OntologyAnnotation(
    term="NMR Number of Scans",
    term_source=nmr)

nmr_pulse_angle = OntologyAnnotation(
    term="NMR Pulse Angle",
    term_source=nmr)

mega_hertz = OntologyAnnotation(
    term="MHz",
    term_source=nmr
)

alum_ref_cmpd = OntologyAnnotation(
    term='KAl(SO4)2 5%, w/v',
    term_source=nmr
)

seconds = OntologyAnnotation(
    term='Seconds',
    term_source=time
)

source_preparation = OntologyAnnotation(
    term='Material Source preparation'
)


# Define ontology annotations for use in drop-downs.
# These definitions should allow for...
# TOOD: Can these be more directly linked to samples?
hydroxide = OntologyAnnotation(term='Hydroxide')
aluminum = OntologyAnnotation(term='Aluminum')
sodium = OntologyAnnotation(term='Sodium')
caesium = OntologyAnnotation(term='Caesium')
lithium = OntologyAnnotation(term='Lithium')
potassium = OntologyAnnotation(term='Potassium')


# MATERIAL SOURCES ------------------------------------------------------------
# These are the 'top-level' definitions of materials.

# Consider moving this to the NMR Demo file...
al_wire = Source()
al_wire.name = 'Aluminum Wire'
al_wire.characteristics = [
    Characteristic(
        category=material_purity,
        value=0.99,
        unit=percent_material_purity,
    )
]

sodium_hydroxide = Source(name='Sodium Hydroxide')
potassium_hydroxide = Source(name='Potassium Hydroxide')
lithium_hydroxide = Source(name='Lithium Hydroxide')
caesium_hydroxide = Source(name='Caesium Hydroxide')
caesium_chloride = Source(name='Caesium Chloride')

# PROTOCOL PARAMETERS ---------------------------------------------------------
# These are fields that are supplied to protocols.
param_temperature = ProtocolParameter(parameter_name=degrees_celsius)
param_magnet_strength = ProtocolParameter(parameter_name=nmr_mag_str)
param_reference_compound = ProtocolParameter(parameter_name=nmr_ref_cmpd)
param_aquisition_time = ProtocolParameter(parameter_name=nmr_aquisition_time)
param_pulse_width = ProtocolParameter(parameter_name=nmr_pulse_width)
param_scans = ProtocolParameter(parameter_name=nmr_number_of_scans)
param_pulse_angle = ProtocolParameter(parameter_name=nmr_pulse_angle)

# PROTOCOLS -------------------------------------------------------------------
# Define experimental protocols.
nmr_aquisition_protocol = Protocol(
    name="NMR Data Aquisition",
    protocol_type=nmr_aquisition,
    description="NMR Aquisition Protocol.",
    parameters=[
        param_temperature,
        param_magnet_strength,
        param_reference_compound,
        param_aquisition_time,
        param_pulse_width,
        param_scans,
        param_pulse_angle,
    ],
)
