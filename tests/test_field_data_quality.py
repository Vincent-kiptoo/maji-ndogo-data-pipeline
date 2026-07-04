import pytest
import pandas as pd
from src.field_data_processor import FieldDataProcessor
from src.config import config_params

@pytest.fixture(scope="module")
def processed_field_data():
    processor = FieldDataProcessor(config_params)
    processor.process()
    return processor.df

class TestFieldDataQuality:
    """Tests to verify that FieldDataProcessor produces clean, valid data."""
    
    def test_no_missing_values(self, processed_field_data):
        assert processed_field_data.isnull().sum().sum() == 0

    def test_unique_field_id(self, processed_field_data): 
        assert processed_field_data['Field_ID'].is_unique


    @pytest.mark.parametrize("column, min_val, max_val", [
        ("Latitude", -15.5, 1),
        ("Longitude", -11, 2),
        ("Elevation", 0, 1200),
        ("Rainfall", 102, 2500),
        ("pH", 3.5, 8),
        ("Soil_fertility", 0.5, 0.85),
        ("Plot_size", 0.5, 15),
    ])

    def test_geographic_bounds(self, processed_field_data, column, min_val, max_val):
        assert processed_field_data[column].between(min_val, max_val).all()

    def test_temperature_logic(self, processed_field_data):
        min_temp = processed_field_data["Min_temperature_C"]
        max_temp = processed_field_data["Max_temperature_C"]

        # rule 1: logical consistency
        assert (min_temp < max_temp).all()

        # rule 2: realistic spread (soft constraint)
        temp_diff = max_temp - min_temp
        assert temp_diff.between(0, 50).mean() > 0.98

    def test_crop_types(self, processed_field_data):
        expected = {
            "wheat", "maize", "rice", "cassava",
            "banana", "coffee", "tea", "potato"
        }

        actual = set(processed_field_data["Crop_type"].str.lower().unique())

        assert actual == expected


    @pytest.mark.parametrize("column, expected", [
        ("Soil_type",{"sandy", "volcanic", "loamy", "silt", "peaty", "rocky"} ),
        ("Location", {"rural_akatsi", "rural_sokoto", "rural_kilimani", "rural_hawassa", "rural_amanzi"}),])

    def test_categorical_values(self, processed_field_data, column, expected):
        actual = set(
            processed_field_data[column]
            .str.strip()
            .str.lower()
            .unique()
        )

        assert actual == expected

    def test_data_health_score(self, processed_field_data):
        null_ratio = processed_field_data.isnull().mean().mean()

        assert null_ratio == 0