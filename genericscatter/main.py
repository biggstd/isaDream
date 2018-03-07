"""
#############################
Generic Scatter Visualization
#############################

.. topic:: Overview

    This Bokeh application will serve as a generic scatter plot for a range of
    chemical values.

    :Date: |today|
    :Author: **Tyler Biggs**

"""

# Standard Python package imports.


# Bokeh visualization imports.
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Select, HoverTool, TapTool, LinearInterpolator
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Div, Tabs, Panel
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
