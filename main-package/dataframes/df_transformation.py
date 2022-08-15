from functools import reduce
import pandas as pd
from datetime import datetime
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


def bin_time_of_day(data, column_to_bin, time_format='%H:%M', column_hour_label='hour'):
    """
    # Hàm này chuyển các múi giờ thành sáng, trưa, chiều, tối
    
    Hours is segmented by
    - Night (from 12 am to 5.59 am)
    - Morning (from 6 am to 11.59 am)
    - Afternoon (from 12 pm to 5.59 pm)
    - Evening (from 6 pm to 11.59 pm)
    
    ## Params
        - time_format`: injected into `datetime.strptime`
        - `column_hour_label`: this function autogenerates an `hour` column for binning, if there is an `hour` column exist, override the new column label here
    """
    returned_data = data.copy(deep=True)
    returned_data[column_to_bin] = returned_data[column_to_bin].apply(lambda x: datetime.strptime(x, time_format))
    returned_data[column_hour_label] = returned_data[column_to_bin].dt.time
    bins = [0, 6, 12, 18, 24]
    labels = ['Night', 'Morning', 'Afternoon', 'Evening']
    returned_data['timebin'] = pd.cut(returned_data[column_hour_label].dt.hour, bins, labels = labels, right = False)
    return returned_data


def group_minutes_to_hour(data, time_column):
    """
    Return bin_hours column có dạng [h0,h1)
    vd: 9h -> 9h59 => [9, 10)
    """
    new_data = data.copy(deep=True)
    bins = list(range(0, 25))
    new_data['bin_hours'] = pd.cut(new_data[time_column].dt.hour, bins, right = False)
    return new_data    


def weekday_weekend_split(df, day_of_week_column:str, weekend_label:list, return_weekday=True):
    """
    # Hàm này dùng để split function to weekdays and weekends
    """
    weeken_boolean = df[day_of_week_column].isin(weekend_label)
    time_weekend = df[weeken_boolean]
    if return_weekday:
        time_weekdays = df[~weeken_boolean]
        return time_weekdays, time_weekend
    return time_weekend

