

import pandas as pd
import numpy as np

def data_clean(df):
    fill_na_other_list = ['installer', 'funder','public_meeting','scheme_management','permit']
    del_list = ['recorded_by', 'extraction_type_group','extraction_type_class', 'payment', 'quantity_group', 'source', 'source_class', 'id', 'num_private', 'quantity_group','waterpoint_type_group', 'wpt_name', 'scheme_name', 'amount_tsh']
    
    for i in fill_na_other_list:
        df[i].fillna('other', inplace = True)
    df.drop(columns =[del_list], inplace = True)  
    df.population.replace(0,df.groupby(['district_code']).population.mean(), inplace = True)
    df.status_group.replace('functional needs repair','non functional', inplace = True)
    
    df['region_and_code'] = df['region'] + df['region_code'].map(str)
    df.drop(columns = ['region', 'region_code'], inplace = True)
    
    i = df.construction_year.median()
    df.construction_year.replace(0,i,inplace=True)
    
    j = df.groupby(['basin']).gps_height.mean()
    df.gps_height.replace(0,j, inplace = True)
    
    cols = [i for i in df.columns if type(df[i].iloc[0]) == str]
    df[cols] = df[cols].where(df[cols].apply(lambda x: x.map(x.value_counts())) > 50,"other")
 
    df['year'] = df.date_recorded.str[:4]
    df['month'] = df.date_recorded.str[-4]
    df.drop(columns = ['date_recorded'], inplace = True)
    df['length_operation'] = df.year.map(int) - df.construction_year.map(int)
    