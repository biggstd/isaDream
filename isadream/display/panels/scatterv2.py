"""

"""

# ----------------------------------------------------------------------------
# Standard and data science imports
# ----------------------------------------------------------------------------
import itertools
import numpy as np
import pandas as pd
from typing import ChainMap, Tuple, Dict, Union, List

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
METADATA_COLUMNS = ("parent_node", "assay_node", "sample_node")
PALETTE = bk.palettes.Category10
TITLE = "Scatter Plot"


# def style(figure: bk.plotting.Figure):
#     figure.title.align = "center"
#     figure.title.text_font = "serif"
#     return figure


def build_selection_controls(bokeh_source: bk.models.ColumnDataSource,
                             x_groups: GroupTypes,
                             y_groups: GroupTypes
                             ) -> Dict[str, bk.models.Select]:
    """Build a dictionary of bokeh selection controls based on given
    groups and data.

    :param bokeh_source: The data set to be examined in the form of
        a bokeh ColumnDataSource model.
    :param x_groups:  A user-given grouping query for axis values.
    :param y_groups:A user-given grouping query for axis values.
    :returns: A dictionary of labels: bk.models.Select controllers.

    """

    selection_controls = dict()  # Dictionary to be returned.

    # Create a dictionary of column groups. They keys are:
    # columns, discrete, continuous, quantileable.
    column_groups = helpers.categorize_columns(bokeh_source.to_df(),
                                               x_groups, y_groups)
    # Get the names of those columns in the Y groups.
    y_names = helpers.get_group_keys(y_groups)

    # Create the selectors.
    selection_controls["x_axis"] = bk.models.Select(
        title="X-Axis",
        options=column_groups["continuous"],
        value=column_groups["continuous"][0])

    selection_controls["y_axis"] = bk.models.Select(
        title="Y Axis",
        options=y_names,
        value=y_names[0])

    # Create a custom control for the axis scale.
    selection_controls["x_axis_type"] = bk.models.Select(
        title="X Axis Scale",
        options=["linear", "log"],
        value="linear")

    # Check if there are values which can be viewed reasonably with
    # a color or point size dimension, create the selector tool if so.
    if len(column_groups["discrete"]) >= 1:
        color = bk.models.Select(
            title='Color', value="None",
            options=["None"] + column_groups["discrete"])
        selection_controls["color"] = color

    if len(column_groups["continuous"]) >= 1:
        size = bk.models.Select(
            title='Size', value="None",
            options=["None"] + column_groups["continuous"])
        selection_controls["size"] = size

    return selection_controls


def create_colors(bokeh_source: bk.models.ColumnDataSource,
                  color_column: str,
                  palette=PALETTE
                  ) -> Union[str, Dict[str, bk.models.ColorMapper]]:
    """

    :param bokeh_source:
    :param color_column:
    :param palette:
    :return:
    """
    if color_column != "None":
        unique_factors = np.unique(bokeh_source.data[color_column])
        color_mapper = bk.models.CategoricalColorMapper(
            factors=unique_factors,
            palette=palette[len(unique_factors)])

        return {"field": color_column, "transform": color_mapper}

    else:
        # Return a default color.
        return "#31AADE"


def get_metadata_keys(bokeh_source: bk.models.ColumnDataSource,
                      index_selections: int,
                      metadata_columns: Tuple[str, ...] = METADATA_COLUMNS
                      ) -> Tuple[str, ...]:
    """

    :param bokeh_source:
    :param index_selections:
    :param metadata_columns:
    :return:
    """
    return tuple(bokeh_source.data.get(col)[index_selections]
                 for col in metadata_columns)


def create_sizes(bokeh_source: bk.models.ColumnDataSource,
                 size_column: str
                 ) -> Union[Dict[str, bk.models.LinearInterpolator], int]:
    """

    :param bokeh_source:
    :param size_column:
    :return:
    """
    if size_column != "None":
        size_scale = bk.models.LinearInterpolator(
            x=[min(bokeh_source.data[size_column]),
               max(bokeh_source.data[size_column])],
            y=[3, 15])
        return dict(field=size_column, transform=size_scale)
    else:
        return 7


def build_metadata_paragraph(metadata_dict: ChainMap,
                             keys: Tuple[str, ...]
                             ) -> bk.models.widgets.Paragraph:
    """

    :param metadata_dict:
    :param keys:
    :return:
    """
    for key in keys:
        print("--------------------------")
        print(type(metadata_dict.get(key)))
        print(metadata_dict.get(key))

    metadata_items = tuple(*itertools.chain.from_iterable(
        [metadata_dict.get(key) for key in keys]))
    print(metadata_items)
    text = str(metadata_items)
    # for key in metadata_keys:
    #     try:
    #         text += item.as_markup
    #         print(text)
    #     except Exception as error:
    #         text += str(item)
    #         print(error)

    paragraph = bk.models.widgets.Paragraph(text=text)
    return paragraph


