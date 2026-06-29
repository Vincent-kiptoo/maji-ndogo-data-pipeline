import re
import pandas as pd
import logging
from src.data_ingestion import read_from_web_CSV

class WeatherDataProcessor:

    def __init__(self, config_params, logging_level = "INFO"):
        """
        Initialize the WeatherDataProcessor with configuration parameters.

        Parameters
        ----------
        config_params : dict
            Dictionary containing 'weather_csv_path' (URL to the raw weather
            station CSV) and 'regex_patterns' (dict mapping measurement names
            to regex patterns used to extract values from messages).
        logging_level : str, default "INFO"
            Logging verbosity for this instance: "DEBUG", "INFO", or "NONE".
        """
        self.weather_csv_data = config_params["weather_csv_path"]
        self.patterns = config_params["regex_patterns"]
        self.weather_df = None
        self.mean_df = None

        self.initialize_logging(logging_level)

    def initialize_logging(self, logging_level):
        logger_name = __name__ + ".WeatherDataProcessor"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        if logging_level.upper() == "DEBUG":
            log_level = logging.DEBUG
        elif logging_level.upper() == "INFO":
            log_level = logging.INFO
        elif logging_level.upper() == "NONE":
            self.logger.disabled = True
            return
        else:
            log_level = logging.INFO
        self.logger.setLevel(log_level)
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)


    def weather_station_mapping(self):
        """
        Fetch the raw weather station data from the configured web CSV.

        Loads the CSV from self.weather_csv_data using read_from_web_CSV,
        storing the result in self.weather_df as the working DataFrame for
        all subsequent processing steps.
        """
        
        self.weather_df = read_from_web_CSV(self.weather_csv_data)
        self.logger.info("Successfully loaded the data from the weather csv data url")

    def extract_measurement(self, message):
        """
        Extract a measurement type and numeric value from a single message.

        Tries each regex pattern in self.patterns in turn; the first pattern
        that matches determines the measurement type and value returned.

        Parameters
        ----------
        message : str
            A single raw weather station message.

        Returns
        -------
        tuple of (str or None, float or None)
            The matched measurement type and its value, or (None, None)
            if no pattern matched.
        """
        for key, pattern in self.patterns.items():
            match = re.search(pattern, message)
            if match:
                self.logger.debug(f"Measurement extracted: {key}")
                return key, float(next((x for x in match.groups() if x is not None)))
        self.logger.debug("No measurement match found.")
        return None, None
    
    def process_messages(self):
        """
        Extract measurements from every message in self.weather_df.

        Adds 'Measurement' and 'Value' columns to self.weather_df by applying
        extract_measurement across the 'Message' column. If self.weather_df
        is None, logs a warning and does nothing.
        """

        if self.weather_df is not None:
            result = self.weather_df['Message'].apply(self.extract_measurement)
            self.weather_df['Measurement'], self.weather_df['Value'] = zip(*result)
            self.logger.info("Messages processed and measurements extracted.")
        else:
            self.logger.warning("weather_df is not initialized, skipping message processing.")
        return self.weather_df

    def calculate_means(self):
        """
        Reshape long-format measurements into wide-format station means.

        Groups self.weather_df by Weather_station_ID and Measurement, takes
        the mean of Value, then unstacks so each measurement type becomes
        its own column. If self.weather_df is None, logs a warning and
        returns None.
        """
        if self.weather_df is not None:
            means = self.weather_df.groupby(by=['Weather_station_ID', 'Measurement'])['Value'].mean()
            self.logger.info("Mean values calculated.")
            return means.unstack()
        else:
            self.logger.warning("weather_df is not initialized, cannot calculate means.")
            return None
        
    def process(self):
        """
        Run the full weather data pipeline: fetch, extract, and aggregate.

        Calls weather_station_mapping, process_messages, and calculate_means
        in order, storing the final wide-format result in self.mean_df.

        Returns
        -------
        pandas.DataFrame or None
            The wide-format station means table.
        """

        self.weather_station_mapping()
        self.process_messages()
        self.mean_df = self.calculate_means()
        self.logger.info("Data processing completed.")
        return self.mean_df