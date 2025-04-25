# 파일: card_sales_data.py

from snowpark_util import create_session
import pandas as pd

def load_gender_population_summary() -> pd.DataFrame:
    session = create_session(database="SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS", schema="GRANDATA")

    query = """
    SELECT 
    """
    return session.sql(query).to_pandas()
