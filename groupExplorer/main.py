"""

"""

# ----------------------------------------------------------------------------
# Standard and data science imports
# ----------------------------------------------------------------------------
import os

# ----------------------------------------------------------------------------
# Bokeh imports
# ----------------------------------------------------------------------------
import bokeh as bk
import bokeh.io
import bokeh.models
import bokeh.layouts

# ----------------------------------------------------------------------------
# ISADream imports
# ----------------------------------------------------------------------------
from isadream import config, demos
from isadream import io
from isadream.display import helpers
from isadream.display.panels import scatterv2, table

# ----------------------------------------------------------------------------
# Temporary Fixtures.
# ----------------------------------------------------------------------------
NMR_GROUPS = dict(
    x_groups=(('Total Aluminate Concentration', ('Molar',), ("Al",)),
              ('Counter Ion Concentration', ('Molar',),
               ("Na+", "Li+", "Cs+", "K+")),
              ('Counter Ion', ('Species',), ("Na+", "Li+", "Cs+", "K+",)),
              ('Base Concentration', ('Molar',), ("OH-",))),
    y_groups=(('27 Al ppm', ('ppm',), ("Al",)),)
)

os.environ["BOKEH_RESOURCES"] = "inline"

json_paths = [demos["SIPOS_NMR_V2"], ]
nodes = io.create_drupal_nodes(json_paths)

main_df, metadata_df, metadata_dict = io.prepare_nodes_for_bokeh(
    NMR_GROUPS["x_groups"],
    NMR_GROUPS["y_groups"],
    nodes)

scatter_tab = scatterv2.scatter_panel(NMR_GROUPS["x_groups"],
                                      NMR_GROUPS["y_groups"],
                                      main_df, metadata_df, metadata_dict)

table_tab = table.table_panel(NMR_GROUPS["x_groups"],
                              NMR_GROUPS["y_groups"],
                              main_df, metadata_df, metadata_dict)

tabs = bk.models.widgets.Tabs(tabs=[scatter_tab, table_tab])


layout = bk.layouts.layout(
    children=[
        bk.models.widgets.Div(text="<h1>Aluminate CrossFilter</h1>"),
        tabs],
    sizing_mode='fixed'
)

bk.io.curdoc().add_root(layout)
