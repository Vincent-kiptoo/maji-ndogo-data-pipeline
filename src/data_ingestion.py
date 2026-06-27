from sqlalchemy import create_engine, text
import logging
import pandas as pd 

logger = logging.getLogger("data_ingestion")
logging.basicConfig(level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def create_db_engine(db_path, echo=False):
    """
    Create a SQLAlchemy database engine.

    Parameters
    ----------
    db_path : str
        Database connection string
    echo : bool, default=False
        If True, SQLAlchemy will log all SQL statements
    
    Returns
    -------
    sqlalchemy.engine.Engine
        SQLAlchemy engine object
    """
    try:
        # Create engine with optional echo for debugging
        engine = create_engine(db_path, echo=echo)
        
        # Test connection
        with engine.connect() as connection:
            # Execute a simple query to verify connection
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            
        logger.info(f"Successfully connected to: {db_path}")
        return engine
        
    except ImportError:
        logger.error("SQLAlchemy is not installed")
        raise
        
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise ConnectionError(f"Failed to connect to database: {e}") from e
    
def query_data(engine, sql_query, allow_empty=False):
    """
    Execute SQL query and return results as DataFrame.
    
    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        Database engine
    sql_query : str
        SQL query string
    allow_empty : bool, default=False
        If True, return empty DataFrame instead of raising error
    
    Returns
    -------
    pandas.DataFrame
        Query results
    
    Raises
    ------
    ValueError
        If query returns empty results and allow_empty is False
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise

    if df.empty and not allow_empty:
        msg = f"Query returned no results: {sql_query[:100]}..."
        logger.error(msg)
        raise ValueError(msg)

    logger.info(f"Query executed. Rows: {len(df)}")
    return df


def read_from_web_CSV(URL):
    """
    Read CSV file from a web URL into a DataFrame.
    
    Parameters
    ----------
    URL : str
        Full web URL pointing to a CSV file
    
    Returns
    -------
    pandas.DataFrame
        DataFrame containing CSV data
    
    Raises
    ------
    ValueError
        If URL is empty or invalid format
    pd.errors.EmptyDataError
        If CSV file is empty
    pd.errors.ParserError
        If URL doesn't point to valid CSV
    Exception
        If network or other errors occur
    """
    # Validate URL is not empty
    if not URL or not isinstance(URL, str):
        error_msg = f"Invalid URL provided: {URL}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    try:
        # Attempt to read CSV from URL
        logger.info(f"Attempting to read CSV from: {URL}")
        df = pd.read_csv(URL)
        
        # Check if data was loaded
        if df.empty:
            error_msg = f"CSV file is empty: {URL}"
            logger.warning(error_msg)
            raise pd.errors.EmptyDataError(error_msg)
        
        logger.info(f"Successfully read CSV: {len(df)} rows, {len(df.columns)} columns")
        return df
        
    except pd.errors.EmptyDataError as e:
        # Empty file
        logger.error(f"CSV file is empty: {URL}")
        raise
        
    except pd.errors.ParserError as e:
        # Malformed CSV
        logger.error(f"Failed to parse CSV from {URL}. Error: {e}")
        raise
        
    except Exception as e:
        # Network errors, invalid URLs, etc.
        logger.error(f"Failed to read CSV from {URL}. Error: {e}")
        raise Exception(f"Could not read CSV from {URL}. Error: {e}") from e

