'''A data model class for IDREAM Drupal Content Nodes.

This module provides the needed utilities to convert an json file to a pandas
dataframe for use in a Bokeh visualization application.

Attributes:
    BASE_PATH (str): The base-path that will be prepended to the filenames
        specified in the .json metadata.

'''

# Generic Python imports.
import os
import json
import itertools

# Data science imports.
import pandas as pd


'''
ENVIRONMENT VARIABLES
---------------------

# TODO: Move to a config file.

The base path is set as an environment variable. It defaults do a
demo data folder within the repository with some basic data.
'''

DEMO_BASE = '/Users/karinharrington/github/isadream/isadream/demo_data/'
# DEMO_BASE = '/home/tylerbiggs/git/isadream/isadream/demo_data/'
BASE_PATH = os.environ.get('IDREAM_JSON_BASE_PATH', DEMO_BASE)

# Demo and test json files.
SIPOS_DEMO = os.path.join(
    BASE_PATH,
    'demo_json/sipos_2006_talanta_nmr_figs.json')


def normalize(x, left_join=False):
    '''Takes a json file and normlizes it into a list of dictionaries.

    From: https://stackoverflow.com/a/43173998/8715297

    Args:
        x (list or dict): The object to be flattened.
        left_join (bool): Controls left-join like behavior.

    Yields:
        A flattened dictionary.

    '''
    if isinstance(x, dict):
        keys = x.keys()
        values = (normalize(i) for i in x.values())
        for i in itertools.product(*values):
            yield dict(zip(keys, i))
    elif isinstance(x, list):
        if not x and left_join is True:
            yield None
        for i in x:
            yield from normalize(i)
    else:
        yield x


def normalize_to_dataframe(node_dict, key):
    '''Reads a nested dictionary and returns a normalized pandas
    dataframe.

    '''
    normalized_dict = normalize(node_dict.get(key))
    return pd.io.json.json_normalize(list(normalized_dict))


def apply_multiindex(working_df):
    '''Convert columns to multiindexed columns.

    This assumes the columns are formatted as strings with period
    delimiters denoting column level separation.

    '''
    working_df.columns = pd.MultiIndex.from_tuples(
        [tuple(col.split('.')) for col in working_df.columns])
    return working_df


def split_columns(working_df):
    '''Split columns into tuples.

    This assumes the columns are formatted as strings with period
    delimiters denoting column level separation.

    '''
    working_df.columns = [tuple(col.split('.'))
                          for col in working_df.columns]
    return working_df


def load_csv(path, base_path=BASE_PATH, **read_csv_kwargs):
    '''Implementation for handling user .csv files.

    Args:
        path (str): The user defined name or path to a .csv datafile.
        base_path (str): The path to be prepended to the path argument.
        **read_csv_kwargs: Arbitrary keyword arguments.

    Returns:
        DataFrame: A pandas dataframe.

    '''
    csv_path = os.path.join(str(base_path), str(path))
    return pd.read_csv(csv_path, skiprows=1, header=None, **read_csv_kwargs)


class Assay:
    '''Model for an individual assay contained within a DrupalNode.

    There can be one or more Assay class instance per DrupalNode, depeding
    on how many datafiles are supplied by the user.

    An assay likely has it's own unique datafile, as well as csv column index
    references. It is also possible for csv column index references to be
    defined outside the assay-level metadata. ie. a common measurement can be
    specified once, while sample measurements must be more granuarly defined.

    + View classes are based on the data contained within a set of Assays.

    In addition to the assays own set of metadata, there are four other basic
    sets of data that need to be incorporated.


    '''

    def __init__(self, assay_df, drupal_node):
        '''initialization for an Assay instance.

        '''
        self.__assay_df = pd.concat([assay_df, drupal_node.metadata_frame])
        # TODO: Encapsulate in a try: except block? Uses an DrupalNode property!
        self.__drupal_node_metadata_frame = drupal_node.metadata_frame

    @property
    def sparse_metadata(self):
        '''Contains the merged Assay and Drupal metdata.

        '''
        return pd.concat([self.__assay_df, self.__drupal_node_metadata_frame])

    @property
    def metdata(self):
        '''Contains the merged Assay and Drupal metadata information, as well
        as the data loaded from the associated `.csv` file.

        '''
        pass

    @classmethod
    def from_drupal_node(cls, drupal_node):
        '''Factory for creating Assays from a DrupalNode instance.

        This is (probably) the most common ways Assays will be created.

        '''

        # Get the private study assays attribute.
        df = drupal_node._DrupalNode__study_assays
        # Re-index so that we can iterate through the data per-datafile.
        df = df.set_index(['dataFile', 'samples.species.speciesReference'])

        # Groupby the lowest index level (the unique datafiles) allows us to
        # iterate through the data.
        for data_file, new_df in df.groupby(level=0):
            yield cls(new_df, drupal_node)


