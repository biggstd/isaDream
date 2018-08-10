"""

"""

# Path hack to allow imports from the parent directory.
import sys, os

sys.path.insert(0, os.path.abspath('../'))

# Local isadream imports.
from isadream.models import utils
from isadream import io

# Load the demo data. This should be replaced by a function call,
demo_json = io.read_idream_json(utils.SIPOS_DEMO)
node = io.parse_json(demo_json)

# Load the default factor?
# TODO: Determine how this should be set.
KEY_FACTOR = ('Measurement', 'ppm')

# ---------------------- Demo data
# Load the demo json.
demo_json = io.read_idream_json(utils.SIPOS_DEMO)
NODE = io.parse_json(demo_json)


def create_figure():
    """Create and return the Bokeh figure."""
    pass


def update_figure():
    """Update the figure."""
    pass


def update_bk_cds():
    """Updates the Bokeh column data source."""
    pass


def tap_select_callback():
    """Callback for selection of a single data point."""
    pass
