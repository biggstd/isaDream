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

json_paths = [demos["SIPOS_NMR"], ]
nodes = helpers.create_drupal_nodes(json_paths)

main_df, metadata = helpers.prepare_bokeh_dicts(
    NMR_GROUPS["x_groups"],
    NMR_GROUPS["y_groups"],
    nodes)

# source = bk.models.ColumnDataSource(main_df)

scatter_tab = scatterv2.scatter_panel(NMR_GROUPS["x_groups"],
                                      NMR_GROUPS["y_groups"],
                                      main_df, metadata)

table_tab = table.table_panel(NMR_GROUPS["x_groups"],
                              NMR_GROUPS["y_groups"],
                              main_df, metadata)

# tabs = bk.models.widgets.Tabs(tabs=[table_tab, ])
tabs = bk.models.widgets.Tabs(tabs=[scatter_tab, table_tab])
# print(main_df["Counter Ion"])


layout = bk.layouts.layout(
    children=[
        bk.models.widgets.Div(text="<h1>Aluminate CrossFilter</h1>"),
        tabs],
    sizing_mode='fixed'
)

bk.io.curdoc().add_root(layout)
