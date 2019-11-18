#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 07:12:51 2019

@author: ladvien
"""
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

class FeatureEngineer:
    
    def __init__(self):
        pass
    
    def fragment_date(self, df, feature_name, drop_parent = True):
        """
            df: DataFrame, the dataframe containing the feature to fragment.
            feature_name: str, the name of the feature column.
            drop_parent: boolean, defualt: True, if True the date_feture will be dropped from
                         the dataframe after adding the fragmented columns.
            
            Procedure:
                1. Get average length of date as string
                2. Force feature to datime
                3. Add columns 'feature_year,' 'feature_month,' and 'feature_day.'
                4. If datetime, add columns 'feature_hour,' 'feature_minute,' and 'feature_day'
        """
        
        print(f'Fragmenting: {feature_name}')

        feature_name_len_min = df[feature_name].astype(str).str.len().min()
        
        try:
            df[feature_name] = pd.to_datetime(df[feature_name], format='%Y-%m-%d %H:%M:%S')
        except:
            print(f'Failed to cast feature to datetime. Feature is type: {df[feature_name].dtype}')
            return 
        
        df[feature_name + '_year'] = df[feature_name].dt.year
        df[feature_name + '_month'] = df[feature_name].dt.month
        df[feature_name + '_day'] = df[feature_name].dt.day
        
        if feature_name_len_min > 10: # Timestamp length.
            df[feature_name + '_hour'] = df[feature_name].dt.hour
            df[feature_name + '_minute'] = df[feature_name].dt.minute
            df[feature_name + '_second'] = df[feature_name].dt.second

        if drop_parent:
            df.drop(feature_name, axis = 1, inplace = True)

    
    def fragment_dates(self, df, feature_names, drop_parent = True):
        """
            df: DataFrame, the dataframe containing the feature to fragment.
            feature_names: [str], a list containing the names of the feature columns.
            drop_parent: boolean, defualt: True, if True the date_feture will be dropped from
                         the dataframe after adding the fragmented columns.
            
            Procedure:
                Loops through the feature_names array and does the following
                1. Get average length of date as string
                2. Force feature to datime
                3. Add columns 'feature_year,' 'feature_month,' and 'feature_day.'
                4. If datetime, add columns 'feature_hour,' 'feature_minute,' and 'feature_day'
        """
        
        for feature_name in feature_names:
            self.fragment_date(df, feature_name, drop_parent)

    def create_days_between_feature(self, df, feature_name_one, feature_name_two):
        """
            df: DataFrame, the dataframe containing the dates to calculate days between.
            feature_name_one: str, the name of the primary feature column.
            feature_name_two: str, the name of the secondary feature column.
            
            Procedure:
                1. Ensure both features are pd.datetime
                2. Subtract secondary date from primary and cast to datetime.days
                3. Add this as a column to dateframe as, 'days_between_primary_and_secondary.'
        """
        if is_datetime(df[feature_name_one]) and is_datetime(df[feature_name_two]):
            df[f'days_between_{feature_name_one}_and_{feature_name_two}'] = \
                (df[feature_name_one] - df[feature_name_two]).dt.days
        else:
            print(f'Excepted datetime features, received 1: {df[feature_name_two].dtype} 2:{df[feature_name_two].dtype}')
            return

            
            
            
        