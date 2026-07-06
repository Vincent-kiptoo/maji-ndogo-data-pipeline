import pandas as pd
import logging
from src.data_ingestion import create_db_engine, query_data, read_from_web_CSV
from src.logging_config import get_logger

class FieldDataProcessor:

    def __init__(self, config_params) -> None:
        self.db_path = config_params["db_path"]
        self.sql_query = config_params["sql_query"]
        self.columns_to_rename = config_params["columns_to_rename"]
        self.values_to_rename = config_params["values_to_rename"]
        self.weather_map_data = config_params["weather_mapping_csv"]
        self.df = None
        self.engine = None
        self.logger = get_logger(__name__)

    def ingest_sql_data(self) -> pd.DataFrame:
        self.engine = create_db_engine(self.db_path)
        self.df = query_data(self.engine, self.sql_query)
        self.logger.info("SQL data is sucessfully loaded into DataFrame.")
        return self.df 

    def rename_columns(self) -> None:
        column1, column2 = list(self.columns_to_rename.keys())[0], list(self.columns_to_rename.keys())[1]
        temp_name = "__temp_name_for_swap__"
        self.df = self.df.rename(columns={column1: temp_name, column2: column1})
        self.df = self.df.rename(columns={temp_name: column2})
        self.logger.info(f"Swapped columns: {column1} with {column2}")

    def apply_corrections(self, column_name='Crop_type', abs_column='Elevation') -> None:
        self.df[abs_column] = self.df[abs_column].abs()
        self.logger.info("Converted negative elevation values to absolute as per project specification")
        self.df[column_name] = self.df[column_name].apply(lambda crop: self.values_to_rename.get(crop, crop))
        self.df[column_name] = self.df[column_name].str.strip()
        self.logger.info("Mispelled names and extra whitespaces were found and got fixed")

    def weather_station_mapping(self) -> pd.DataFrame:
        return read_from_web_CSV(self.weather_map_data)

    def process(self) -> pd.DataFrame:
        self.ingest_sql_data()
        self.rename_columns()
        self.apply_corrections()
        weather_map_df = self.weather_station_mapping()
        self.df = self.df.merge(weather_map_df, on='Field_ID', how='left')
        self.df = self.df.drop(columns="Unnamed: 0")
        return self.df
