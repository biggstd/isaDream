"""
################################
Literature NMR Data - Bokeh Demo
################################

This application is divorced from any database. Rather, it
simply loads a set of demo metadata files.

"""

# General Imports
import pandas as pd

# Bokeh imports
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Select, HoverTool, TapTool, LinearInterpolator
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Div, Tabs, Panel
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap

# isaDream imports.
from isadream.nmr_demo_sa import *

COLORS = Category10
SIZES = list(range(6, 22, 3))

# Simulate the return from a database query.
# Build the investigation object.
invest = build_nmr_output()

# Run the search simulation.
matching_studies = get_studies_by_design_descriptor(invest, al_27_nmr)

# Convert the returned list of studies to pandas dataframes and python
# dictionaries for use in Bokeh's columnDataSource.
data_frame, metadata_dict = build_data_md_pair(matching_studies)

# Create some sample derivative columns.
data_frame = create_ratio_column(data_frame, 'molarity hydroxide', 'Aluminate Molarity')
data_frame = create_ratio_column(data_frame, 'Aluminate Molarity', 'molarity hydroxide')

# Get the column names for use in the selectors.
columns = sorted(data_frame.columns)
discrete = [x for x in columns if data_frame[x].dtype == object]
continuous = [x for x in columns if x not in discrete]
quantileable = [x for x in continuous if len(data_frame[x].unique()) > 20]

# Assign the columnDataSources.
source = ColumnDataSource()


def update_data():
    """Upodates the Bokeh ColumnDataSource with subsets of data
    collected from a search result."""

    # Set the X and Y values to those selected by the user.
    source.data = dict(
        x=data_frame[x_selector.value],
        y=data_frame[y_selector.value],
    )

    # Iterate over the entire dataframe generated by the 'search'
    # function, and add all of these generated columns to the
    # Bokeh ColumnDataSource.
    for col in list(data_frame):
        source.add(data=data_frame[col], name=col)

    # print(list(data_frame))
    # print(data_frame)


def tap_select_callback(attr, old, new):
    """The callback function for when a user uses the TapTool to
    select a single data point.
    """
    new_index = new['1d']['indices'][0]
    study_key = source.data['study_ID'][new_index]
    assay_key = source.data['assay_ID'][new_index]
    # print(study_key, assay_key)
    layout.children[1].children[2] = build_metadata_paragraph(
        study_key, assay_key)


def build_hover_tool():
    """Constructs a Bokeh HoverTool instance based on current selections.
    """
    hover = HoverTool(
        tooltips=[
            ('X, Y', '($x, $y)'),
            ('ppm Al', '@{ppm aluminum}'),
            ('[OH-]', '@{molarity hydroxide}'),
            ('[Al] total', '@{Aluminate Molarity}')
        ]
    )
    return hover


def create_figure():
    """
    Create the bokeh plot.
    """
    update_data()

    panels = []

    for axis_type in ["linear", "log"]:

        fig = figure(
            name='primary_figure',
            width=600,
            x_axis_type=axis_type
        )

        sizes = 7
        if size.value != 'None':
            size_scale = LinearInterpolator(
                x=[min(source.data[size.value]), max(source.data[size.value])],
                y=[2, 15]
            )
            sizes = dict(field=size.value, transform=size_scale)

        if color.value != 'None':
            colors = factor_cmap(
                field_name=color.value,
                # palette=Category10[len(source.data[color.value].unique())],
                palette=Category10[10],
                factors=sorted(source.data[color.value].unique())
            )
        else:
            colors = "#31AADE"

        fig.circle(
            source=source,
            x='x',
            y='y',
            color=colors,
            size=sizes,
            legend=color.value,
        )

        fig.legend.location = "bottom_left"

        x_title = x_selector.value
        y_title = y_selector.value

        fig.xaxis.axis_label = x_title
        fig.yaxis.axis_label = y_title

        fig.add_tools(build_hover_tool())
        fig.add_tools(TapTool())

        panel = Panel(child=fig, title=axis_type)
        panels.append(panel)

    tabs = Tabs(tabs=panels, width=620)

    return tabs