class DrupalNode:
    '''The Study model generated for a single Drupal Node.

    Each Drupal content node for a given experiment is modeled under the same
    `.json` structure.

    There are sub-groups to this structure:
        1. **Node information**: Information concerning the Drupal Node, and
           the overall experiment description and title.
        2. **Study Factors**: Experimental data that applies to all the data
           contained by this node.
        3. **Node Samples**: Experimental materials that apply to all data
           contained within this node.
        4. **Assays**: Individual datafiles and their associated factors.
        5. **Commments**: Commments that apply to this entire Node.

    The atomic units of this model are:
        + **Factors**: Any quantitative or qualitative value. There are several
          subtypes of Factors. They are named differently only for the purposes
          of working with Drupal fields (and perhaps clarity.) Their names are
          based on their location in the `json` structure.
            + studyFactors
            + studySampleFactors
            + materialCharacteristic
            + studySampleFactors
            + AssaySampleFactors
          Out of five possible fields the user must supply three of them, one
          must be the `factorType`, another must be a `unitRef` the other must
          be a value. Either a decimal, string or reference.
          + A very special type of **Factor** is the `csvColumnIndex`
        + **Species**: The visual Bokeh models are based on a 'species'
          interpretation. That is the way in which we can theoretically
          compare values accross experiements. Each Species entry must have:
            + speciesReference: A string reference of the species.
            + stoichiometry: A decimal value representing this species
              relative ratio as compared to a samples Factors. This value may be
              used by visualizations that are concentration based.

    # TODO: Discuss comments and other parts of the json file.
            Expand on csvColumnIndex.

    **Outline of Dataflow**:

    Drupal Entry -> SQL Database -> PHP Drupal Module -> .json file ->
    isaDream DrupalNode -> idream Assays -> Bokeh Applicaitons


    '''

    def __init__(self, node_json_path):

        self.json_path = os.path.join(BASE_PATH, node_json_path)

        # Load the json file into memory.
        with open(self.json_path) as json_file:
            self.json_dict = json.load(json_file)

        # The higher tiers of metadata apply to all data (and Assay instances
        # generated by this instance.) within this class.
        self.__node_information = normalize_to_dataframe(self.json_dict, 'nodeInformation')
        self.__study_factors = normalize_to_dataframe(self.json_dict, 'studyFactors')
        self.__study_samples = normalize_to_dataframe(self.json_dict, 'studySamples')
        self.__study_comments = normalize_to_dataframe(self.json_dict, 'comments')

        # The data to be used to construct Assay instances.
        self.__study_assays = normalize_to_dataframe(self.json_dict, 'assays')

        # TODO: Outline dataframes and their flow to Bokeh.

    @property
    def node_information(self):
        '''Node information property.

        Returns a re-indexed node information dataframe.
        '''
        return self.__node_information

    @property
    def study_factors(self):
        '''Study Factor property.

        Returns a re-indexed and stacked study factor dataframe.

        This property can contain csv column index references.

        '''
        # Get a copy of the working dataframe.
        df = self.__study_factors.copy()

        # Reindex this dataframe with a meaningfull name.
        df['study_factor_idx'] = [f'study_factor_{val}' for val in df.index.values]
        df = df.set_index('study_factor_idx')

        # Stack the dataframe so that it will have only one column.
        df = pd.DataFrame(df.stack())

        # Transpose the dataframe so that it will have one long row.
        df = df.T
        return df

    @property
    def study_samples(self):
        '''Study Sample property.

        Returns a re-indexed and stacked set of study samples as a dataframe.

        This property can contain csv column index references.

        '''
        # Get a copy of the starting dataframe.
        df = self.__study_samples.copy()

        # Reindex this dataframe with a meaningfull name.
        df['study_sample_idx'] = [f'study_sample_{val}' for val in df.index.values]
        df = df.set_index('study_sample_idx')

        # df = self.apply_multiindex(df)
        # Stack the dataframe so that it will have only one column.
        df = pd.DataFrame(df.stack())

        # Transpose the dataframe so that it will have one long row.
        df = df.T
        return df

    @property
    def study_comments(self):
        '''Study comment property.

        Returns a stacked and re-indexed comment dataframe.

        '''
        # Get a copy of the starting dataframe.
        df = self.__study_comments.copy()

        # Reindex this dataframe with a meaningfull name.
        df['study_comments_idx'] = [f'study_comments_{val}' for val in df.index.values]
        df = df.set_index('study_comments_idx')

        # Stack the dataframe so that it will have only one column.
        df = pd.DataFrame(df.stack())

        # Transpose the dataframe so that it will have one long row.
        df = df.T
        return df

    @property
    def assays(self):
        '''Assay property.

        Returns a stacked and re-inexed assay dataframe.

        This property can contain csv column index references.

        '''
        # Get a copy of the starting dataframe.
        df = self.__study_assays.copy()

        # Reindex this dataframe with a meaningfull name.
        df['study_assay_idx'] = [f'study_assay_{val}' for val in df.index.values]
        df = df.set_index('study_assay_idx')

        # Stack the dataframe so that it will have only one column.
        df = pd.DataFrame(df.stack())

        # Transpose the dataframe so that it will have one long row.
        df = df.T
        return df

    @property
    def metadata_frame(self):
        '''Contains all metadata above the assay level.

        '''
        secondary_metadata = [self.node_information,
                              self.study_factors,
                              self.study_samples,
                              self.study_comments]

        working_df = pd.concat(secondary_metadata, axis=1)
        return working_df

    @property
    def assay_metadata(self):
        '''The expanded, lowest-level metadata dataframe.

        Returns the metadata of this node contained with in a pandas dataframe.

        '''
        # Concatenate the assay and metadata frames. Since the meteadata frame
        # will only ever have one row entry, and its information applies to
        # all points in `self.assay_df`, it is filled.
        working_df = pd.concat([self.assay_df, self.metadata_frame], axis=1).ffill()
        # Return the dataframe, infer_objects() should recognize the correct
        # data types stored within.
        return working_df.infer_objects()

    @property
    def study_metadata(self):
        '''The expanded study-level metadata frame.

        Returns the study-level metadaa of this node.

        '''
        # Concatenate the study and metadata frames. Since the meteadata frame
        # will only ever have one row entry, and its information applies to
        # all points in `self.assay_df`, it is filled.
        working_df = pd.concat(
            [self.__study_sample_df, self.metadata_frame], axis=1).ffill()
        return working_df.infer_objects()

    @property
    def csv_metadata(self):
        '''A list of metadata dataframes for each csv column.

        Based on the same multiindex as in the `assay_metadata` property,
        (filename, speciesReference). This returns a list wherein each dataframe
        has information concerning each csv column index.

        '''
        working_df = self.assay_metadata
        working_df.columns = pd.MultiIndex.from_tuples(working_df.columns)
        # working_df = apply_multiindex(working_df)
        columns = working_df.loc(axis=1)[:, :, 'csvColumnIndex'].columns.values
        columns = tuple(c[:-1] for c in columns)
        return [working_df.loc(axis=1)[col[0], :, :] for col in columns]
