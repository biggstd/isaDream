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
                  data: pd.DataFrame,
                  metadata: ChainMap) -> bk.models.Panel:
    """

    :param x_groups:
    :param y_groups:
    :param data:
    :param metadata:
    :return:

    """
    source = bk.models.ColumnDataSource(data)

    # ------------------------------------------------------------------------
    # Define Column Data Source update callback.
    # ------------------------------------------------------------------------

    def update_data():
        """ A generic column data source update callback."""
        curr_selections = get_selections()
        new_source = dict(x=data[curr_selections["x"]],
                          y=data[curr_selections["y"]])

        if curr_selections.get("color_selector"):
            color_selection = curr_selections["color_selector"]
            unique_factors = data[color_selection].unique()

            new_source["color"] = bk.transform.factor_cmap(
                field_name=color_selection,
                palette=PALETTE[len(unique_factors)],
                factors=sorted(unique_factors))

        if curr_selections.get("size_selector"):
            size_selection = curr_selections["size_selector"].value

            size_scale = bk.models.LinearInterpolator(
                x=[min(data[size_selection]),
                   max(data[size_selection])],
                y=[3, 15])

            new_source["size"] = dict(field=size_selection,
                                      transform=size_scale)

        source.data.update(new_source)
        print(source.data)

    # ------------------------------------------------------------------------
    # Define selector controls.
    # ------------------------------------------------------------------------
    # Build a dictionary of controls.
    def build_selection_controls(data, x_groups, y_groups):
        column_groups = helpers.categorize_columns(data, x_groups, y_groups)
        y_names = helpers.get_group_keys(y_groups)

        controls = dict(
            x=bk.models.Select(title="X-Axis",
                               options=column_groups["continuous"],
                               value=column_groups["continuous"][0]),
            y=bk.models.Select(title="Y Axis",
                               options=y_names,
                               value=y_names[0])
        )

        if len(column_groups["discrete"]) >= 1:
            color = bk.models.Select(title='Color', value=None,
                                     options=[None] + column_groups["discrete"])
            controls["color"] = color

        if len(column_groups["continuous"]) >= 1:
            size = bk.models.Select(title='Size', value=None,
                                    options=[None] + column_groups["continuous"])
            controls["size"] = size

        return controls

    control_dict = build_selection_controls(data, x_groups, y_groups)

    def controller_callback(attr, old, new):
        print("Controller callback activated.")
        update_data()

    # Iterate through the controls and add a callback for each one.
    for name, selector in control_dict.items():
        selector.on_change("value", controller_callback)

    def get_selections():
        selections = dict()
        for name, selector in control_dict.items():
            selections[name] = selector.value
        return selections

    # Create a bokeh widget box layout to hold the controls.
    control_widget = bk.layouts.widgetbox(list(control_dict.values()))

    # ------------------------------------------------------------------------
    # Define the primary figure.
    # ------------------------------------------------------------------------
    def build_figure(selections: dict) -> bk.plotting.Figure:
        figure = bk.plotting.Figure(name="scatter_panel_figure",
                                    plot_width=600,
                                    plot_height=600)

        figure.xaxis.axis_label = selections["x"]
        figure.yaxis.axis_label = selections["y"]

        circles = figure.circle(source=source,
                                x=selections["x"],
                                y=selections["y"],
                                color=selections.get("color", "#31AADE"),
                                size=selections.get("size", 7))

        # We only need to construct a legend if a color is used.
        if selections.get("color"):
            print(selections.get("color"))
            legend_item = bk.models.LegendItem(
                label=dict(field=selections.get("color"), renderers=[circles]))
            legend = bk.models.Legend(items=[legend_item])
            figure.add_layout(legend, "below")
            figure.legend.orientation = "horizontal"

        return figure

    # ------------------------------------------------------------------------
    # Initialize defaults and define the layout.
    # ------------------------------------------------------------------------
    update_data()
    layout = bk.layouts.row(control_widget, build_figure(get_selections()))

    panel = bk.models.Panel(child=layout, title=TITLE)
    return panel