def update_plot(attr, old, new):
    """
    Define the function to be run upon an update call.
    """
    layout.children[1].children[1] = create_figure()
    pass


def format_assay_text(study, assay):
    """Prepares the ISA assay object for easy reading in an HTML
    format."""
    out_str = (
        format_publication_html(study, assay) +
        format_protocol_html(study, assay) +
        format_material_html(study, assay)
    )
    return out_str


def format_publication_html(study, assay):

    out_html = "<h4>Publications:</h4>"

    for pub in study.publications:
        out_html += (
            '<strong>Title</strong>: {0}<br />'
            '<strong>DOI</strong>: '
            '<a href="https://doi.org/{1}">{1}</a><br />'
            .format(
                pub.title,
                pub.doi
            )
        )
    return out_html


def format_protocol_html(study, assay):

    out_html = "<h4>Experiment Protocol(s):</h4>"

    for proc in assay.process_sequence:
        out_html += (
            '<strong>Protocol Name</strong>: {0}<br />'
            .format(
                proc.executes_protocol.name,
            )
        )
        for param in proc.parameter_values:
            # Check to see if the value is an OntologyAnnotation
            # with a term string that we should print.
            if hasattr(param.value, 'term'):
                param_val = param.value.term
            else:
                param_val = param.value

            out_html += (
                '<strong>{0}</strong>: {1} {2}<br />'
                .format(
                    param.category.parameter_name.term,
                    param_val,
                    param.unit.term
                )
            )
    return out_html


def format_material_html(study, assay):

    out_html = "<h4>Sample Information:</h4>"

    for sam in assay.samples:
        out_html += (
            '<strong>Sample Name: </strong>{0}<br />'
            '<strong>Derives From</strong>:<br />'
            .format(
                sam.name,
            )
        )
        for sor in sam.derives_from:
            out_html += '<em>{0}</em><br />'.format(sor.name)

            for char in sor.characteristics:

                if hasattr(char.unit, 'term'):
                    out_html += '{0} {1}: {2}<br />'.format(
                        chr(8226), char.value, char.unit.term
                    )
                else:
                    out_html += '{0} {1}<br />'.format(
                        chr(8226), char.value
                    )

    return out_html


def build_metadata_paragraph(study_key=None, assay_key=None):
    """Constructs an HTML paragraph based on a given key."""
    # if key is None:
    if all(v is None for v in [study_key, assay_key]):
        return Div(
            text="No data point selected.",
            width=300,
        )
    else:
        active_study = metadata_dict[study_key]
        active_assay = metadata_dict[assay_key]
        new_paragarph = Div(
            text=format_assay_text(active_study, active_assay),
            width=300,
        )
        return new_paragarph


# HTML Elements ---------------------------------------------------------------
title_div = Div(text="<h1>Aluminate CrossFilter</h1>")

# Controls and Selectors ------------------------------------------------------
source.on_change('selected', tap_select_callback)

x_selector = Select(title='X Axis', options=continuous, value=continuous[0])
x_selector.on_change('value', update_plot)

y_selector = Select(title='Y-Axis', options=continuous, value=continuous[1])
y_selector.on_change('value', update_plot)

color = Select(title='Color', value='None', options=['None'] + discrete)
color.on_change('value', update_plot)

size = Select(title='Size', value='None', options=['None'] + continuous)
size.on_change('value', update_plot)

controls = widgetbox([x_selector, y_selector, color, size])

layout = layout(
    children=[
        title_div,
        [controls, create_figure(), build_metadata_paragraph()],
    ],
    sizing_mode='fixed'
)

curdoc().add_root(layout)
curdoc().title = "27 Al NMR Crossfilter"
