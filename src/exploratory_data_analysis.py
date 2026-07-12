"""
This Module explores the processed Maji Ndogo agricultural dataset to understand its structure, 
assess data quality, examine the distribution of variables, and identify relationships between agricultural, 
environmental, and weather-related factors that influence crop productivity. 
The insights from this analysis will guide subsequent statistical analysis and predictive modeling.
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from src.pipeline import create_final_dataset
from logging_config import get_logger


class EDAHelper:
    def __init__(self, df = None) -> None:
        self.logger = get_logger(__name__)

        if df is not None:
            self.original_df = df.copy()
        else:
            self.original_df = None

        self.df = None
        self.logger.info("EDAHelper is initialized")
    
    def get_data(self, df) -> pd.DataFrame:
        """
        Loads the data and creates a working copy for analysis.
        The original data remains untouched.
        
        Returns:
            pd.DataFrame: A working copy of the data
        """






    

    def get_data(self) -> pd.DataFrame:
        """
        Loads the data for the downstream of further analysis
        args:

        """
        self.logger.info("Loading the dataset for downstream of EDA analysis")
        self.df = create_final_dataset()
        return self.df
    def quality_assesment(self, df) -> pd.DataFrame |  None:
        """
        This method displays the quality assessment of the DataFrame.
        It aids in fostering the understanding of the data
        
        Args:
            df (pd.DataFrame): The DataFrame to assess
        returns pd.DataFrame
        """
    
        print("DATA QUALITY ASSESSMENT")
        
        missing_counts = df.isnull().sum()
        missing_values = missing_counts[missing_counts > 0]
        
        print("\n MISSING VALUES:")
        if len(missing_values) == 0:
            print("No missing values found!")
        else:
            for col, count in missing_values.items():
                pct = (count / len(df) * 100)
                print(f"  {col:20} | {count:5} missing ({pct:5.1f}%)")
        
        duplicate_count = df.duplicated().sum()
        
        print("\nDUPLICATE RECORDS:")
        if duplicate_count == 0:
            print("No duplicate rows found!")
        else:
            print(f"  Found {duplicate_count} duplicate rows ({duplicate_count/len(df)*100:.1f}%)")

        print("\n DATA TYPE COUNTS:")
        data_type_count = df.dtypes.value_counts()
        return data_type_count
    
    def get_categorical_columns(self, df) -> pd.DataFrame:
        columns = df.select_dtypes(str).columns.to_list()
        categorical_columns = pd.DataFrame(columns, columns=["categorical_columns"])
        return categorical_columns

    
