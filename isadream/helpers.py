"""Helper functions for creating Bokeh applications.

"""

# Standard library imports.
import os
import glob
import itertools

# Data science imports.
import pandas as pd

# Local project imports.
from . import io


def prepare_bokeh_dicts(x_groups, y_groups, drupal_nodes):
    groups = x_groups + y_groups

    assays = itertools.chain.from_iterable(
        [node.assays for node in drupal_nodes])

    cds_dicts = [assay.build_column_data_dicts(groups)
                 for assay in assays]

    cds_frames = [pd.DataFrame(cds) for cds, _ in cds_dicts]

    metadata_dfs = [pd.DataFrame(mdf) for _, mdf in cds_dicts]

    main_dataframe = pd.concat(cds_frames, sort=False)
    main_dataframe = main_dataframe.reset_index(drop=True)

    metadata_dataframe = pd.concat(metadata_dfs, axis=1, sort=False)

    return main_dataframe, metadata_dataframe


def categorize_columns(dataframe, x_groups, y_groups):
    x_keys = [key for key, _, _ in x_groups]
    y_keys = [key for key, _, _ in y_groups]
    group_keys = x_keys + y_keys

    columns = sorted(dataframe.columns)
    columns = [x for x in columns if x in group_keys]

    discrete = [x for x in columns
                if dataframe[x].dtype == object
                and x in x_keys]

    continuous = [x for x in columns
                  if x not in discrete
                  and x in x_keys]

    quantileable = [x for x in continuous
                    if len(dataframe[x].unique()) < 6
                    and x in x_keys]

    return columns, discrete, continuous, quantileable


def get_group_keys(group):
    return [key for key, _, _ in group]


def get_session_json_paths(current_document, base_path='data'):
    """

    :param current_document: A call to `curdoc()` by Bokeh.
    :return:
    """

    arguments = current_document().session_context.request.arguments

    # Get the list of arguments (there should be only one).
    file_path = arguments.get('J')[0].decode("utf-8")

    # The data will always be found in the "data" sub-directory.
    # It is placed there by the Drupal server.
    file_path = os.path.join(base_path, file_path)

    json_files = list()

    for jfile in glob.glob(f"{file_path}/*.json"):
        with open(jfile, "r") as current_file:
            json_files.append(current_file)

    return json_files


def create_drupal_nodes(json_files):
    for json_file in json_files:
        json_dict = io.read_idream_json(json_file)
        yield io.parse_json(json_dict)
