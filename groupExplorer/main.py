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
from isadream import config
from isadream.display import helpers
from groupExplorer.panels import scatter

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

json_paths = [config["JSON_DEMOS"]["SIPOS_NMR"], ]
nodes = helpers.create_drupal_nodes(json_paths)

main_df, metadata = helpers.prepare_bokeh_dicts(
    NMR_GROUPS["x_groups"],
    NMR_GROUPS["y_groups"],
    nodes)

# source = bk.models.ColumnDataSource(main_df)

scatter_tab = scatter.scatter_panel(NMR_GROUPS["x_groups"],
                                    NMR_GROUPS["y_groups"],
                                    main_df, metadata)

print(scatter_tab)

tabs = bk.models.widgets.Tabs(tabs=[scatter_tab, ])
layout = bk.layouts.layout(
    children=[
        bk.models.widgets.Div(text="<h1>Aluminate CrossFilter</h1>"),
        tabs],
    sizing_mode='fixed'
)

bk.io.curdoc().add_root(layout)
