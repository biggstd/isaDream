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
import pandas as pd
import json
import os
import itertools
from pandas.io.json import json_normalize


json_path = '../isadream/demo_data/demo_json/sipos_2006_talanta_nmr_figs.json'
BASE_PATH = '../isadream/demo_data/'


def normalize(x):
    if isinstance(x, dict):
        keys = x.keys()
        values = (normalize(i) for i in x.values())
        for i in itertools.product(*values):
            yield (dict(zip(keys, i)))
    elif isinstance(x, list):
        for i in x:
            yield from normalize(i)
    else:
        yield x


def load_csv(path, base_path=BASE_PATH):
    csv_path = os.path.join(base_path, path)
    return pd.read_csv(csv_path, skiprows=1, header=None)





with open(json_path) as jp:
    sjson = json.load(jp)



assay_df = json_normalize(list(normalise(sjson['assays'])))
study_sample_df = json_normalize(list(normalise(sjson['studySamples'])))
full_df = json_normalize(list(normalise(sjson)))
