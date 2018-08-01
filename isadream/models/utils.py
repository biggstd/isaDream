'''


'''
# Generic Python imports.
import os
import itertools

# Data science imports.
import pandas as pd

# DEMO_BASE = '/Users/karinharrington/github/isadream/isadream/demo_data/'
DEMO_BASE = '/home/tyler/git/isadream/isadream/demo_data/'
BASE_PATH = os.environ.get('IDREAM_JSON_BASE_PATH', DEMO_BASE)

# Demo and test json files.
SIPOS_DEMO = os.path.join(
    BASE_PATH,
    'demo_json/sipos_2006_talanta_nmr_figs.json')


def normalize(dict_or_list, left_join=False):
    '''Takes a json file and normlizes it into a list of dictionaries.

    From: https://stackoverflow.com/a/43173998/8715297

    Args:
        x (list or dict): The object to be flattened.
        left_join (bool): Controls left-join like behavior.

    Yields:
        A flattened dictionary.

    '''
    if isinstance(dict_or_list, dict):
        keys = dict_or_list.keys()
        values = (normalize(i) for i in dict_or_list.values())
        for i in itertools.product(*values):
            yield dict(zip(keys, i))
    elif isinstance(dict_or_list, list):
        if not dict_or_list and left_join is True:
            yield None
        for i in dict_or_list:
            yield from normalize(i)
    else:
        yield dict_or_list


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
