"""
====================================
NMR Demo Study and Assay Definitions
====================================


This file defines the Study and Assay components
necessary to generate a complete set of ISA *.json
document(s).

This ISA file is for demo purposes.

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
from isatools import isajson
from isatools.isajson import ISAJSONEncoder
import json
import os
import pandas as pd

# Import all of the custom ontologies defined
# for the IDREAM project thus far.
from isadream.ontologies import *


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

    # Ontology Sources --------------------------------------------------------
    inv.ontology_source_references.append(nmr)
    inv.ontology_source_references.append(intrinsic_properties)
    inv.ontology_source_references.append(extrinsic_properties)

    # Publications ------------------------------------------------------------
    # TODO: Append publications to their corresponding studies.
    sipos2006_talanta = Publication()
    sipos2006_talanta.title = (
        '27 Al NMR and Raman spectroscopic studies of alkaline aluminate '
        'solutions with extremely high caustic content - Does the '
        'octahedral species Al(OH)_6^{3-} exist in solution?')
    sipos2006_talanta.doi = '10.1016/j.talanta.2006.02.008'
    sipos2006_talanta.author_list = 'Pal Sipos, Glenn Hefter, Peter M. May'

    sipos2006_RSC = Publication()
    sipos2006_RSC.title = (
        'Chemical speciation in concentrated alkaline aluminate solutions '
        'in sodium, potassium and caesium media. Interpretation of the '
        'unusual variations of the observed hydroxide activity.')
    sipos2006_RSC.doi = '10.1039/b513357b'
    sipos2006_RSC.author_list = (
        'Pal Sipos, Mark Schibeci, Gabor Peintler, Peter M. May, Glen Hefter')

    # Study Factors -----------------------------------------------------------
    # Study Factors are variables that an experimentalist changes in order to
    # observe a result.
    molarity_factor = StudyFactor()
    molarity_factor.name = "Molarity Study Factor"
    molarity_factor.factor_type = molarity

    aluminate_molarity = StudyFactor()
    aluminate_molarity.name = 'Aluminate Molarity'
    aluminate_molarity.factor_type = molarity

    celsius = StudyFactor()
    celsius.name = "Degrees Celsius"
    celsius.factor_type = degrees_celsius

    counter_ion_factor = StudyFactor()
    counter_ion_factor.name = "Counter Ion"
    counter_ion_factor.factor_type = counter_ion

    # Material Samples --------------------------------------------------------
    # Attributes: name, characteristics, factor_values, derives_from, comments.
    # Normally these would be unique on a per-study basis. For this demo case
    # The same instances are used here for simplicity.

    Cs_Al_soln = Sample()
    # TODO: Add ionic strength Characteristic or a FactorValue.
    Cs_Al_soln.name = 'Caesium Aluminate Solution'
    Cs_Al_soln.derives_from = [
        al_wire,
        caesium_hydroxide,
        caesium_chloride]
    Cs_Al_soln.characteristics = [
        Characteristic(category=counter_ion, value=caesium)]
    Cs_Al_soln.factor_values = [
        FactorValue(
            factor_name=aluminate_molarity,
            value=3.0,
            unit=molarity,
        ),
        FactorValue(
            factor_name=counter_ion_factor,
            value='Cs+',
            unit=counter_ion,
        ),
    ]

    KOH_Al_soln = Sample()
    KOH_Al_soln.name = 'sipos_2006_talanta_KOH_Al_soln'
    KOH_Al_soln.derives_from = [al_wire, potassium_hydroxide]
    KOH_Al_soln.characteristics = [
        Characteristic(category=counter_ion, value=potassium)]
    KOH_Al_soln.factor_values = [
        FactorValue(
            factor_name=aluminate_molarity,
            value=0.005,
            unit=molarity,),
        FactorValue(
            factor_name=counter_ion_factor,
            value='K+',
            unit=counter_ion,
        ),
    ]

    NaOH_Al_soln = Sample()
    NaOH_Al_soln.name = 'sipos_2006_talanta_NaOH_Al_soln'
    NaOH_Al_soln.derives_from = [al_wire, sodium_hydroxide]
    NaOH_Al_soln.characteristics = [
        Characteristic(category=counter_ion, value=sodium)]
    NaOH_Al_soln.factor_values = [
        FactorValue(
            factor_name=aluminate_molarity,
            value=0.005,
            unit=molarity,),
        FactorValue(
            factor_name=counter_ion_factor,
            value='Na+',
            unit=counter_ion,
        ),
    ]

    LiOH_Al_soln = Sample()
    LiOH_Al_soln.name = 'sipos_2006_talanta_LiOH_Al_soln'
    LiOH_Al_soln.derives_from = [al_wire, lithium_hydroxide]
    LiOH_Al_soln.characteristics = [
        Characteristic(category=counter_ion, value=lithium)]
    LiOH_Al_soln.factor_values = [
        FactorValue(
            factor_name=aluminate_molarity,
            value=0.005,
            unit=molarity,),
        FactorValue(
            factor_name=counter_ion_factor,
            value='Li+',
            unit=counter_ion,
        ),
    ]
    # DataFile Definitions ----------------------------------------------------
    df_sipos_2006_talanta_fig_3_KOH = DataFile(
        filename='sipos_2006_talanta_fig_3_KOH.csv',
        comments=[
            Comment(name='column_0', value='molarity hydroxide'),
            Comment(name='column_1', value='ppm aluminum'),
        ]
    )

    df_sipos_2006_talanta_fig_3_NaOH = DataFile(
        filename='sipos_2006_talanta_fig_3_NaOH.csv',
        comments=[
            Comment(name='column_0', value='molarity hydroxide'),
            Comment(name='column_1', value='ppm aluminum'),
        ]
    )

    df_sipos_2006_talanta_fig_3_LiOH = DataFile(
        filename='sipos_2006_talanta_fig_3_LiOH.csv',
        comments=[
            Comment(name='column_0', value='molarity hydroxide'),
            Comment(name='column_1', value='ppm aluminum'),
        ]
    )

    df_sipos_2006_RSC_table1 = DataFile(
        filename='sipos2006_RSC_table_1.csv',
        comments=[
            Comment(name='column_0', value='molarity hydroxide'),
            Comment(name='column_1', value='ppm aluminum')
        ]
    )

    # Study definitions -------------------------------------------------------
    stu1 = Study()
    stu1.identifier = "sipos2006_talanta"
    stu1.title = "Sipos 2006 Talanta Study"
    stu1.description = "Study abstraction of Sipos' 2006 Talanta paper."
    stu1.publications = [sipos2006_talanta]
    # Design descriptors define the type of study, ie. the primary
    # measurements and conditions used.
    stu1.design_descriptors = [
        ppm,
        al_27_nmr,
        molarity
    ]
    stu1.sources = [
        al_wire,
        sodium_hydroxide,
        potassium_hydroxide,
        lithium_hydroxide
    ]
    stu1.samples = [NaOH_Al_soln]
    stu1.units = [ppm, molarity, celsius]
    stu1.factors = [molarity_factor, celsius]
    inv.studies.append(stu1)

    stu2 = Study()
    stu2.identifier = 'sipos2006_RSC'
    stu2.title = 'Sipos 2006 Royal Society of Chemistry Study'
    stu2.description = 'Study abstraction of Sipos 2006 RSC paper.'
    stu2.publications = [sipos2006_RSC]
    stu2.design_descriptors = [
        ppm,
        al_27_nmr,
        molarity
    ]
    stu2.characteristic_categoires = [
        aluminum,
        hydroxide,
        caesium
    ]
    stu2.sources = [
        al_wire,
        sodium_hydroxide,
        caesium_hydroxide,
        caesium_chloride
    ]
    inv.studies.append(stu2)

    # Assay definitions -------------------------------------------------------

    sipos_2006_talanta_fig_3_KOH = Assay()
    sipos_2006_talanta_fig_3_KOH.identifier = 'sipos_2006_talanta_fig_3_KOH'
    sipos_2006_talanta_fig_3_KOH.measurement_type = ppm
    sipos_2006_talanta_fig_3_KOH.technology_type = al_27_nmr
    sipos_2006_talanta_fig_3_KOH.technology_platform = 'Bruker 300Mhz'
    sipos_2006_talanta_fig_3_KOH.sources = [
        al_wire,
        potassium_hydroxide,
    ]
    sipos_2006_talanta_fig_3_KOH.samples = [
        KOH_Al_soln,
    ]
    sipos_2006_talanta_fig_3_KOH.units = [ppm, molarity]
    sipos_2006_talanta_fig_3_KOH.data_files = [
        df_sipos_2006_talanta_fig_3_KOH
    ]
    sipos_2006_talanta_fig_3_KOH.process_sequence = [
        Process(
            name='sipos2006_nmr_process',
            executes_protocol=nmr_aquisition_protocol,
            parameter_values=[
                ParameterValue(
                    category=param_temperature,
                    value=25,
                    unit=degrees_celsius,
                ),
                ParameterValue(
                    category=param_magnet_strength,
                    value=300,
                    unit=mega_hertz,
                ),
                ParameterValue(
                    category=param_reference_compound,
                    value=alum_ref_cmpd,
                    unit=nmr_ref_cmpd
                ),
                ParameterValue(
                    category=param_aquisition_time,
                    value=0.5,
                    unit=seconds
                ),
                ParameterValue(
                    category=param_pulse_width,
                    value=0.000005,
                    unit=seconds
                ),
                ParameterValue(
                    category=param_scans,
                    value=120,
                    unit=nmr_number_of_scans
                ),
                ParameterValue(
                    category=param_pulse_angle,
                    value=90,
                    unit=nmr_pulse_angle
                ),
            ],
            inputs=[NaOH_Al_soln],
            outputs=[df_sipos_2006_talanta_fig_3_KOH],
        )
    ]

    stu1.assays.append(sipos_2006_talanta_fig_3_KOH)

    sipos_2006_talanta_fig_3_NaOH = Assay()
    sipos_2006_talanta_fig_3_NaOH.identifier = 'sipos_2006_talanta_fig_3_NaOH'
    sipos_2006_talanta_fig_3_NaOH.measurement_type = ppm
    sipos_2006_talanta_fig_3_NaOH.technology_type = al_27_nmr
    sipos_2006_talanta_fig_3_NaOH.technology_platform = 'Bruker 300Mhz'
    sipos_2006_talanta_fig_3_NaOH.sources = [
        al_wire,
        sodium_hydroxide,
    ]
    sipos_2006_talanta_fig_3_NaOH.samples = [
        NaOH_Al_soln,
    ]
    sipos_2006_talanta_fig_3_NaOH.units = [ppm, molarity]
    sipos_2006_talanta_fig_3_NaOH.data_files = [
        df_sipos_2006_talanta_fig_3_NaOH
    ]
    stu1.assays.append(sipos_2006_talanta_fig_3_NaOH)

    sipos_2006_talanta_fig_3_LiOH = Assay()
    sipos_2006_talanta_fig_3_LiOH.identifier = 'sipos_2006_talanta_fig_3_LiOH'
    sipos_2006_talanta_fig_3_LiOH.measurement_type = ppm
    sipos_2006_talanta_fig_3_LiOH.technology_type = al_27_nmr
    sipos_2006_talanta_fig_3_LiOH.technology_platform = 'Bruker 300Mhz'
    sipos_2006_talanta_fig_3_LiOH.sources = [
        al_wire,
        lithium_hydroxide,
    ]
    sipos_2006_talanta_fig_3_LiOH.samples = [
        LiOH_Al_soln,
    ]
    sipos_2006_talanta_fig_3_LiOH.units = [ppm, molarity]
    sipos_2006_talanta_fig_3_LiOH.data_files = [
        df_sipos_2006_talanta_fig_3_LiOH
    ]
    stu1.assays.append(sipos_2006_talanta_fig_3_LiOH)

    sipos_2006_RSC_table1 = Assay()
    sipos_2006_RSC_table1.identifier = 'sipos_2006_RSC_table1'
    sipos_2006_RSC_table1.measurement_type = ppm
    sipos_2006_RSC_table1.technology_type = al_27_nmr
    sipos_2006_RSC_table1.technology_platform = 'Bruker 300MHz'
    sipos_2006_RSC_table1.sources = [
        al_wire,
        caesium_chloride,
        caesium_hydroxide
    ]
    sipos_2006_RSC_table1.samples = [Cs_Al_soln]
    sipos_2006_RSC_table1.units = [ppm, molarity]
    sipos_2006_RSC_table1.data_files = [
        df_sipos_2006_RSC_table1
    ]
    stu2.assays.append(sipos_2006_RSC_table1)

    return inv


def get_studies_by_design_descriptor(investigation, descriptor):
    """Returns ISA Study objects with the given descriptor.

    Searches an ISA Investigation object and returns Study
    objects that have the given descriptor string.
    """

    # Create an empty list to store the studies to be returned.
    matching_study_list = list()

    # Pull all the studies from a given investigation, and store
    # them in a list. This is an ISA tools property call that
    # returns a list of studies.
    all_studies_list = investigation.studies

    # Seach each of these studies for the desired descriptor.
    for study in all_studies_list:
        # If the given descriptor is found within, append this
        # study to the output list.
        if descriptor in study.design_descriptors:
            matching_study_list.append(study)

    return matching_study_list


def get_assays_by_measurement_type(study, measurement_ontology):
    """Returns ISA Assay objects with the given measurement type.

    Searches an ISA Study object, and returns a list of ISA assay
    objects with the matching measurement ontology.
    """

    # Create an empty list to store the Assay objects to be returned.
    matching_assay_list = list()

    # Pull all of the all of the Assay objects from the input Study.
    all_assays_list = study.assays

    # Search each assay, and append it to the output list if the
    # measurement type matches the input given in
    # measurement_ontology.
    for assay in all_assays_list:
        if measurement_ontology == assay.measurement_type:
            matching_assay_list.append(assay)

    return matching_assay_list


def get_dataFiles_with_ID_from_assay(assay):
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

    # Pull the identifier of this assay.
    # assay_id = assay.identifier

    return data_files


def build_pandas_dataframe(data_file, prepath=None):
    """
    Reads a custom comment in the dataFile object input.

    TODO: Add error handling as decribed below.
    THIS FUNCTION SHOULD READ THE CUSTOM COMMENT EMBEDDED
    WITHIN THE DATAFILE OBJECT. IT SHOULD THROW AN ERROR
    IF THIS COMMENT IS NOT PRESENT.
    """

    # Get the data file path.
    data_path = data_file.filename

    # If a prepath entry is found, construct the directory.
    if prepath is not None:
        data_path = os.path.join(prepath, data_path)

    # TODO: Implement below...
    # Get the pandas csv options from the comment.
    # Create the dataframe with the options loaded.

    # Create the dataframe.
    data_frame = pd.read_csv(
        filepath_or_buffer=data_path,
        # index_col=False
    )

    # Get the column headers from the comment.
    # Get the comment by name using the ISA tools function.
    # get_comment(self, name)
    # Find the number of columns in the data frame, then
    # iterate through the column_# list to this length to
    # retrieve the proper column names.
    new_column_names = list()

    for i in range(len(data_frame.columns)):
        # Build the comment name that maps to column_i.
        i_col_name = data_file.get_comment('column_{}'.format(i)).value
        # Add that comment valuye to the list of new column names.
        new_column_names.append(i_col_name)

    # Assign the new column names to the data frame.
    data_frame.columns = new_column_names

    return data_frame


def add_ISA_metadata_key_to_pandas_dataframe(data_frame, col, val):
    """Adds the study and assay identifier to an input data_frame.

    This simply creates a new column `col` the dataframe, and assigns
    all values of that column to the input given in `val`.

    The purpose of this is so that an extracted and processed
    data set from a given data file can be associated with the
    correct set of metadata.
    """
    # Create a new pandas column with the name `col` and fill out all
    # values with the `val`.
    data_frame[col] = val

    # TODO: Unclear if I need to return this value... I think the
    # code alayoutbove should modify the dataframe in place...

    return data_frame


def get_factor_values_from_study(study):
    """Returns a list of factors and their corresponding values.

    The list returned is a nested, list of lists.
    """
    # Use the ISA study factors property to generate the list of
    # factor objects within the input study.
    factor_values = study.factors

    return factor_values


def jsonify_isa_object(isa_object):
    """Converts an ISA object object to a .json string.
    """
    return json.dumps(
        isa_object,
        cls=ISAJSONEncoder,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )


def tabify_investigation(investigation):
    """Converts an ISA object to a tabular format."""
    return isatab.dumps(investigation)


def build_data_md_pair(study_list):
    """
    Builds a pandas dataframe object from a list of studies, to this dataframe
    is added:
        + FactorValues
        + Study Identifier
        + Assay Identifier
    Builds a metadata dictionary of study objects with their identifier.
    """
    df_list = list()
    metadata_dict = dict()

    for study in study_list:

        # For each matching study, get its identifier.
        study_ID = study.identifier

        # Create the entry for the metadata dictionary.
        metadata_dict[study_ID] = study

        # Get each matching assay within the found studies.
        matching_assays = get_assays_by_measurement_type(study, ppm)

        # For each of these assays, get the associated DataFile and:
        for assay in matching_assays:

            # Get the Assay identifier.
            assay_ID = assay.identifier

            # Create the Assay metadata dictionary entry.
            metadata_dict[assay_ID] = assay

            # For each data_file object.
            for data_file in assay.data_files:

                # Build the pandas dataframe:
                new_df = build_pandas_dataframe(
                    data_file,
                    '/home/tylerbiggs/git/isaDream/isadream/demo_data')

                # Add the appropriate tags to the newly minted dataframe.
                new_df['assay_ID'] = assay_ID
                new_df['study_ID'] = study_ID

                # For each of the factor values appended to a sample, add the
                # factor name and value to the dataframe.
                for sample in assay.samples:
                    for factor in sample.factor_values:
                        # Combine the name and unit for now.
                        new_df[str(factor.factor_name.name)] = factor.value

                # Append the new dataframe to the output list.
                df_list.append(new_df)

    # Concatenate the dataframes generated.
    dataframe_out = pd.concat(df_list, ignore_index=True)

    # Return the dataframe and the metadata dictionary.
    return dataframe_out, metadata_dict


if __name__ == '__main__':
    invest = build_nmr_output()
    print(jsonify_isa_object(invest))
    # print(tabify_investigation(invest))
    # # Testing some other functions.
    # matching_studies = get_studies_by_design_descriptor(invest, al_27_nmr)

    # print([jsonify_isa_object(x) for x in matching_studies])
    # out_assays = list()

    # for study in matching_studies:
    #     matching_assays = get_assays_by_measurement_type(study, ppm)
    #     out_assays.extend(matching_assays)
    # print(out_assays)
