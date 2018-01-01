"""
====================================
NMR Demo Study and Assay Definitions
====================================


This file defines the Study and Assay components
necessary to generate a complete set of ISA *.json
documents.

For each **Study** there must be:

    + An Identifier string.
    + A title string.
    + A description string.
    + Design_descriptors must be appended, these are
    classifications of the study based on its overall
    design.
    + A list of sources.
    + A list of samples.
    + A list of units used.
    + A list of factors in the Study.

Each Study must also be appended to the Investigation.


For each **Assay** object there must be:

    + A measurement type.
    + A technology type as an Ontology.
    + A technology platform as a string.
    + A list of samples.
    + A list of units.
    + A list of data files, given as DataFile objects.
        + These must have the column headers defined
          in a custom Comment object, which can be
          stored in the DataFile object natively with
          respect to ISA tools.
        + These columns must be linked to a StudyFactor.
    + A list of sources.

Each Assay must be appended to its corresponding Assay.


As these are defined mock up a GUI for inputing this
data into a web browser.

"""

from isatools.model import *
import pandas as pd


pandas_df_comment = Comment()
pandas_df_comment.name = ""


def build_nmr_output():
    """
    Returns a series of ISA documents describing the NMR
    data to be shown in the demo.

    Returns an Investigation object.
    """
    inv = Investigation()
    inv.identifier = "IDREAM_Aluminate"
    inv.title = "IDREAM Aluminate Database"
    inv.description = (
        "A database for the IDREAM project that stores "
        "data needed for IDREAM researchers. It stores literature "
        "data, experimental and simulation data, along with "
        "any associated metadata.")

    nmr = OntologySource(
        name='Nuclear Magnetic Resonance',
        description="Concepts related to NMR experiments.")
    inv.ontology_source_references.append(nmr)

    intrinsic_properties = OntologySource(
        name='Intrinsic Material Property',
        description=(
            'Propertiy of a material that are independent of '
            'other context and other things.'))
    inv.ontology_source_references.append(intrinsic_properties)

    extrinsic_properties = OntologySource(
        name='Extrinsic Material Property',
        description='Property of a material that is dependent '
        'on context and relationships.')
    inv.ontology_source_references.append(extrinsic_properties)

    ppm = OntologyAnnotation(term_source=nmr)
    ppm.term = "ppm"

    al_27_nmr = OntologyAnnotation(term_source=nmr)
    al_27_nmr.term = "27 Al NMR"

    molarity = OntologyAnnotation(term_source=amnt_conc)
    molarity.term = "Molarity"

    material_purity = OntologyAnnotation(term_source=extrinsic_properties)
    material_purity.term = "Material Purity"

    percent_material_purity = OntologyAnnotation(
        term_source=extrinsic_properties)
    percent_material_purity.term = 'Percent by Weight Purity'

    degrees_celsius = OntologyAnnotation(term_source=extrinsic_properties)
    degrees_celsius.term = "Temperature in degrees celsius"

    # MATERIAL SOURCES

    al_source = Source(name='Aluminum Wire')
    al_source.characteristics.append(temp_characteristic)

    sodium_hydroxide = Source(name='Sodium Hydroxide')

    potassium_hydroxide = Source(name='Potassium Hydroxide')

    lithium_hydroxide = Source(name='Lithium Hydroxide')

    # STUDY FACTORS

    molarity_factor = StudyFactor()
    molarity_factor.name = "Molarity Study Factor"
    molarity_factor.factor_type = molarity

    celsius = StudyFactor()
    celsius.name = "Degrees Celsius"
    celsius.factor_type = degrees_celsius

    # MATERIAL SAMPLES

    sodium_aluminate_soln = Sample()
    sodium_aluminate_soln.name = "The sodium solution used in sipos 2006."
    # Set the derives_from list to include all the source materials used.
    sodium_aluminate_soln.derives_from = [al_source, sodium_hydroxide]
    sodium_aluminate_soln.factor_values = [
        FactorValue(factor_name=celsius, value=25, unit=degrees_celsius)
    ]

    stu1 = Study()
    stu1.identifier = "Sipos 2006 Study"
    stu1.title = "Sipos 2006 NMR Study  Figure 2"
    stu1.description = "Test study for Sipos' 2006 NMR study."
    stu1.design_descriptors.append(ppm)
    stu1.sources = [al_source, sodium_hydroxide]
    stu1.samples = [sodium_aluminate_soln]
    stu1.units = [ppm, molarity, celsius]
    stu1.factors = [molarity_factor, celsius]
    inv.studies.append(stu1)

    # Table 1. from Sipos 2006 Dalton Trans.
    stu2 = Study()
    stu2.identifier = ''

    # Sipos 2006 Science Direct.
    # Build a protocol, or add factor values to track the following.
    # 
    # 

    assay = Assay()
    assay.measurement_type = ppm
    assay.technology_type = al_27_nmr
    assay.technology_platform = "Bruker DPX 300MHz"
    assay.samples = [sodium_aluminate_soln]
    assay.units = [ppm, molarity, celsius]
    assay.data_files = [DataFile(filename='sipos2006-fig2.csv')]
    assay.sources = [al_source, sodium_hydroxide]

    stu.assays.append(assay)

    return inv


def get_dataFiles_from_assay(assay):
    """
    Searches an ISA *.json document for data files, and their
    column headers.

    THIS READS THE CUSTOM COMMENT DEFINED FOR PANDAS DATAFRAME
    GENERATION.

    :param isa_investigation:
        The investigation object to be read.

    :returns:
        Any DataFile objects appended to the ISA investigation
        input.
    """
    # Pull the list of DataFile objects from the Investigation.
    data_files = assay.data_files

    return data_files


def build_metadata_dict(isa_investigation, key):
    """
    Builds a dictionary from an isa_investigation object.
    Essentially builds a dictionary from...

    # TODO: What level of the investigation, study, assay should
    this key be assigned to?

    :param isa_investigation:
        An ISA Investigation object to be processed.

    :param key:
        The key to assign to the given ISA investigation.

    :returns:
        {key: isa_investigation} dictionary.
    """
    pass


def build_pandas_dataframe(dataFile):
    """
    Reads a custom comment in the dataFile object input.

    THIS FUNCTION SHOULD READ THE CUSTOM COMMENT EMBEDDED
    WITHIN THE DATAFILE OBJECT. IT SHOULD THROW AN ERROR
    IF THIS COMMENT IS NOT PRESENT.
    """
    # Get the data file path.

    # Get the column headers from the comment.
    # Get the comment by name using the ISA tools function.
    # get_comment(self, name)

    # Get the pandas csv options from the comment.

    # Create the dataframe with the options loaded.

    # df = pd.read_csv

    return dataframe
