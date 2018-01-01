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
