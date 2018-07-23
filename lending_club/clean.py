"""
Methods to clean and transform data set.
"""
from dateutil.relativedelta import relativedelta
import pandas as pd

from lending_club import db


def columns_by_type(df, typ):
    """
    Helper function to subset a data frame by the types in the data dictionary

    Args:
        df (dataframe): data dictionary
        typ (str): demographics, loan, credit, LC_calcs, outcomes

    Returns:
        list of column names in the data set

    """
    return list(df.loc[df[typ] == 1, 'name'])


def get_distinct_vals(column):
    """
    Returns the distinct values from a column from the loans sqlite file. Used to make maps for categorical values.

    Args:
        column (str): column name from loan sqlite file

    Returns:
        List of distinct values

    """
    query = """
    SELECT DISTINCT {column} FROM loan;
    """.format(column=column)
    df = db.sql_to_df(query)
    return list(df[df.columns[0]])


def difference_in_months(datetime1, datetime2):
    """
    Return the difference between two datetime objects in months.

    Args:
        datetime1: datetime object
        datetime2: datetime object

    Returns:
        Difference between the two datetime objects in months

    """
    if pd.isnull(datetime1) | pd.isnull(datetime2):
        return None
    else:
        try:
            delta = relativedelta(datetime1, datetime2)
            return abs(delta.years * 12 + delta.months)
        except AssertionError as e:
            print(str(datetime1), str(datetime2))


def roi(row):
    """
    Helper function to calculate an ROI given a particular row of loan data.
    Args:
        row(Series): a row of the loan data frame

    Returns:
        calculated ROI

    """
    cost = row['funded_amnt'] + row['collection_recovery_fee']
    return (row['total_pymnt'] - cost) / cost


def percent_to_float(ser):
    """
    Helper function to take a Pandas Series of percentages, labeled with a percent sign and convert to a float.

    Args:
        ser: Pandas series

    Returns:
        Numeric series

    """
    return pd.to_numeric(ser.str.replace('%', '').str.strip())
