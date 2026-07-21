# Maji Ndogo Data Pipeline

This project implements a modular ETL (Extract, Transform, Load) pipeline for processing agricultural and weather datasets from the Maji Ndogo Farm Survey. The fictional nation of Maji Ndogo serves as a realistic representation of agricultural systems across Africa, highlighting the transformative role of data in improving productivity and sustainability. The pipeline incorporates automated data cleaning, statistical validation, and quality assurance mechanisms, with a strong focus on modular architecture, reproducibility, testing, and configuration-driven development practices.

## What it does

1. **Ingests** farm survey data from a SQLite database and weather data
   from CSV files hosted on the web.
2. **Cleans** the data — fixing mislabeled columns, correcting misspelled
   categorical values, and mapping fields to their nearest weather station.
3. **Validates** the cleaned data with automated tests (`pytest`) and a
   statistical hypothesis test comparing field-reported weather to
   independent weather station readings.
   **Merges** both field data and wether data into a single unified DataFrame
5. **Exposes** the result as ready-to-analyse pandas DataFrames for
   exploratory data analysis (EDA).

## Project structure

```
maji-ndogo-data-pipeline/
├── src/
│   ├── __init__.py
|   ├── logging_config.py              # Central logging configuration
│   ├── config.py                      # Central configuration (paths, queries, mappings)
│   ├── data_ingestion.py              # Low-level SQL + CSV ingestion functions
|   ├── exploratory_data_analysis.py   # performs exploratory data analysis 
│   ├── field_data_processor.py        # FieldDataProcessor class — cleans field survey data
│   ├── weather_data_processor.py      # WeatherDataProcessor class — cleans weather station data
|   └──  pipepline.py                  # Merges field and weather datasets into a single DataFrame  
├── notebooks/
│   ├──  01_data_overview.ipynb            # Exploratory analysis — imports the modules above
|   └── 02_statistical_analysis.ipynb      # Perform statistical analysis including hypothesis test etc
├── tests/
|   └── __init__.py
    |
│   └── test_field_data_quality      # pytest checks on the cleaned field  data
|   └──  test_data_ingestion.py
|   └──  test_intergration.py
├── data/                             # Local only — gitignored, holds the .db file
├── requirements.txt
└── README.md
```

## Getting started

```bash
git clone https://github.com/Vincent-kiptoo/maji-ndogo-data-pipeline.git
cd maji-ndogo-data-pipeline

python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# venv\Scripts\Activate.ps1   # Windows PowerShell

pip install -r requirements.txt
```

You'll also need `Maji_Ndogo_farm_survey_small.db` in the `data/` folder
(not included in this repo — see `.gitignore`).

## Usage

```python
from src.config import config_params
from src.data_ingestion import create_db_engine, query_data, read_from_web_CSV
from src.field_data_processor import FieldDataProcessor
from src.weather_data_processor import WeatherDataProcessor
from src.logging_config.py import get_logger

field_processor = FieldDataProcessor(config_params)
field_processor.process()
field_df = field_processor.df

weather_processor = WeatherDataProcessor(config_params)
weather_processor.process()
weather_df = weather_processor.weather_df
```

## Running tests

```bash
pytest tests/test_field_data_quality.py -v
```

## Tech stack

- **pandas** / **SQLAlchemy** — data ingestion and manipulation
- **scipy** — statistical hypothesis testing
- **pytest** — automated data validation
- **logging** — pipeline observability

## Status

Work in progress. Built as a portfolio project demonstrating data
pipeline design, OOP in Python, testing, eploratory data analysis, statistical analysis and Git/GitHub workflows
