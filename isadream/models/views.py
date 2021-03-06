'''Viewer classes for the IDREAM data model.

This class takes one or more models and prepares the data for visuzlization by
a Bokeh application.

'''

# General Python imports.
import abc

# Data Science imports.

# Visualization / Bokeh imports.

# Local imports.
# from .model import Model


class View(abc.ABC):
    '''A base class for viewing data.

    This is an abstract base class, and is not usefull to instanciate
    on its own.

    A view will be generated by information by a controller, will have
    data passed to it in the form of one or more Model classes.

    Also note that classes defined in this way do not actually produce
    visualizations. Rather they are an object-oriented way of oranizing
    the functions required to build a Bokeh application for the IDREAM
    database.

    '''

    @abc.abstractmethod
    def __init__(self, key_dims, val_dims, models):
        '''Basic Veiw initialization.

        This is an abstract implementation for all future view applications.
        It is not usefull, nor should it be possible, to instanciate this
        class on its own.

        The attributes and functions defined within this class are 'required'
        (under the requirements for an IDREAM visuzlization, not a Bokeh app.)
        to be defined for a visualization to work. The layout and application
        should be built as directory-based Bokeh applications per the
        documentation.

        # TODO: Add documentation links.

        Args:
            key_dims (tuple[str]): The key dimensions of the view. These
                are the values that will be assignable to the X-axis.
            val_dims (tuple[str]): The value dimensions of the view. Such
                values will be assignable to the Y-axis.
            models (tuple[`Model`]): Model(s) assigned to this visualization.

        Values or columns within `key_dims` and `val_dims` may also be drawn
        with different glyphs (ie. different colors, sizes, etc.). These will
        likely have to be defined on a per-visualization basis.

        '''
        self.key_dims = key_dims
        self.val_dims = val_dims
        self.models = models

    @staticmethod
    def prepare_dataframe_columns(data_frame, quantile_size=10):
        '''Group columns for a visualization.
        '''
        columns = sorted(data_frame.columns)
        discrete = [col for col in columns if data_frame[col].dtype == object]
        continuous = [col for col in columns if col not in discrete]
        quantileable = [col for col in continuous
                        if len(data_frame[col].unique()) > quantile_size]
        # TODO: Break these into different properties? Perhaps of the Model class.
        return columns, discrete, continuous, quantileable

    @staticmethod
    @abc.abstractmethod
    def build_column_data_source():
        '''Builds a column data source from one or more ISADREAM.Model objects.
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def update_data():
        '''Updates a column data source.
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def tap_select_callback():
        '''Callback for when a user selects a point.
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def build_hover_tool():
        '''Callback for when a user selects a point.
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def create_figure():
        '''The primary figure of this application.
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def update_plot():
        '''The function to be run upon an update call.
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def build_metadata_div():
        '''Function that constructs the metadata Div element for a selected point.
        '''
        pass


# TODO: Should these be methods?
"""
class NMR(View):
    '''NMR Viewer class. To be moved.

    '''

    def __init__(self, model):
        pass


class ConcentrationRatio(View):
    '''Ratio Viewer class. To be moved.

    '''

    def __init__(self, model):
        pass
"""