def create_metadata_column(bokeh_source: bk.models.ColumnDataSource,
                           metadata: ChainMap,
                           selected_indexes: List[int] = None
                           ) -> bk.layouts.column:
    """

    :param bokeh_source:
    :param metadata:
    :param selected_indexes:
    :return:
    """

    # We must handle the None case so that we can call this function
    # upon application start, as well as point deselection.
    if selected_indexes is not None:
        # Get the foreign keys from the bokeh source.
        selected_metadata_keys = (get_metadata_keys(bokeh_source, index)
                                  for index in selected_indexes)

        # Use those active keys to build metadata paragraphs.
        paragraphs = [build_metadata_paragraph(metadata, keys)
                      for keys in selected_metadata_keys]

    else:
        paragraphs = [bk.models.widgets.Paragraph(
            text="No data point selected.")]

    # Build a column of the generated metadata paragraphs.
    # They should resolve from most general to most specific.
    metadata_column = bk.layouts.column(children=paragraphs)

    return metadata_column


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
    # ------------------------------------------------------------------------
    # Create the interactive bokeh column data source.
    # ------------------------------------------------------------------------
    source = bk.models.ColumnDataSource(main_df)

    # ------------------------------------------------------------------------
    # Define point selection callback.
    # ------------------------------------------------------------------------
    def point_selection_callback(attr, old, new):
        # Get the selected value indices or None with a ternary operator.
        selected_indexes = new['1d']['indices'] \
            if new['1d']['indices'] else None

        # Create the metadata column layout element.
        column = create_metadata_column(source, metadata, selected_indexes)
        # Get the parent layout element and update its children.
        curr_layout = bk.plotting.curdoc().get_model_by_name('metadata_column')
        curr_layout.children[0] = column

    # Add the point selection callback to the bokeh source object.
    source.on_change("selected", point_selection_callback)

    # ------------------------------------------------------------------------
    # Define selector controls, and add a callback function.
    # ------------------------------------------------------------------------
    # Create dictionary of controls based on the given groups and data.
    controls = build_selection_controls(source, x_groups, y_groups)

    def controller_callback(attr, old, new):
        # Get the parent layout that contains the main figure.
        curr_layout = bk.plotting.curdoc().get_model_by_name('main_figure')
        # Replace the current child with an updated figure.
        curr_layout.children[0] = build_figure()

    # Assign the callback function defined above to each of the generated
    # selector controls.
    for control in controls.values():
        control.on_change("value", controller_callback)

    # Create a bokeh widget box layout to hold the controls.
    control_widget = bk.layouts.widgetbox(list(controls.values()))

    # ------------------------------------------------------------------------
    # Define the primary figure.
    # ------------------------------------------------------------------------
    def build_figure() -> bk.plotting.Figure:

        # Create the basic figure object.
        figure = bk.plotting.Figure(name="scatter_panel_figure",
                                    x_axis_type=controls["x_axis_type"].value,
                                    plot_width=600,
                                    plot_height=600)

        # Set the axis titles of the figure.
        figure.xaxis.axis_label = controls["x_axis"].value
        figure.yaxis.axis_label = controls["y_axis"].value

        # Draw circles (corresponding to data) on the figure.
        circles = figure.circle(
            source=source,
            x=controls["x_axis"].value,
            y=controls["y_axis"].value,
            color=create_colors(source, controls["color"].value),
            size=create_sizes(source, controls["size"].value))

        # An ad-hoc method to create a legend outside of the plot area.
        # The renderer created above is used to give context to the legend.
        # TODO: Fix the resizing bug associated with this.
        if controls["color"].value != "None":
            legend_item = bk.models.LegendItem(
                label=dict(field=controls["color"].value), renderers=[circles])
            legend = bk.models.Legend(items=[legend_item])
            figure.add_layout(legend, "below")
            figure.legend.orientation = "horizontal"

        # Add tools for interactivity to the figure.
        figure.add_tools(bk.models.TapTool())  # Required for selections.

        return figure

    # ------------------------------------------------------------------------
    # Initialize defaults and define the layout.
    #
    # The layout elements can be retrieved and updated by their assigned
    # names.
    # ------------------------------------------------------------------------
    layout = bk.layouts.layout(
        name="panel_layout",
        # Top level lists are columns, nested lists are rows.
        children=[[
            bk.layouts.column(name="control_widget",
                              children=[control_widget]),
            bk.layouts.column(name="main_figure",
                              children=[build_figure()]),
            bk.layouts.column(name="metadata_column",
                              children=[create_metadata_column(source, metadata)])
        ]])
    panel = bk.models.Panel(child=layout, title=TITLE)
    return panel
