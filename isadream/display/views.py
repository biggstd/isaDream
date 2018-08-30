"""Generic helper functions for Bokeh views.

Functions in this module are to be written as de-coupled as possible
from the isadream model structure, as well as any specific Bokeh application.

A general rule: if the function references a Bokeh model by a string name,
or interacts with the isadream api, it should not be placed in this module.

"""

# ----------------------------------------------------------------------------
# Boilerplate
# ----------------------------------------------------------------------------

import logging

log = logging.getLogger(__name__)

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library imports

# External imports

# Bokeh imports
import bokeh as bk
import bokeh.models
import bokeh.layouts
import bokeh.palettes
import bokeh.plotting
import bokeh.transform

# ----------------------------------------------------------------------------
# Globals and constants
# ----------------------------------------------------------------------------

# These are the columns (as generated from `isadream.io`) where the
# foreign key for the metadata dictionary resides.
METADATA_COLUMNS = ["parent_node", "assay_node", "sample_node"]


# ----------------------------------------------------------------------------
# General API
# ----------------------------------------------------------------------------

def build_hover_tool(x_groups, y_groups):
    """Build a generic hover tooltip for visualizations.

    """
    # We want to display all the groups upon hovering, regardless of
    # their source axis.
    all_groups = x_groups + y_groups

    # The list of tooltips is prepared per the requirements of the
    # bokeh.models.HoverTool() documentation.
    # TODO: Reconsider this string building hack.
    tooltips = [(label, "@{" + label + "}")
                for label, _, _ in all_groups]

    return bk.models.HoverTool(tooltips=tooltips)


def get_selection_metadata_keys(data, selections=None,
                                columns=METADATA_COLUMNS):
    """Get the foreign (metadata dict) keys from a data set.

    """
    return [data.get(col)[index]
            for col in columns
            for index in selections]


def build_metadata_paragraph(keys, metadata):
    """The most atomic display of a metadata element. Builds a
    bokeh paragraph widget.

    :param keys: A list of keys that may be found in `metadata`.
    :param metadata: A dictionary (or hashable object) which
        contains the metadata to be displayed in the paragraph.

    TODO: Consider changing from Paragraph to Div.
    :return: A bokeh.models.widgets.Paragraph instance populated
        with the appropriate metadata.

    """

    # It is possible this function gets called with `None` objects
    # passed as keys. We must first filter these out.
    filtered_keys = [(filter(None, keys))]

    # If this list is empty, then return a place-holder paragraph.
    if not filtered_keys:
        return bk.models.Paragraph(text="No point selected.")

    # Otherwise, construct the text with the remaining keys.
    text = ""  # Create an empty string to add to.
    for key in filtered_keys:
        text += metadata.get(key, "No value found.\n")

    return bk.models.Paragraph(text=text)


def build_metadata_column(name, paragraphs):
    """Construct a bokeh column for viewing selected metadata.

    Each selected point is stored in its own Div element.

    :param name:
    :param paragraphs: The pre-constructed bokeh Paragraph
        objects to be combined.
    :return:
    """
    return bk.layouts.column(name=name, children=paragraphs)

# ----------------------------------------------------------------------------
# Dev API
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Private API
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Code
# ----------------------------------------------------------------------------
