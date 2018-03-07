"""
##################################
IDREAM Bokeh Visualization Helpers
##################################

This will be converted to a module that will be imported.

"""

# General Python imports.
import glob
import json

# Data Science imports.
import pandas as pd


def get_formatted_session_context(curdoc, endpoint_args='J'):
    """Returns the current session context of the given endpoint in UTF-8
    format.

    :param curdoc:
        A bokeh reference to the current document. Should this be passed as
        ``curdoc()`` or ``curdoc``?

    :param endpoint_args:
        The string or identifier for the endpoint to read.

    :returns:
        A UTF-8 formatted string of the values found in the given
        ```endpoint_args``.
    """
    # Get the HTML session context.
    sess_cont = curdoc().session_context.request.arguments

    # Get the hash or string value here.
    return sess_cont.get(endpoint_args)[0].decode("utf-8")


def find_json_files(path):
    """Finds all ``*.json`` files within a given path. Reads these files and
    appends the contents to a list that is returned.

    :param path:
        A filepath to a folder that contains the desired ``.json`` files.

    :returns:
        A the contents of the ``.json`` files as dictionaries.
    """

    json_dicts = list()

    for jstr in glob.glob(f"{path}/*.json"):
        with open(jstr, 'r') as curr_jstr:
            json_dicts.append(json.load(curr_jstr))

    return json_dicts


def construct_dataframes(data_dicts):
    """Constructs a dataframe from the given list of dictionaries.

    :param data_dicts:

    :returns:

    """
    metadata_dict = dict()
    df_list = list()

    for curr_dict in data_dicts:

        # Get the ID and create a metadata entry with that value.
        curr_id = curr_dict("ID")
        metadata_dict[curr_id] = curr_dict

        # Get the associated datafile.
        curr_datafile = curr_dict.get("data_file")

        # Build the pandas dataframe.
        new_df = pd.read_csv(curr_datafile)

        # Add a label column to track the associated metadata.
        new_df['metadata_key'] = curr_id

        # Iterate through the factor values and add them to the dataframe.
        study_factors = curr_dict.get("study_factors")
        for factor_name in study_factors:
            val = curr_dict["study_factors"][factor_name]
            new_df[factor_name] = val

        df_list.append(new_df)

    # Concatentate the dataframes generated.
    data_frame = pd.concat(df_list, ignore_index=True)

    # Return the dataframe and metadata dictionary.
    return metadata_dict, data_frame
