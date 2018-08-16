import uuid
from pydot import Node, Edge

factor_record = ("{<f0> Elemental Factor    | "
                 "{<f1> Factor Type         | <f2> Reference } |"
                 "{<f3> Decimal Value       | <f4> Value}      |"
                 "{<f5> String Value        | <f6> Value}      |"
                 "{<f7> Reference Value     | <f8> Reference}  |"
                 "{<f9> Unit Value          | <f10> Reference} |"
                 "{<f9> Data Reference      | <f10> Reference}  "
                 "}")

species_record = ("{<f0> Elemental Species Factor   | "
                  "{<f1> Species Reference          | <f2> Reference } |"
                  "{<f3> Stoichiometry              | <f4> Value}      "
                  "}")

information_record = ("{<f0> Elemental Information | { <f1> Key(s) | <f2> Values } }")

comment_record = ("{<f0> Elemental Comment      | "
                  "{<f1> Name                   | <f2> Value }    |"
                  "{<f3> Body                   | <f4> Value }    "
                  "}")

data_record = ("{<f0> Elemental Datafile  | "
               "{<f1> Name | <f2> Value } |"
               "{<f3> Data | <f4> Index Dictionary } "
               "}")

elemental_labels = {
    "factor": factor_record,
    "species": species_record,
    "info": information_record,
    "comment": comment_record,
    "data": data_record,
}


def elemental_node(node_type):
    """Returns a unique record node of the requested type."""
    return Node(str(uuid.uuid4()), label=elemental_labels[node_type],
                shape="record", rankdir="LR")


def container_node(node_type):
    """Returns a unique container node of the requested type."""
    return Node(str(uuid.uuid1()), label=node_type, color="blue")
