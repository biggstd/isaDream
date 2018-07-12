'''
Provides the needed utilities to convert an json file to a pandas dataframe for
use in a Bokeh visualization application.
'''

import os
import abc
import json
import itertools

import numpy as np
import pandas as pd


'''
ENVIRONMENT VARIABLES
---------------------

# TODO: Move to a config file?

The base path is set as an environment variable. It defaults do a
demo data folder within the repository with some basic data.
'''


DEMO_BASE = '/home/tylerbiggs/git/isadream/isadream/demo_data/'
BASE_PATH = os.environ.get('IDREAM_JSON_BASE_PATH', DEMO_BASE)

# Demo and test json files.
SIPOS_DEMO = os.path.join(BASE_PATH, 'demo_json/sipos_2006_talanta_nmr_figs.json')


'''
UTILITY FUNCTIONS
-----------------

Functions having nothing to do with the MVC class scope.
'''


def load_csv(path, base_path=BASE_PATH):
    '''Implementation for handling user .csv files.'''
    csv_path = os.path.join(base_path, path)
    return pd.read_csv(csv_path, skiprows=1, header=None)


def normalize(x, left_join=False):
    '''Takes a json file and normlizes it into a list of dictionaries.

    From: https://stackoverflow.com/a/43173998/8715297
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
    dataframe.'''
    normalized_dict = normalize(node_dict.get(key))
    return pd.io.json.json_normalize(list(normalized_dict))


def apply_reindex(working_df, target_df):
    '''Appllies the given index to the given dataframe and fills
    the new rows with values of working_df.

    This only makes sense if working_df is a one-row dataframe.
    '''
    return working_df.reindex(target_df.index, method='ffill')


def apply_multiindex(working_df):
    '''Convert columns to multiindexed columns.

    This assumes the columns are formatted as strings with period
    delimiters denoting column level separation.
    '''
    working_df.columns = pd.MultiIndex.from_tuples(
        [tuple(col.split('.')) for col in working_df.columns])
    return working_df


class Model:
    '''The combined Assay and Study model generated for a single
    drupal node.
    '''

    def __init__(self, node_json_path):

        self.json_path = os.path.join(BASE_PATH, node_json_path)

        # Load the json file into memory.
        with open(self.json_path) as json_file:
            self.json_dict = json.load(json_file)

        # The assay dataframe is the primary component of metadata.
        self.assay_df = self.__prepare_assay_dataframe()

        # The higher tiers of metadata apply to all data within this class.
        self.__node_info_df = self.__prepare_node_information_dataframe()
        self.__study_factor_df = self.__prepare_study_factor_dataframe()
        self.__study_sample_df = self.__prepare_study_sample_dataframe()
        self.__study_comment_df = self.__prepare_study_comment_dataframe()


    def __prepare_node_information_dataframe(self):
        key = 'nodeInformation'
        return normalize_to_dataframe(self.json_dict, key)


    def __prepare_study_sample_dataframe(self):
        key = 'studySamples'
        df = normalize_to_dataframe(self.json_dict, key)
        return df


    def __prepare_assay_dataframe(self):
        key = 'assays'
        df = normalize_to_dataframe(self.json_dict, key)
        return df


    def __prepare_study_comment_dataframe(self):
        key = 'comments'
        return normalize_to_dataframe(self.json_dict, key)


    def __prepare_study_factor_dataframe(self):
        '''Factors and conditions are found here.

        This dataframe needs more labels, rather than to be flattened, so
        that it can work nicely with the other dataframes.
        '''
        key = 'studyFactors'
        df = normalize_to_dataframe(self.json_dict, key)
        df = pd.DataFrame(df.stack())
        df = df.T
        # The trick to get the column index to expand is below.
        # The expansion function expands based on period delimited levels.
        df.columns = ['.StudyFactor.'.join(map(str, tup)) for tup in df.columns]
        return df


    @property
    def metadata_frame(self):
        '''The metadata dataframe property.

        Returns the combined metadata, re-indexed and combined with the study
        dataframe.
        '''
        secondary_metadata = [self.__node_info_df,
                              self.__study_factor_df,
                              self.__study_sample_df,
                              self.__study_comment_df]

        metadata_frame = pd.concat(secondary_metadata, axis=1)
        return metadata_frame


    @property
    def assay_metadata(self):
        '''
        '''
        md_frame = apply_reindex(self.metadata_frame, self.assay_df)
        working_df = pd.concat([self.assay_df, md_frame], axis=1)
        working_df = working_df.set_index(
            ['dataFile', 'samples.species.speciesReference'])
        working_df = apply_multiindex(working_df)
        return working_df


    @property
    def csv_data(self):
        '''
        '''
        return [load_csv(file) for file in self.assay_metadata.index.levels[0]]



class View(abc.ABC):
    '''A base class for viewing data.

    A view will be generated by information by a controller, will have
    data passed to it in the form of one or more Model classes.
    '''
    def __init__(self):
        pass


class Controller:
    '''A partial controler that reads requests from the drupal site,
    and creates a configuration for a bokeh visualization.

    These will be key-value pairs used to construct the requested View
    class.
    '''
    pass


class NMR(View):
    '''NMR Viewer class. To be moved.'''
    def __init__(self, model):
        pass


class ConcentrationRatio(View):
    '''Ratio Viewer class. To be moved.'''
    def __init__(self, model):
        pass
