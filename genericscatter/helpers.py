"""
##################################
IDREAM Bokeh Visualization Helpers
##################################

This will be converted to a module that will be imported.

Resources
#########

Also to practice tables in .rst.

======================== =============================================
Description              Link
======================== =============================================
AJAX and Bokeh Examples  https://stackoverflow.com/a/38871646
======================== =============================================

"""

# General Python imports.
import os
import glob
import json


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


def find_json_files(path, data_mount):
    """Finds all ``*.json`` files within a given path. Reads these files and
    appends the contents to a list that is returned.

    :param path:
        A filepath to a folder that contains the desired ``.json`` files.

    :param data_mount:
        The mount path of the data files to be prepended to the path.

    :returns:
        A the contents of the ``.json`` files as dictionaries.
    """
    # Prepend the data_mount path.
    full_path = os.path.join(data_mount, path)

    json_dicts = list()

    # Searth the constructed path for .json files, read those found and
    # append the contents as a dictionary to the json_dicts list.
    for jstr in glob.glob(f"{full_path}/*.json"):
        with open(jstr, 'r') as curr_jstr:
            json_dicts.append(json.load(curr_jstr))

    return json_dicts
