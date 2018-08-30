"""Test the bokeh helpers module.

"""

# ----------------------------------------------------------------------------
# Imports for Testing
# ----------------------------------------------------------------------------

from isadream.display import helpers


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------

def test_prepare_bokeh_dicts(nmr_groups, sipos_drupal_node):
    x_groups, y_groups = nmr_groups
    helpers.prepare_bokeh_dicts(x_groups, y_groups, [sipos_drupal_node])
