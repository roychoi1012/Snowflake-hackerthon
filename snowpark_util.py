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

'''
demo_session = create_session()
print("✅ 연결 성공")

query = """
SELECT DEP_NAME, SUM(COUNT) AS TOTAL_VISITORS
FROM SNOWFLAKE_STREAMLIT_HACKATHON_LOPLAT_DEPARTMENT_STORE_DATA
WHERE DEP_NAME IN ('더현대서울', '롯데백화점_본점', '신세계_강남')
AND DATE_KST BETWEEN '2021-04-01' AND '2022-04-30'
GROUP BY DEP_NAME
ORDER BY TOTAL_VISITORS DESC
"""

query2 = """
SELECT DISTINCT DEP_NAME
FROM SNOWFLAKE_STREAMLIT_HACKATHON_LOPLAT_DEPARTMENT_STORE_DATA
"""


df = demo_session.sql(query)
print("✅ 데이터 로드 성공")

df.show()


print("✅ 데이터 출력 성공")
'''
