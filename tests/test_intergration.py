import pandas as pd

from src.field_data_processor import FieldDataProcessor
from src.weather_data_processor import WeatherDataProcessor
from src.config import config_params

def test_field_weather_pipeline():

    field_processor = FieldDataProcessor(config_params)
    field_df = field_processor.process()

    weather_processor = WeatherDataProcessor(config_params)
    weather_df = weather_processor.process()
    assert weather_df is not None
    assert field_df is not None

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
            "Pollution_level_y": "Station_Pollution_Level"})


    assert isinstance(final_df, pd.DataFrame)
    assert len(final_df) == len(field_df)
    assert "Field_Rainfall" in final_df.columns
    assert "Station_Rainfall" in final_df.columns
    assert "Temperature" in final_df.columns
    assert final_df["Station_Rainfall"].isna().sum() == 0