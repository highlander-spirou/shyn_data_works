from functools import reduce
import pandas as pd
from typing import Optional, Iterable

def get_df_categories_in_year(df, year:int, index:Optional[str]=None):
    """
    # Hàm này dùng để lấy các cột của index column theo năm   
    - Must have a column `year` in the dataframe
    
    ### Params
    df: (shape) => | year || region || wine || champagne
    
    ### Return:
    | region || wine_2010 || beer_2010 || champagne_2010
    
    """
    returned_df = df.copy(deep=True)
    returned_df = returned_df.query("year == @year")
    if index is not None:
        returned_df.set_index(index, inplace=True)
    returned_df.columns.tolist()
    new_column_list = {}
    for i in returned_df:
        new_column_list[i] = i + '_' + str(year)
    returned_df.rename(columns=new_column_list, inplace=True)
    return returned_df

def reduce_inner_join(list_df:Iterable[pd.DataFrame], on:str, index:Optional[str]=None):
    """
    # Hàm này dùng reduce để SQL-inner-join nhiều tables
    - Has the same restrictions as SQL joins
    """
    df_merged = reduce(lambda left,right: pd.merge(left,right,on=[on], how='inner'), list_df)
    if index is not None:
        df_merged.set_index(index, inplace=True)
    return df_merged