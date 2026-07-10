import pytest
import pandas as pd

from sqlalchemy import text

from src.data_ingestion import create_db_engine, query_data, read_from_web_CSV

def test_create_db_engine_success(tmp_path):

    db_path = tmp_path / "test_database.db"

    engine = create_db_engine(
        f"sqlite:///{db_path}"
    )
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    assert result.scalar() == 1


def create_test_database(tmp_path):

    db_path = tmp_path / "test_database.db"

    engine = create_db_engine(
        f"sqlite:///{db_path}"
    )

    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE students (
                id INTEGER,
                name TEXT
            )
        """))

        connection.execute(text("""
            INSERT INTO students VALUES
            (1, 'Alice'),
            (2, 'Bob')
        """))

    return engine


def test_query_data_returns_dataframe(tmp_path):

    engine = create_test_database(tmp_path)

    df = query_data(
        engine,
        "SELECT * FROM students"
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert set(df.columns) == {"id", "name"}


def test_query_data_empty_result_raises_error(tmp_path):

    engine = create_test_database(tmp_path)

    with pytest.raises(ValueError):
        query_data(
            engine,
            "SELECT * FROM students WHERE id=99"
        )


def test_query_data_allow_empty(tmp_path):

    engine = create_test_database(tmp_path)

    df = query_data(
        engine,
        "SELECT * FROM students WHERE id=99",
        allow_empty=True
    )

    assert isinstance(df, pd.DataFrame)
    assert df.empty


def test_query_data_invalid_sql(tmp_path):

    engine = create_test_database(tmp_path)

    with pytest.raises(Exception):
        query_data(
            engine,
            "SELECT * FROM wrong_table"
        )
