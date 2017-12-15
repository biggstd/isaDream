"""
#########################
IDREAM Investigation Base
#########################

Constructs the ISA investigation base for use in
generating all ISA *.json documents.
"""

# General Python imports.
import json

# isatools specific imports.
from isatools.model import *
from isatools.isajson import ISAJSONEncoder


def IDREAM_investigation_base():
    """
    Creates the investigation base for use in generating
    linked IDREAM .json metadata files.

    This function collects all defined ontologies, and
    fills out an ISA tools investigation object with
    those references, along with other default values.

    :returns:
        An ISATools investigation object.
    """

    # Declare the investigation to be returned.
    inv = Investigation()

    # Assign data to the investigation.
    inv.identifier = 'IDREAM Aluminate Investigation'
    inv.title = 'IDREAM Aluminate Database'
    inv.description = (
        'A database for the IDREAM project that stores '
        'data and metadata from literature, experimental, '
        'and simulated sources.'
    )

    # Return the constructed investigation object.
    return inv


def jsonify_investigation(investigation):
    """
    Converts a given investigation to an ISA json.

    :param investigation:
        An ISA tools investigation object.

    :returns:
        A string of json text, formatted for readability.
    """

    # Create and return the .json object.
    return json.dumps(
        obj=investigation,
        cls=ISAJSONEncoder,
        sort_keys=True,
        indent=4,
        separators=(',', ':'))
