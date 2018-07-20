'''A data model class for IDREAM Drupal Content Nodes.

This module provides the needed utilities to convert an json file to a pandas 
dataframe for use in a Bokeh visualization application.

Attributes:
    BASE_PATH (str): The base-path that will be prepended to the filenames
        specified in the .json metadata.

'''

# Generic Python imports.
import os
import abc
import json
import itertools

# Data science imports.
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



def load_csv(path, base_path=BASE_PATH, **read_csv_kwargs):
    '''Implementation for handling user .csv files.

    Args:
        path (str): The user defined name or path to a .csv datafile.
        base_path (str): The path to be prepended to the path argument.
        **read_csv_kwargs: Arbitrary keyword arguments.

    Returns:
        DataFrame: A pandas dataframe.
    
    '''
    csv_path = os.path.join(base_path, path)
    return pd.read_csv(csv_path, skiprows=1, header=None, **read_csv_kwargs)


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
    Drupal Content Node.
    
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
        '''The highest-level metadata dataframe.

        Returns the combined metadata. All the metadata for this study is contained
        within the single row of this dataframe.
        '''
        secondary_metadata = [self.__node_info_df,
                              self.__study_factor_df,
                              self.__study_sample_df,
                              self.__study_comment_df]

        metadata_frame = pd.concat(secondary_metadata, axis=1)
        return metadata_frame


    @property
    def assay_metadata(self):
        '''The expanded, lowest-level metadata dataframe.
        
        Returns the metadata of this node contained within a multiindex
        referencing (filename, speciesReference).
        '''
        md_frame = apply_reindex(self.metadata_frame, self.assay_df)
        working_df = pd.concat([self.assay_df, md_frame], axis=1)
        working_df = working_df.set_index(
            ['dataFile', 'samples.species.speciesReference'])
        working_df = apply_multiindex(working_df)
        # Return the dataframe, infer_objects() should recognize the correct
        # data types stored within.
        return working_df.infer_objects()


    @property
    def labeled_csv_data(self):
        '''The same as csv_metadata, except with the csv column data as a new
        column.
        '''
        working_df = self.csv_metadata.copy()

        for data_file_df in working_df:
            csv_idx_array = data_file_df.loc(axis=1)[:,:,'csvColumnIndex'].values
            md_idx_array = data_file_df.index.values
            # Create the mapping dictionary.
            data_map = {md_idx: load_csv(md_idx[0], usecols=[int(csv_idx)]).T.values.flatten()
                        for md_idx, csv_idx in zip(md_idx_array, csv_idx_array)}    
            data_file_df['data'] = md_idx_array
            data_file_df['data'] = data_file_df['data'].map(data_map)
            
        return working_df
    
    @property
    def csv_metadata(self):
        '''A list of metadata dataframes for each csv column.
        
        Based on the same multiindex as in the `assay_metadata` property,
        (filename, speciesReference). This returns a list wherein each dataframe
        has information concerning each csv column index.
        '''
        working_df = self.assay_metadata
        columns = self.assay_metadata.loc(axis=1)[:, : ,'csvColumnIndex'].columns.values
        columns = tuple(c[:-1] for c in columns)
        return [working_df.loc(axis=1)[col[0], :, :] for col in columns]




