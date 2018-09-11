"""

"""

# ----------------------------------------------------------------------------
# Standard and data science imports
# ----------------------------------------------------------------------------
import os

import numpy as np

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

NMR_SIM_GROUPS = dict(
    x_groups=(
        ('Al-Na Distance', ('Al-M Distance',), ("Al",)),
        ('Periodic Box Size', ('Periodic Box Size',), ("Al")),
        ('Solvent Molecule Count', ('Solvent Molecule Count',), ("Al")),
    ),
    y_groups=(
        ('Isotropic Shielding Factor', ('Isotropic Shielding Factor',), ("Al")),
    ),
    dx_groups=(
        # ---
        # Molality calculation.
        #   = number of moles of solute per kilogram of solvent.
        # 
        # Calculate the kg of the solvent.
        #  1 atomic mass unit / (angstrom^3) = 1 660.53904 kg / m3
        #
        # ---
        (
            "Estimated Molality",
            ("Solvent Molecule Count", "Periodic Box Size"),
            (
                lambda x, y: 1 / ( ( (np.array(x) * 18.02  / 6.022e23) / np.array(y)**3 ) / 1660.53904 )
            )
        ),
    ),
    dy_groups=(
        (
            "ppm delta",
            # Isotropic Calculation
            # intercept - sigma / - slope
            ("Isotropic Shielding Factor", ), 
            (lambda x: np.array(x) - 532.36)
        ),
    )
)

# os.environ["BOKEH_RESOURCES"] = "inline"

nmr_json_paths = [demos["SIPOS_NMR"], demos["SIPOS_NMR_V2"]]
nmr_nodes = io.create_drupal_nodes(nmr_json_paths)

nmr_data = io.prepare_nodes_for_bokeh(
    NMR_GROUPS["x_groups"],
    NMR_GROUPS["y_groups"],
    nmr_nodes)


sim_json_paths = [demos["ERNESTO_NMR_1"]]
sim_nodes = io.create_drupal_nodes(sim_json_paths)

sim_df, sim_md_df, sim_md = io.prepare_nodes_for_bokeh(
    NMR_SIM_GROUPS["x_groups"],
    NMR_SIM_GROUPS["y_groups"],
    nmr_nodes)

# Create any requested derived columns.
if NMR_SIM_GROUPS.get("dx_groups"):
    for group in NMR_SIM_GROUPS.get("dx_groups"):
        sim_df = helpers.create_derived_column(sim_df, group)


# TODO: Input demo here.



scatter_tab = scatterv2.scatter_panel(NMR_GROUPS["x_groups"],
                                      NMR_GROUPS["y_groups"],
                                      *nmr_nodes)

table_tab = table.table_panel(NMR_GROUPS["x_groups"],
                              NMR_GROUPS["y_groups"],
                              *nmr_nodes)

sim_tab = table.table_panel(NMR_SIM_GROUPS["x_groups"],
                            NMR_SIM_GROUPS["y_groups"],
                            sim_df, sim_md_df, sim_md)


nmr_calc_tab = scatterv2.scatter_panel(NMR_GROUPS["x_groups"],
                                      NMR_GROUPS["y_groups"],
                                      *nmr_nodes)

tabs = bk.models.widgets.Tabs(tabs=[scatter_tab, table_tab])


layout = bk.layouts.layout(
    children=[
        bk.models.widgets.Div(text="<h1>Aluminate CrossFilter</h1>"),
        tabs],
    sizing_mode='fixed'
)

bk.io.curdoc().add_root(layout)
