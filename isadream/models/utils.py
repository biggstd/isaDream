'''


'''
# Generic Python imports.
import os
import itertools

# Data science imports.
import pandas as pd

# DEMO_BASE = '/Users/karinharrington/github/isadream/isadream/demo_data/'
DEMO_BASE = '/home/tylerbiggs/git/isadream/isadream/demo_data/'
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


def pad_infinite(iterable, padding=None):
    return itertools.chain(iterable, itertools.repeat(padding))


def pad(iterable, size, padding=None):
    return itertools.islice(pad_infinite(iterable, padding), size)


def flatten(foo):
    if isinstance(foo, str):
        yield foo
    else:
        for x in foo:
            if hasattr(x, '__iter__') and not isinstance(x, str):
                for y in flatten(x):
                    yield y
            else:
                yield x


def split_index(dataframe, mode='index'):
    '''Split columns into tuples.

    This assumes the columns are formatted as strings with period
    delimiters denoting column level separation.

    '''
    def try_split(val):
        '''Just try to split, if we fail, return the original value.'''
        try:
            return val.split('.')
        except:
            return val

    def tuplize_row(row):
        '''Convert a given row to a tuple. See parent function.'''
        values = flatten(row)
        values = [try_split(val) for val in values]
        values = flatten(values)

        return list(values)

    working_df = dataframe.copy()

    if mode == 'index':
        new_index = [tuplize_row(col) for col in working_df.index]
        max_len = len(max(new_index, key=len))
        working_df.index = [tuple(pad(col, max_len)) for col in new_index]

    elif mode == 'columns':
        new_cols = [tuplize_row(col) for col in working_df.columns]
        max_len = len(max(new_cols, key=len))
        working_df.columns = [tuple(pad(col, max_len)) for col in new_cols]

    return working_df


def try_xs(dataframe, key, level=1):
    '''
    '''
    try:
        return dataframe.xs(key, level=level)
    except KeyError:
        return None

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
