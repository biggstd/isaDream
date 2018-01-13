from nmr_demo_sa import *
from ontologies import *


if __name__ == '__main__':
    invest = build_nmr_output()
    print(jsonify_investigation(invest))
