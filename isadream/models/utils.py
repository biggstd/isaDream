'''


'''
# Generic Python imports.
import os
import csv
import itertools
import collections

# Data science imports.
import pandas as pd

# TODO: Move this demo data elsewhere.
# DEMO_BASE = '/Users/karinharrington/github/isadream/isadream/demo_data/'
DEMO_BASE = '/home/tyler/git/isadream/isadream/demo_data/'
# DEMO_BASE = '/home/tylerbiggs/git/isadream/isadream/demo_data/'
BASE_PATH = os.environ.get('IDREAM_JSON_BASE_PATH', DEMO_BASE)
# Demo and test json files.
SIPOS_DEMO = os.path.join(BASE_PATH, 'demo_json/sipos_2006_talanta_nmr_figs.json')


def load_csv_as_dict(path, base_path=BASE_PATH):
    """Load a CSV file as a Python dictionary.

    The header in each file will be skipped.

    :param path:
    :param base_path:
    :return: A dictionary object with integer keys representing the csv
        column index the data was found in.

    """

    csv_path = os.path.join(str(base_path), str(path))

    data = collections.defaultdict(tuple)

    # Open the file and create a reader (an object that when iterated
    # on gives the values of each row.
    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)

        # Pop the header and get its length.
        field_int_index = range(len(next(reader)))
        field_int_index = [str(x) for x in field_int_index]

        # Iterate over the remaining rows and append the data.
        for row in reader:
            for idx, header in zip(field_int_index, reader.fieldnames):
                data[idx] = data[idx] + (float(row[header]), )

    return dict(data)


def join_lists(input_lists):
    """Helper function to join and flatten lists when one of the inputs
    can be `None`.

    """
    lists = filter(None, input_lists)
    return list(itertools.chain.from_iterable(lists))


def ensure_list(val_or_values):
    """Examine a value and ensure that it is returned as a list."""
    if hasattr(val_or_values, '__iter__') and not isinstance(val_or_values, str):
        return val_or_values
    elif val_or_values is None:
        return []
    else:
        return [val_or_values]


def get_all_elementals(node, elemental_cls, children=('assays', 'samples', 'sources')):
    """

    :param node:
    :param elemental_cls:
    :param children:
    :return:
    """

    # Construct the list to be output.
    element_list = list()

    # Examine the current node for the desired elemental.
    if hasattr(node, elemental_cls):
        element_container = getattr(node, elemental_cls)
        if element_container:
            element_list.extend(getattr(node, elemental_cls))

    # Now examine the containers on the node that may contain the desired element.
    for attr in children:

        # Check if the node has a given container attribute.
        # This method allows us to access the container regardless of what type it is.
        if hasattr(node, attr):

            # Get the value of that container.
            element_containers = getattr(node, attr)

            # Since the container can empty, check it here.
            # This does not work when combined with the if statement above. Why?
            if not element_containers:
                # If this is empty simply go to the next loop iteration.
                continue

            # Each item this container is examined recursively with this function.
            children_elements = [get_all_elementals(container, elemental_cls, children=children)
                                 for container in element_containers]

            # Flatten the list returned, and extend the output list with the new values.
            element_list.extend(itertools.chain.from_iterable(children_elements))

    return element_list


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


def query_node_factors(node, factor_query):
    for factor in node.factors:
        if factor.query(factor_query):
            return True


def query_node_species(node, species_query):
    for species in node.species:
        if species.query(species_query):
            return True
