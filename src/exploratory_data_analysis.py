"""
This module explores the processed Maji Ndogo agricultural dataset to understand
its structure, assess data quality, examine variable distributions, and identify
patterns that may influence crop productivity.
"""

from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.container import BarContainer

from src.logging_config import get_logger
from src.pipeline import create_final_dataset


class ExploratoryDataAnalysis:
    def __init__(self, df: pd.DataFrame | None = None) -> None:
        self.logger = get_logger(__name__)
        self.original_df = df.copy() if df is not None else None
        self.df = df.copy() if df is not None else None
        self.logger.info("EDAHelper initialized")

    def _ensure_dataframe(self) -> pd.DataFrame:
        """Return the working dataframe or raise a clear error."""
        if self.df is None:
            raise ValueError("No dataframe loaded. Call get_data() first.")
        if self.df.empty:
            raise ValueError("The dataframe is empty. Please check your data source.")
        return self.df

    def get_data(self) -> pd.DataFrame:
        """
        Load the data and create a working copy for analysis.
        The original data remains untouched.
        """
        raw_data = create_final_dataset()
        self.original_df = raw_data.copy()
        self.df = raw_data.copy()

        self.logger.info(f"Data loaded successfully with {len(self.df)} rows")
        return self.df

    def quality_assessment(self) -> pd.Series:
        """
        Print a simple quality assessment and return datatype counts.
        """
        df = self._ensure_dataframe()
        print("DATA QUALITY ASSESSMENT")

        missing_counts = df.isnull().sum()
        missing_values = missing_counts[missing_counts > 0]

        print("\nMISSING VALUES:")
        if missing_values.empty:
            print("No missing values found!")
        else:
            for col, count in missing_values.items():
                pct = count / len(df) * 100
                print(f"  {col:20} | {count:5} missing ({pct:5.1f}%)")

        duplicate_count = df.duplicated().sum()

        print("\nDUPLICATE RECORDS:")
        if duplicate_count == 0:
            print("No duplicate rows found!")
        else:
            print(f"  Found {duplicate_count} duplicate rows ({duplicate_count / len(df) * 100:.1f}%)")

        print("\nDATA TYPE COUNTS:")
        return df.dtypes.value_counts()

    def get_categorical_columns(self) -> list:
        """Return a dataframe listing categorical columns."""
        df = self._ensure_dataframe()
        columns = df.select_dtypes(include=["object", "category"]).columns.tolist()
        return columns

    def list_categorical_values(self, column: str) -> pd.DataFrame:
        """List the unique values found in a categorical column."""
        df = self._ensure_dataframe()
        if column not in df.columns:
            raise KeyError(f"Column '{column}' was not found.")

        unique_values = df[column].dropna().unique()
        return pd.DataFrame({column: unique_values})

    def get_numeric_columns(self, exclude: list[str] | None = None) -> list[str]:
        """Return numeric columns, excluding identifiers by default."""
        df = self._ensure_dataframe()
        if exclude is None:
            exclude = ["Weather_station_ID", "Field_ID"]

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        return [col for col in numeric_cols if col not in exclude]

    def summary_statistics(self, numeric_cols: list[str] | None = None) -> pd.DataFrame:
        """Return descriptive statistics for the selected numeric columns."""
        df = self._ensure_dataframe()

        if numeric_cols is None:
            numeric_cols = self.get_numeric_columns()

        missing_columns = [col for col in numeric_cols if col not in df.columns]
        if missing_columns:
            raise KeyError(f"Columns not found: {missing_columns}")

        return df[numeric_cols].describe().T

    def single_num_variable_desc_statistics(self, column: str) -> pd.Series:
        """Return descriptive statistics for one numeric variable."""
        df = self._ensure_dataframe()
        if column not in df.columns:
            raise KeyError(f"Column '{column}' was not found.")

        return df[column].describe()

    def plot_numerical_distribution(self, column, title=None) -> None:
        """
        A Plot for the distribution of a numerical variable with counts.
        """
        df = self._ensure_dataframe()

        if not isinstance(column, str):
            raise ValueError(f"Expected string column name, got {type(column)}")
        
        mean = round(float(df[column].mean()), 3)
        std = df[column].std()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(data=df, x=column, bins=30, kde=True, ax=ax) 
        
        ax.axvline(mean, color="red", linewidth=2, linestyle="dashed", label=f"Mean: {mean}")
        ax.axvline(mean + std, color="orange", linewidth=2, linestyle="-", label=f"+1 Std")
        ax.axvline(mean - std, color="black", linewidth=2, linestyle="-", label=f"-1 Std")

        plot_title = title if title else f"Distribution of {column}"
        ax.set_title(plot_title)
        ax.legend()
        plt.tight_layout()
        plt.show()

    def numerical_outlier_detection(self, column: str, title: str | None = None) -> None:
        """Visualize outliers for a single numeric column."""
        df = self._ensure_dataframe()
        if column not in df.columns:
            raise KeyError(f"Column '{column}' was not found.")

        plt.figure(figsize=(8, 6))
        sns.boxplot(x=df[column])
        plt.title(title or f"{column} outliers", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.show()

    def plot_categorical_distribution(self, column: str, title: str | None = None) -> None:
        """Plot the distribution of a categorical variable with counts and percentages."""
        df = self._ensure_dataframe()
        if column not in df.columns:
            raise KeyError(f"Column '{column}' was not found.")

        if title is None:
            title = f"{column} distribution"

        plt.figure(figsize=(8, 5))
        ax = sns.countplot(data=df, y=column, order=df[column].value_counts().index)

        counts = [patch.get_width() for patch in ax.containers[0]]
        labels = [f"{int(val)} ({val / len(df) * 100:.1f}%)" for val in counts]
        ax.bar_label(cast(BarContainer, ax.containers[0]), labels=labels, padding=5)

        plt.title(title, fontsize=14, fontweight="bold")
        plt.xlabel("Count", fontsize=12)
        plt.ylabel(column, fontsize=12)
        plt.tight_layout()
        plt.show()
