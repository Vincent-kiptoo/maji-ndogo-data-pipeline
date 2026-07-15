"""
This Module explores the processed Maji Ndogo agricultural dataset to understand its structure, 
assess data quality, examine the distribution of variables, and identify relationships between agricultural, 
environmental, and weather-related factors that influence crop productivity. 
The insights from this analysis will guide subsequent statistical analysis and predictive modeling.
"""
import io
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from src.pipeline import create_final_dataset
from src.logging_config import get_logger

class EDAHelper:
    def __init__(self, df: pd.DataFrame | None = None) -> None:
        self.logger = get_logger(__name__)

        self.original_df = df.copy() if df is not None else None
        self.df = df.copy() if df is not None else None

        self.logger.info("EDAHelper is initialized") 
    
    def get_data(self) -> pd.DataFrame:
        """
        Loads the data and creates a working copy for analysis.
        The original data remains untouched.
        
        Returns:
            pd.DataFrame: A working copy of the data
        """
        raw_data = create_final_dataset()
        self.original_df = raw_data.copy()
        self.df = raw_data.copy()

        self.logger.info(f"The data is successfully loaded with {len(self.df)} rows")
        return self.df



    def quality_assessment(self) -> pd.Series:
        """
        This method displays the quality assessment of the DataFrame.
        It aids in fostering the understanding of the data
        
        Returns:
                pd.Series: Count of each data type in the DataFrame
        """
    
        print("DATA QUALITY ASSESSMENT")

        if self.df is None or self.df.empty:
            raise ValueError("The DataFrame is empty please check get_data() method ")
        missing_counts = self.df.isnull().sum()
        missing_values = missing_counts[missing_counts > 0]
        
        print("\nMISSING VALUES:")
        if len(missing_values) == 0:
            print("No missing values found!")
        else:
            for col, count in missing_values.items():
                pct = count / len(self.df) * 100
                print(f"  {col:20} | {count:5} missing ({pct:5.1f}%)")
        
        duplicate_count = self.df.duplicated().sum()
        
        print("\nDUPLICATE RECORDS:")
        if duplicate_count == 0:
            print("No duplicate rows found!")
        else:
            print(f"  Found {duplicate_count} duplicate rows ({duplicate_count/len(self.df)*100:.1f}%)")

        print("\nDATA TYPE COUNTS:")
        data_type_count = self.df.dtypes.value_counts()
        return data_type_count
    
    def get_categorical_columns(self) -> pd.DataFrame:
        """
        Identifies categorical columns in the DataFrame.
    
        Returns:
            pd.DataFrame: DataFrame containing names of categorical columns
        """

        if self.df is None or self.df.empty:
            raise ValueError("The DataFrame cant be empty")
        columns = self.df.select_dtypes(include=["object", 'category']).columns.to_list()
        categorical_columns = pd.DataFrame({"categorical_columns": columns})
        return categorical_columns
    
    def list_categorical_values(self, column) -> pd.DataFrame:
        """
        This method lists unique values of categorical variables
        args:
            df: the Dataframe 
            column: the colums of the categorical variables
        returns: 
            pandas DataFrame: pd.DataFrame
        """
        if self.df is None or self.df.empty:
            raise ValueError("The DataFrame cannnot be empty")
        unique_values = pd.DataFrame(self.df[column].unique(), columns=[column])
        return unique_values

    
