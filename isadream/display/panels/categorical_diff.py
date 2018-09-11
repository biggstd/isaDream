"""

"""

# ----------------------------------------------------------------------------
# Standard and data science imports
# ----------------------------------------------------------------------------
import pandas as pd
from typing import ChainMap

# ----------------------------------------------------------------------------
# Bokeh imports
# ----------------------------------------------------------------------------
import bokeh as bk
import bokeh.models
import bokeh.layouts
import bokeh.palettes
import bokeh.plotting
import bokeh.transform

# ----------------------------------------------------------------------------
# ISADream imports
# ----------------------------------------------------------------------------
from isadream.display import helpers
from isadream.models.groups import GroupTypes

# ----------------------------------------------------------------------------
# Global style definitions.
# ----------------------------------------------------------------------------
TITLE = "Data Table"


# ----------------------------------------------------------------------------
# Bokeh Panel Definition
# ----------------------------------------------------------------------------
def table_panel(x_groups: GroupTypes,
                y_groups: GroupTypes,
                main_df: pd.DataFrame,
                metadata_df: pd.DataFrame,
                metadata: dict) -> bk.models.Panel:
    """

    :param x_groups:
    :param y_groups:
    :param data:
    :param metadata:
    :return:

    """
    source = bk.models.ColumnDataSource(main_df)

    x_keys = helpers.get_group_keys(x_groups)
    y_keys = helpers.get_group_keys(y_groups)

    p = bk.plotting.figure(y_range=cats, plot_width=900, 
                           x_range=(-15, 15), toolbar_location=None)

    p.outline_line_color = None
    p.background_fill_color = "#efefef"

    p.xaxis.ticker = bk.models.FixedTicker(ticks=list(range(0, 101, 10)))
    p.xaxis.formatter = bk.models.PrintfTickFormatter(format="%d%%")

    p.ygrid.grid_line_color = None
    p.xgrid.grid_line_color = "#dddddd"
    p.xgrid.ticker = p.xaxis[0].ticker

    p.axis.minor_tick_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.axis_line_color = None

    p.y_range.range_padding = 0.12

    panel = bk.models.Panel(child=table, title=TITLE)

    return panel
