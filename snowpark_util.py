from snowflake.snowpark import Session

def create_session(database: str, schema: str = "PUBLIC") -> Session:
    connection_parameters = {
        "account": "STMNGJB-JGB89962",
        "user": "ROYCHOI1012",
        "password": "Chldmsfuf1012!",
        "role": "ACCOUNTADMIN",
        "warehouse": "COMPUTE_WH",
        "database": database,
        "schema": schema
    }
    return Session.builder.configs(connection_parameters).create()

# 1번 데이터베이스
session1 = create_session("DEPARTMENT_STORE_FOOT_TRAFFIC_FOR_SNOWFLAKE_STREAMLIT_HACKATHON")

# 2번 데이터베이스
session2 = create_session("KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA")

# 3번 데이터베이스
session3 = create_session("SNOWFLAKE_STREAMLIT_HACKATHON_LOPLAT_SEOUL_TEMPERATURE_RAINFALL")

