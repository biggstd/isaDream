"""Compound Classes of the package.

These are classes which are composed of elemental, compound, or a combination
of the two.

"""

# Standard library imports.
from textwrap import dedent  # Prevent indents from percolating to the user.
import collections  # For sub-classing Python built-ins.

import param  # Boiler-plate for controlled class attributes.

# Local project imports.
from .elemental import (Factor, SpeciesFactor, Comment)
from .. import modelUtils


class SourceNode(param.Parameterized):
    """Model for a single Source.

    A source is similar to a sample.

    # TODO: Consider adding nested sources.
    """

    source_name = param.String(
        allow_None=False,
        doc=dedent("""\
        User given name of this source.
        """)
    )

    species = param.List(
        allow_None=False,
        class_=SpeciesFactor,
        doc=dedent("""\
        A list of species objects that this source models.
        """)
    )

    factors = param.List(
        allow_None=True,
        class_=Factor,
        doc=dedent("""\
        A list of factor objects that describe this source.
        """)
    )

    comments = param.List(
        allow_None=True,
        class_=Comment,
        doc=dedent("""\
        A list of comment objects that describe this source.
        """)
    )

    @property
    def all_factors(self):
        """Get all factors associated with this source.

        This function should handle nested sources in the future with only
        minor modifications.

        """
        return collections.ChainMap(modelUtils.get_all_elementals(self, 'factors'))

    @property
    def all_species(self):
        """Get all species associated with this source.

        This function should handle nested sources with only minor modifications.

        :return:
        """
        return modelUtils.get_all_elementals(self, 'species')


class SampleNode(param.Parameterized):
    """Model for a physical of simulated sample.

    A Sample object is a collection of species and factors.

    """

    sample_name = param.String(
        allow_None=False,
        doc=dedent("""\
        The user supplied name of this sample.
        """)
    )

    factors = param.List(
        allow_None=True,
        class_=Factor,
        doc=dedent("""\
        Factors that apply to only to this sample.
        """)
    )

    species = param.List(
        allow_None=False,  # There must at least be a reference for a sample to be of use.
        class_=SpeciesFactor,
        doc=dedent("""\
        A list of species that are contained within this source.
        """)
    )

    sources = param.List(
        allow_None=True,
        class_=SourceNode,
        doc=dedent("""\
        A list of sources that are contained within this sample.

        If supplied, factors and species from sources will apply to this assay instance
        as well. If matching factors are found, the highest ranking source or sample
        factor will take precedence.
        """)
    )

    comments = param.List(
        allow_None=True,
        class_=Comment,
        doc=dedent("""\
        A list of comment objects that pertain to this sample.
        """)
    )

    @property
    def all_factors(self):
        """Recursively find all factors of this assay.

        This includes all those factors and species within sources as well.
        See the ` modelUtils.get_all_elementals` documentation for details.

        """
        return modelUtils.get_all_elementals(self, 'factors')

    @property
    def all_species(self):
        """Recursively find all species of this assay.

        This includes all those factors and species within sources as well.
        See the ` modelUtils.get_all_elementals` documentation for details.

        """
        nodes_out = list()
        for species in set(modelUtils.get_all_elementals(self, 'species')):
            if species.species_reference is not None and species.stoichiometry is not None:
                nodes_out.append(species)

        return nodes_out

    @property
    def unique_species(self):
        """Get all unique species contained within this assay.

        This prevents sources from adding duplicate species.

        """
        return set((s.species_reference for s in self.all_species))

    @property
    def all_sources(self):
        """Get all sources contained within this assay.

        This includes nested sources.

        :return: A list of Source model objects.
        """
        return modelUtils.get_all_elementals(self, 'sources')

    def query(self, query_terms):
        """Perform a simple query on the values of this assay instance, returns a boolean.

        :return: `True` if a query term is found, `False` otherwise.
        """
        query_terms = modelUtils.ensure_list(query_terms)
        if any(species.query(term)
               for term in query_terms
               for species in self.all_species):
            return True


class AssayNode(param.Parameterized):
    """Model for single assay / experiment - contains a datafile and all
    metadata pertaining to that file.

    This model is used by the `isadream.io` module to create data frames
    and metadata dictionaries. This model should be considered the 'core'
    of this model set.

    """

    assay_datafile = param.String(
        allow_None=True,  # There could technically be a single point uploaded.
        doc=dedent("""\
        The filename of the data file which this assay instance models.
        
        The base-path of where this file is actually stored is not considered here.
        """)
    )

    assay_title = param.String(
        allow_None=False,
        doc=dedent("""\
        The user-supplied title of this assay.
        """)
    )

    factors = param.List(
        allow_None=True,
        class_=Factor,
        doc=dedent("""\
        A list of Factor objects that apply to this assay.
        """)
    )

    samples = param.List(
        allow_None=True,
        class_=SampleNode,
        doc=dedent("""\
        A list of Sample objects that are used within this assay.
        """)
    )

    comments = param.List(
        allow_None=True,
        class_=Comment,
        doc=dedent("""\
        A list of Comment objects that describe this assay.
        """)
    )

    parental_factors = param.List(
        allow_None=True,
        class_=Factor,
        doc=dedent("""\
        A list of Factor objects from the parent DrupalNode of this assay.
        
        All of these factors apply to this assay.
        """)
    )

    parental_samples = param.List(
        allow_None=True,
        class_=SampleNode,
        doc=dedent("""\
        A list of Sample objects from the parent DrupalNode of this assay.
        
        All of these Samples are used by this assay.
        """)
    )

    parental_info = param.Dict(
        allow_None=True,
        doc=dedent("""\
        The metadata information of the parent DrupalNode of this assay.
        """)
    )

    parental_comments = param.List(
        allow_None=True,
        class_=Comment,
        doc=dedent("""\
        A list of comments from the parent DrupalNode of this assay.
        """)
    )


class DrupalNode(param.Parameterized):
    """Model for a single Drupal content node.

    Much of this class is declarative, with the Param package doing all of the
    heavy-lifting in the background.

    """

    title = param.String(
        allow_None=False,
        doc=dedent("""\
        User supplied title of the Drupal Node or experiment.

        This model contains all the information concerning a given Drupal Node.
        """)
    )

    info = param.Dict(
        allow_None=True,
        doc=dedent("""\
        A set of key-value pairs of information concerning this experiment. 

        This can be any arbitrary set of key-value paris.
        """)
    )

    assays = param.List(
        allow_None=True,
        class_=AssayNode,
        doc=dedent("""\
        A list of Assay models that contain all core data components.
        """)
    )

    factors = param.List(
        allow_None=True,
        doc=dedent("""\
        A list of Factor models that pertain to all assays contained by this
        DrupalNode instance.
        """)
    )

    samples = param.List(
        allow_None=True,
        doc=dedent("""\
        A list of Sample models that are used by all assays contained by this
        DrupalNode instance.
        """)
    )

    comments = param.List(
        allow_None=True,
        doc=dedent("""\
        A list of Comment models that apply to all of the assays contained by
        this DrupalNode instance.
        """)
    )
