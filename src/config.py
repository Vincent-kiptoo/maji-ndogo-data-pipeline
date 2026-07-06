"""
Configuration module for the Maji Ndogo data pipeline.

This module centralizes all configuration parameters used throughout the pipeline,
including database connection strings, SQL queries, data transformation rules, 
CSV sources, and regex patterns for data extraction and validation.

The configuration follows a single-source-of-truth approach, allowing easy updates
to pipeline behavior without modifying core pipeline logic.
"""

# DATABASE CONFIGURATION
db_path = "sqlite:///data/Maji_Ndogo_farm_survey_small.db"

# SQL QUERY CONFIGURATION

sql_query = """
SELECT *
FROM geographic_features
LEFT JOIN weather_features USING (Field_ID)
LEFT JOIN soil_and_crop_features USING (Field_ID)
LEFT JOIN farm_management_features USING (Field_ID)
"""

# DATA TRANSFORMATION CONFIGURATION
columns_to_rename = {"Annual_yield": "Crop_type", 
                     "Crop_type": "Annual_yield"}


values_to_rename = {
        'cassaval': 'cassava',
        'wheatn': 'wheat',
        'teaa': 'tea'
    }

# EXTERNAL DATA SOURCES (CSV URLs)
weather_mapping_csv = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv"
weather_csv_path = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv"

# REGEX PATTERNS FOR DATA EXTRACTION
regex_patterns = {
    'Rainfall': r'(\d+(\.\d+)?)\s?mm',
     'Temperature': r'(\d+(\.\d+)?)\s?C',
    'Pollution_level': r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
    }

# CENTRALIZED CONFIGURATION DICTIONARY
config_params = {
    "db_path": db_path,
    "sql_query": sql_query,
    "columns_to_rename": columns_to_rename,
    "values_to_rename": values_to_rename,
    "weather_mapping_csv": weather_mapping_csv,
    "weather_csv_path": weather_csv_path,
    "regex_patterns": regex_patterns,
}

"""
Centralized dictionary containing all configuration settings. Enables 
convenient access to all config parameters through a single import.

Usage
-----
>>> from src.config import config_params
>>> db_connection = config_params["db_path"]
>>> rainfall_pattern = config_params["regex_patterns"]["Rainfall"]
"""
