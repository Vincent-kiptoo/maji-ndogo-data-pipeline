"""
Configuration module for the Maji Ndogo data pipeline.

This module centralizes all configuration parameters used throughout the pipeline,
including database connection strings, SQL queries, data transformation rules, 
CSV sources, and regex patterns for data extraction and validation.

The configuration follows a single-source-of-truth approach, allowing easy updates
to pipeline behavior without modifying core pipeline logic.

Attributes
----------
db_path : str
    Database connection string for SQLite database containing Maji Ndogo farm survey data
sql_query : str
    SQL query that joins geographic, weather, soil/crop, and farm management features
    on Field_ID as the common key
columns_to_rename : dict
    Mapping of column names to be swapped during data transformation
values_to_rename : dict
    Mapping of standardized crop type names (corrects typos and inconsistencies)
weather_mapping_csv : str
    URL to CSV file containing weather data field mapping for external weather stations
weather_csv_path : str
    URL to CSV file containing weather station data
regex_patterns : dict
    Compiled regex patterns for extracting numerical values from text fields
config_params : dict
    Dictionary aggregating all configuration parameters for convenient access

Examples
--------
Access configuration parameters in pipeline modules:

>>> from src.config import config_params
>>> db_path = config_params["db_path"]
>>> sql_query = config_params["sql_query"]
>>> weather_csv_path = config_params["weather_csv_path"]

Update configuration centrally without modifying pipeline code:

>>> from src.config import columns_to_rename
>>> # All modules using columns_to_rename will reflect updates automatically
"""

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

db_path = "sqlite:///data/Maji_Ndogo_farm_survey_small.db"
"""str: SQLite database connection string pointing to Maji Ndogo farm survey data."""

# ============================================================================
# SQL QUERY CONFIGURATION
# ============================================================================

sql_query = """
SELECT *
FROM geographic_features
LEFT JOIN weather_features USING (Field_ID)
LEFT JOIN soil_and_crop_features USING (Field_ID)
LEFT JOIN farm_management_features USING (Field_ID)
"""
"""
str: SQL query joining all feature tables.

Performs LEFT JOINs to preserve all records from geographic_features while 
including available data from related feature tables (weather, soil/crop, farm management).
Joins are performed on Field_ID as the primary key.
"""

# ============================================================================
# DATA TRANSFORMATION CONFIGURATION
# ============================================================================

columns_to_rename = {"Annual_yield": "Crop_type", 
                     "Crop_type": "Annual_yield"}
"""
dict: Column name mappings for data transformation.

Swaps the names of Annual_yield and Crop_type columns. This appears to correct
a labeling inconsistency in the source data where these columns were mislabeled.

Example
-------
Before transformation: {'Annual_yield': [...], 'Crop_type': [...]}
After transformation:  {'Crop_type': [...], 'Annual_yield': [...]}
"""

values_to_rename = {
        'cassaval': 'cassava',
        'wheatn': 'wheat',
        'teaa': 'tea'
    }
"""
dict: Standardized crop type name mappings.

Corrects common typos and inconsistencies in crop type values found in the 
Crop_type column. This standardization ensures data consistency and accurate 
aggregation during analysis.

Corrections
-----------
cassaval -> cassava : Common misspelling of cassava crop
wheatn -> wheat : Incomplete spelling of wheat crop
teaa -> tea : Misspelled variant of tea crop
"""

# ============================================================================
# EXTERNAL DATA SOURCES (CSV URLs)
# ============================================================================

weather_mapping_csv = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv"
"""
str: URL to weather data field mapping CSV.

Contains the mapping between weather stations and farm fields, allowing 
linkage of weather station observations to individual farm records.
Source: Explore-AI Public Data Repository
"""

weather_csv_path = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv"
"""
str: URL to weather station observations CSV.

Contains historical weather data (temperature, rainfall, pollution levels) 
from monitoring stations. Data is mapped to farm fields via weather_mapping_csv.
Source: Explore-AI Public Data Repository
"""

# ============================================================================
# REGEX PATTERNS FOR DATA EXTRACTION
# ============================================================================

regex_patterns = {
    'Rainfall': r'(\d+(\.\d+)?)\s?mm',
     'Temperature': r'(\d+(\.\d+)?)\s?C',
    'Pollution_level': r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
    }
"""
dict: Regular expressions for extracting numerical data from text fields.

Used to parse and standardize numerical values embedded in text data.

Patterns
--------
Rainfall : Extracts decimal numbers followed by optional whitespace and 'mm'
    Examples: '150mm', '25.5 mm', '10mm'
    Captures: 150, 25.5, 10

Temperature : Extracts decimal numbers followed by optional whitespace and 'C'
    Examples: '25C', '18.5 C', '32.0C'
    Captures: 25, 18.5, 32.0

Pollution_level : Extracts signed decimal numbers with two format variations
    Format 1: '= -45.2' or '= 50'
    Format 2: 'Pollution at -45.2' or 'Pollution at 50'
    Captures: -45.2, 50, etc. (supports negative values)
"""

# ============================================================================
# CENTRALIZED CONFIGURATION DICTIONARY
# ============================================================================

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
dict: Aggregated configuration parameters.

Centralized dictionary containing all configuration settings. Enables 
convenient access to all config parameters through a single import.

Usage
-----
>>> from src.config import config_params
>>> db_connection = config_params["db_path"]
>>> rainfall_pattern = config_params["regex_patterns"]["Rainfall"]
"""
