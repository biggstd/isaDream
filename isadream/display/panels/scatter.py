"""

"""

# ----------------------------------------------------------------------------
# Standard and data science imports
# ----------------------------------------------------------------------------
import numpy as np
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
# import bokeh.transform

# ----------------------------------------------------------------------------
# ISADream imports
# ----------------------------------------------------------------------------
from isadream.display import helpers
from isadream.models.groups import GroupTypes

# ----------------------------------------------------------------------------
# Global style definitions.
# ----------------------------------------------------------------------------
PALETTE = bk.palettes.Category10
TITLE = "Scatter Plot"


def style(figure: bk.plotting.Figure):
    figure.title.align = "center"
    figure.title.text_font = "serif"
    return figure


# ----------------------------------------------------------------------------
# Bokeh Panel Definition
# ----------------------------------------------------------------------------

def scatter_panel(x_groups: GroupTypes,
                  y_groups: GroupTypes,
                  main_df: pd.DataFrame,
                  metadata: ChainMap) -> bk.models.Panel:
    """

    :param x_groups:
    :param y_groups:
    :param main_df:
    :param metadata:
    :return:

    """
    source = bk.models.ColumnDataSource(main_df)

    # ------------------------------------------------------------------------
    # Define Column Data Source update callback.
    # ------------------------------------------------------------------------

    def update_data():
        """ A generic column data source update callback."""
        source.data = dict(x=main_df[x_axis.value],
                           y=main_df[y_axis.value])

        for col in main_df.columns:
            source.add(data=main_df[col], name=col)

        # print(source.data)

    # ------------------------------------------------------------------------
    # Define selector controls.
    # ------------------------------------------------------------------------
    # Build a dictionary of controls.
    # def build_selection_controls(data, x_groups, y_groups):
    column_groups = helpers.categorize_columns(main_df, x_groups, y_groups)
    y_names = helpers.get_group_keys(y_groups)

    x_axis = bk.models.Select(title="X-Axis",
                              options=column_groups["continuous"],
                              value=column_groups["continuous"][0])
    y_axis = bk.models.Select(title="Y Axis",
                              options=y_names,
                              value=y_names[0])

    controls = [x_axis, y_axis]

    if len(column_groups["discrete"]) >= 1:
        color = bk.models.Select(title='Color', value="None",
                                 options=["None"] + column_groups["discrete"])
        # controls["color"] = color
        controls.append(color)

    if len(column_groups["continuous"]) >= 1:
        size = bk.models.Select(title='Size', value="None",
                                options=["None"] + column_groups["continuous"])
        controls.append(size)

    def controller_callback(attr, old, new):
        update_data()
        curr_layout = bk.plotting.curdoc().get_model_by_name('panel_layout')
        curr_layout.children[1] = build_figure()

    for control in controls:
        control.on_change("value", controller_callback)

    # Create a bokeh widget box layout to hold the controls.
    control_widget = bk.layouts.widgetbox(controls)

    # ------------------------------------------------------------------------
    # Define the primary figure.
    # ------------------------------------------------------------------------
    def build_figure() -> bk.plotting.Figure:
        figure = bk.plotting.Figure(name="scatter_panel_figure",
                                    plot_width=600,
                                    plot_height=600)

        figure.xaxis.axis_label = x_axis.value
        figure.yaxis.axis_label = y_axis.value

        if color.value != "None":
            unique_factors = np.unique(source.data[color.value])
            color_mapper = bk.models.CategoricalColorMapper(
                factors=unique_factors,
                palette=bk.palettes.Category10[len(unique_factors)], )
            colors = {"field": color.value, "transform": color_mapper}
        else:
            colors = "#31AADE"

        if size.value != "None":
            size_scale = bk.models.LinearInterpolator(
                x=[min(source.data[size.value]),
                   max(source.data[size.value])],
                y=[3, 15])
            sizes = dict(field=size.value, transform=size_scale)
        else:
            sizes = 7

        circles = figure.circle(source=source,
                                x="x",
                                y="y",
                                color=colors,
                                size=sizes)

        # We only need to construct a legend if a color is used.
        try:
            if color.value != "None":
                legend_item = bk.models.LegendItem(
                    label=dict(field=color.value), renderers=[circles])
                legend = bk.models.Legend(items=[legend_item])
                figure.add_layout(legend, "below")
                figure.legend.orientation = "horizontal"
        except NameError:
            pass

        return figure

    # ------------------------------------------------------------------------
    # Initialize defaults and define the layout.
    # ------------------------------------------------------------------------
    update_data()
    layout = bk.layouts.row(control_widget, build_figure(), name="panel_layout")

    panel = bk.models.Panel(child=layout, title=TITLE)
    return panel
