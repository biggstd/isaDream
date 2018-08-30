"""Helper functions for creating Bokeh applications.

"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library imports
import os
import glob
import logging
import itertools
import collections

# Type hinting imports.
from typing import Tuple, List, Callable

# External imports
import pandas as pd

# Bokeh imports
import bokeh as bk
# import bokeh.models
import bokeh.document
# import bokeh.layouts
# import bokeh.palettes
# import bokeh.plotting
# import bokeh.transform

# Local project imports.
from isadream import io
from isadream import DATA_MOUNT
from isadream.models.nodal import DrupalNode

# ----------------------------------------------------------------------------
# Globals and constants
# ----------------------------------------------------------------------------

# Setup the error logger.
log = logging.getLogger(__name__)

# Get the environment variable to find the base path for data files
# described in the loaded metadata.
HTTP_QUERY_STRING = "JD"


# ----------------------------------------------------------------------------
# General API
# ----------------------------------------------------------------------------

def get_session_json_paths(current_document: bk.document.Document,
                           base_path: str = DATA_MOUNT) -> List[str]:
    """Get the HTTP request of an active bokeh document.

    The HTTP request points to the path where this document should load
    its .json metadata files.

    :param current_document: A bokeh Document instance. Usually provided by
        a call to `bk.plotting.curdoc()`.
    :param base_path: The base directory for reading json datafiles.

    :returns: A list of json file paths.

    """

    # Get the HTTP request and find the arguments being passed.
    arguments = current_document.session_context.request.arguments
    log.info(f"Document HTTP context arguments: {arguments}")

    # Get the list of arguments (there should be only one).
    file_path = arguments.get(HTTP_QUERY_STRING)[0].decode("utf-8")

    # The data should always be found in the "data" sub-directory.
    # It is placed there by the Drupal server.
    file_path = os.path.join(base_path, file_path)
    log.info(f"Json file path found to be: {file_path}")

    return [json_file for json_file in
            glob.glob(f"{file_path}/*.json")]


def create_drupal_nodes(json_files: List[str]) -> List[DrupalNode]:
    """Create multiple DrupalNode models from a list of json files.

    :param json_files: A list of json file paths as strings.
    :returns: A list of DrupalNode objects.

    """

    return [io.parse_node_json(io.read_idream_json(json_file))
            for json_file in json_files]


def prepare_bokeh_dicts(x_groups: Tuple[str, str, Tuple[str]],
                        y_groups: Tuple[str, str, Tuple[str]],
                        drupal_nodes: List[DrupalNode]
                        ) -> Tuple[pd.DataFrame, collections.ChainMap]:
    """Prepare a main pd.DataFrame and a metadata ChainMap from a
    list of DrupalNodes.

    :param x_groups: A user-given grouping query for X-axis values.
    :param y_groups: A user-given grouping query for Y-axis values.
    :param drupal_nodes: A list of DrupalNode objects to apply the
        group queries to.

    :returns: A populated pd.DataFrame and a ChainMap with all the
        data and metadata requested by the given  groups from the
        given nodes.

    """

    # Get all assays from all nodes.
    assays = itertools.chain.from_iterable(
        [node.assays for node in drupal_nodes])

    # Collect data and metadata entries for each assay.
    cds_dicts = [io.build_node_data(assay, x_groups + y_groups)
                 for assay in assays]

    # Construct a pd.DataFrame for each entry, and a ChainMap of the
    # metadata for each entry.
    cds_frames = [pd.DataFrame(cds) for cds, _ in cds_dicts]
    metadata = collections.ChainMap(*[mdf for _, mdf in cds_dicts])

    # Concatenate all the data frames together and reset the index.
    main_data_frame = pd.concat(cds_frames, sort=False)
    main_data_frame = main_data_frame.reset_index(drop=True)

    return main_data_frame, metadata


def categorize_columns(data_frame: pd.DataFrame,
                       x_groups: Tuple[str, str, Tuple[str]],
                       y_groups: Tuple[str, str, Tuple[str]]
                       ) -> Tuple[List[str], List[str],
                                  List[str], List[str]]:
    """Helper function for categorizing user-group defined columns.

    The categories are then used to choose which visualization
    dimension is appropriate for a given column.

    :param data_frame:
    :param x_groups:
    :param y_groups:

    :returns:

    """

    # Extract the keys from the groups.
    x_keys = get_group_keys(x_groups)
    y_keys = get_group_keys(y_groups)
    group_keys = x_keys + y_keys

    # Sort the columns, omit any not in group_keys -- ie. the
    # metadata foreign key columns.
    columns = sorted(data_frame.columns)
    columns = [x for x in columns if x in group_keys]

    # Discrete objects (strings and the like).
    discrete = [x for x in columns
                if data_frame[x].dtype == object
                and x in x_keys]

    # Continuous values only should remain.
    continuous = [x for x in columns
                  if x not in discrete
                  and x in x_keys]

    # Some of the continuous values may make more sense to bin
    # if there are few enough unique values.
    quantileable = [x for x in continuous
                    if len(data_frame[x].unique()) < 6
                    and x in x_keys]

    return columns, discrete, continuous, quantileable


def get_group_keys(group):
    return [key for key, _, _ in group]


def create_derived_columns(data_frame: pd.DataFrame,
                           derived_group: Tuple[str, Tuple[str, ...], Callable]
                           ) -> pd.DataFrame:
    """Calculate a column based on those already present in the data frame.

    :param data_frame:
    :param derived_group:
    :returns: A modified data_frame with the new column.

    """

    # Extract the column names and the callable from the derived group.
    new_column, precursor_columns, group_function = derived_group

    # Apply the calculation with the precursor columns, and save the
    # result to the given data frame.
    data_frame[new_column] = group_function(*precursor_columns)

    return data_frame

#
# def load_session_data(x_groups: tuple[str, str, tuple[str]],
#                       y_groups: tuple[str, str, tuple[str]],
#                       current_document: bk.document.Document
#                       ) -> tuple[bk.models.ColumnDataSource,
#                                  collections.ChainMap]:
#     """Load data for a document instance based on the provided query groups.
#
#     :return:
#
#     """
#
#     # Find the paths based on the session context.
#     json_paths = get_session_json_paths(current_document)
#
#     # Build DrupalNode models from each of the found json files.
#     nodes = create_drupal_nodes(json_paths)
#
#     # Combine these nodes into a single set of data and metadata
#     # based on the user-supplied query groups.
#     main_data_frame, metadata_dict = prepare_bokeh_dicts(
#         x_groups=x_groups, y_groups=y_groups, nodes=nodes)
#
#     # Build a Bokeh column data source object.
#     source = bk.models.ColumnDataSource(main_data_frame)
#
#     return source, metadata_dict
