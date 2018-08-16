"""

"""

# Path hack to allow imports from the parent directory.
import sys, os

sys.path.insert(0, os.path.abspath('../isadream/'))

# Data science imports.

# Visualization imports.
import bokeh as bk
import bokeh.models
import bokeh.layouts
import bokeh.palettes
import bokeh.plotting
import bokeh.transform

# Local isadream imports.
from isadream import helpers, modelUtils

x_groups = (('Total Aluminate Concentration', 'Molar', ("Al",)),
            ('Counter Ion Concentration', 'Molar', ("Na+", "Li+", "Cs+", "K+")),
            ('Counter Ion', 'Species', ("Na+", "Li+", "Cs+", "K+",)),
            ('Base Concentration', 'Molar', ("OH-",)))

y_groups = (('27 Al ppm', 'ppm', ("Al",)),)

try:

    json_paths = helpers.get_session_json_paths(bk.plotting.curdoc)

    nodes = helpers.create_drupal_nodes(json_paths)

    main_df, meta_df = helpers.prepare_bokeh_dicts(x_groups, y_groups, nodes)

    columns, discrete, continuous, quantileable = helpers.categorize_columns(
        main_df, x_groups, y_groups)

    x_keys, = helpers.get_group_keys(x_groups)
    y_keys = helpers.get_group_keys(y_groups)

    source = bk.models.ColumnDataSource(main_df)


except Exception as inst:
    print(type(inst))
    print(inst)
    demo_base_path = modelUtils.SIPOS_DEMO

    json_paths = [modelUtils.SIPOS_DEMO, ]

    nodes = helpers.create_drupal_nodes(json_paths)

    main_df, meta_df = helpers.prepare_bokeh_dicts(
        x_groups, y_groups, nodes)

    columns, discrete, continuous, quantileable = helpers.categorize_columns(
        main_df, x_groups, y_groups)

    x_keys = helpers.get_group_keys(x_groups)
    y_keys = helpers.get_group_keys(y_groups)

    source = bk.models.ColumnDataSource(main_df)


def build_metadata_paragraph(parent_key=None, assay_key=None, sample_key=None):
    """

    :return:
    """
    if all(key is None for key in (parent_key, assay_key, sample_key)):
        return bk.models.widgets.Paragraph(text="No data point selected.",
                                           name='metadata_paragraph')

    else:
        keys = filter(None, (parent_key, assay_key, sample_key))
        selected_information = str([meta_df[key].values for key in keys])
        paragraph = bk.models.widgets.Paragraph(
            name='metadata_paragraph',
            text=selected_information)

        return paragraph


def build_metadata_paragraphs(index_selections=None):
    selected_paragraphs = list()

    for index in index_selections:
        active_parent = source.data.get('parent_node')[index]
        active_assay = source.data.get('assay_node')[index]
        active_study = source.data.get('sample_node')[index]

        selected_point_paragraph = build_metadata_paragraph(
            active_parent, active_assay, active_study)

        selected_paragraphs.append(selected_point_paragraph)

    return selected_paragraphs


def build_metadata_column(paragraphs):
    return bk.layouts.column(name='metadata_column',
                             children=paragraphs)


def tap_select_callback(attr, old, new):
    """The callback function for when a user uses the TapTool to
    select a single data point.

    """
    selected_indexes = new['1d']['indices']

    paragraphs = build_metadata_paragraphs(selected_indexes)

    metadata_column = bk.plotting.curdoc().get_model_by_name('metadata_column')
    metadata_column.children = paragraphs


def update_document(attr, old, new):
    update_bk_cds()

    panels = create_tab_panels()

    bk_figure = bk.plotting.curdoc().get_model_by_name('figure_tab')
    bk_figure.tabs = panels


def initialize_tabs():
    update_bk_cds()
    panels = create_tab_panels()
    tabs = bk.models.widgets.Tabs(tabs=panels, name='figure_tab')

    return tabs


def build_figure(axis_type):
    figure = bk.plotting.figure(
        name='primary_figure',
        width=600,
        x_axis_type=axis_type)

    sizes = 7

    if size.value != 'None':
        size_scale = bk.models.LinearInterpolator(
            x=[min(source.data[size.value]), max(source.data[size.value])],
            y=[2, 15]
        )
        sizes = dict(field=size.value, transform=size_scale)

    if color.value != 'None':
        colors = bk.transform.factor_cmap(
            field_name=color.value,
            palette=bk.palettes.Category10[len(source.data[color.value].unique())],
            factors=sorted(source.data[color.value].unique()),
        )
    else:
        colors = "#31AADE"

    rend = figure.circle(
        name='figure_renderer',
        source=source,
        x='x',
        y='y',
        color=colors,
        size=sizes,
    )

    if color.value is not "None":
        legend = bk.models.Legend(
            items=[bk.models.LegendItem(label=dict(field=color.value),
                                        renderers=[rend])])
        figure.add_layout(legend, "below")
        figure.legend.orientation = "horizontal"

    x_title = x_selector.value
    y_title = y_selector.value

    figure.xaxis.axis_label = x_title
    figure.yaxis.axis_label = y_title

    # figure.add_tools(build_hover_tool())
    figure.add_tools(bk.models.TapTool())

    return figure


def build_panel(axis_type):
    figure = bk.layouts.row(build_figure(axis_type))
    return bk.models.widgets.Panel(child=figure, title=axis_type)


def create_tab_panels():
    """Update the figure."""
    tab_panels = list()
    for axis_type in ['linear', 'log']:
        panel = build_panel(axis_type)
        tab_panels.append(panel)

    return tab_panels


def update_bk_cds():
    """Updates the Bokeh column data source."""
    source.data = dict(
        x=main_df[x_selector.value],
        y=main_df[y_selector.value],
    )

    for col in main_df.columns:
        source.add(data=main_df[col], name=col)


x_selector = bk.models.Select(title="X Axis", options=continuous, value=continuous[0])
x_selector.on_change('value', update_document)

y_selector = bk.models.Select(title="X Axis", options=y_keys, value=y_keys[0])
y_selector.on_change('value', update_document)

color = bk.models.Select(title='Color', value='None', options=['None'] + discrete)
color.on_change('value', update_document)

size = bk.models.Select(title='Size', value='None', options=['None'] + continuous)
size.on_change('value', update_document)

controls = bk.layouts.widgetbox([x_selector, y_selector, color, size])

source.on_change('selected', tap_select_callback)

layout = bk.layouts.layout(
    children=[
        bk.models.widgets.Div(text="<h1>Aluminate CrossFilter</h1>"),
        [controls, initialize_tabs()],
        build_metadata_column([build_metadata_paragraph()])
    ],
    sizing_mode='fixed'
)

bk.plotting.curdoc().add_root(layout)
bk.plotting.curdoc().title = "27 Al NMR Crossfilter"
