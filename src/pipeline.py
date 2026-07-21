import pandas as pd
from src.field_data_processor import FieldDataProcessor
from src.weather_data_processor import WeatherDataProcessor
from src.config import config_params


def create_final_dataset():
    """
    This method merges both field and wether data into a single unified dataframe and
    rename the columns to ensure consistency
    """

    field_df = FieldDataProcessor(config_params).process()

    weather_df = WeatherDataProcessor(config_params).process()
    if field_df is None:
        raise ValueError("Field_df is an empty DataFrame")
    if weather_df is None:
        raise ValueError("weather_df is an empty DataFrame")
    final_df = field_df.merge(
        weather_df,
        on="Weather_station_ID",
        how="left"
    )

    final_df = final_df.rename(
        columns={
            "Rainfall_x": "Field_Rainfall",
            "Rainfall_y": "Station_Rainfall",
            "Pollution_level_x": "Field_Pollution_Level",
            "Pollution_level_y": "Station_Pollution_Level"
        }
    )

    return final_df
