# 파일: population_data.py

from snowpark_util import create_session
import pandas as pd

def load_gender_population_summary() -> pd.DataFrame:
    session = create_session(database="KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA", schema="HACKATHON_2025Q2")

    query = """
    SELECT SGG, SUM(MALE) AS MALE_POP, SUM(FEMALE) AS FEMALE_POP
    FROM REGION_MOIS_POPULATION_GENDER_AGE_M_H
    WHERE SGG IN ('중구', '영등포구', '서초구')
    GROUP BY SGG
    ORDER BY SGG
    """
    return session.sql(query).to_pandas()
