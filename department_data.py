# data.py
import pandas as pd
from snowpark_util import create_session

def load_department_store_data(start_date, end_date, dep_names):
    session = create_session("DEPARTMENT_STORE_FOOT_TRAFFIC_FOR_SNOWFLAKE_STREAMLIT_HACKATHON")

    query = f"""
    SELECT DEP_NAME, SUM(COUNT) AS TOTAL_VISITORS
    FROM SNOWFLAKE_STREAMLIT_HACKATHON_LOPLAT_DEPARTMENT_STORE_DATA
    WHERE DEP_NAME IN ({','.join(f"'{name}'" for name in dep_names)})
    AND DATE_KST BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY DEP_NAME
    ORDER BY TOTAL_VISITORS DESC
    """

    return session.sql(query).to_pandas()
