from functools import reduce
import pandas as pd

from typing import Iterable, Optional


def reduce_inner_join(list_df:Iterable[pd.DataFrame], on:str, index:Optional[str]=None):
    """
    # Hàm này dùng reduce để SQL-inner-join nhiều tables
    - Has the same restrictions as SQL joins
    """
    df_merged = reduce(lambda left,right: pd.merge(left,right,on=[on], how='inner'), list_df)
    if index is not None:
        df_merged.set_index(index, inplace=True)
    return df_merged