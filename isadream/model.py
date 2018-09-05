"""Provide a base class for all parameterized ChemMD models that can be
used or displayed in a ChemMD.display.

"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------
# Generic Python imports.
import param  # Boiler-plate for controlled class attributes.
import logging
from textwrap import dedent  # Prevent indents from percolating to the user.

logger = logging.getLogger(__name__)


class ElementalNode(param.Parameterized):
    """Builds the markdown element for a single node.

    This function should not be directly called, it is used by the
    `as_markdown` property.

    """
    pass
    # @property
    # def as_markdown(self) -> str:
    # markdown_text = ""
    # # Iterate over the name and value of each parameter.
    # for name, value in self.get_param_values():
    #     if value:
    #         markdown_text += dedent(f"""\
    #             **{name}**:  {value}\n
    #         """)
    #
    # return markdown_text


class CompoundNode(param.Parameterized):
    """An base class from which all other metadata node types will
    inherit from.

    """
    #
    # def __init__(self, **params):
    #     logging.debug(f"Created CompoundNode type: {self}")
    #     # Call the param.Parameterized __init__ function.
    #     super().__init__(**params)
    #
    # @property
    # def as_markdown(self) -> str:
    #     """Return a representation of this node as a markdown formatted
    #     string.
    #
    #     Recursively parses every sub-node and calls `_build_markdown`
    #     on each one.
    #
    #     """
    #
    #     markdown_text = ""
    #     # Iterate over the name and value of each parameter.
    #     try:
    #         for name, value in self.get_param_values():
    #             if isinstance(value, list):
    #                 for val in value:
    #                     try:
    #                         markdown_text += val.as_markdown()
    #                     except Exception as error:
    #                         print(error)
    #                         markdown_text += val.as_markdown()
    #     except:
    #         pass
    #     return markdown_text
