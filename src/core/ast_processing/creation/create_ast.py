import rpy2.robjects as ro
import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


def get_ast_from_file(path):
    try:
        ro.r(f'parsed <- parse("{path}")')
        ast = ro.r('getParseData(parsed)')
        with localconverter(ro.default_converter + pandas2ri.converter):
            df = ro.conversion.rpy2py(ast)
    # TODO better exception handling
    except Exception:
        df = pd.DataFrame({'A': []})

    return df
