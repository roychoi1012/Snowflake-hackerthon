import streamlit as st
import geopandas as gpd
import pandas as pd
import json
import os
from shapely.geometry import shape
from snowflake.snowpark import Session
import folium
from streamlit_folium import st_folium

# 1️⃣ Snowflake 세션 생성 - 보안 강화
def create_session() -> Session:
    # 환경 변수 또는 Streamlit secrets를 사용
    connection_parameters = {
        "account": st.secrets["snowflake"]["account"],
        "user": st.secrets["snowflake"]["user"],
        "password": st.secrets["snowflake"]["password"],
        "role": st.secrets["snowflake"]["role"],
        "warehouse": st.secrets["snowflake"]["warehouse"],
        "database": st.secrets["snowflake"]["database"],
        "schema": st.secrets["snowflake"]["schema"]
    }
    return Session.builder.configs(connection_parameters).create()

# Streamlit 앱 제목
st.title("서울시 대출 위험도 지도")
st.write("서울시 행정동별 대출 위험도를 시각화한 지도입니다.")

# 데이터 로드 및 처리
@st.cache_data
def load_data():
    try:
        session = create_session()
        
        # 2️⃣ 두 테이블 조인 - 필요한 필드만 선택
        a = session.table("ASSET_INCOME_INFO").alias("A")
        m = session.table("M_SCCO_MST").alias("M")

        joined_df = (
            a.join(m, a["DISTRICT_CODE"] == m["DISTRICT_CODE"])
            .select(
                a["DISTRICT_CODE"].alias("ADM_CD"),
                m["DISTRICT_KOR_NAME"],
                m["DISTRICT_GEOM"],
                a["TOTAL_BALANCE_AMOUNT"],
                a["TOTAL_NON_BANK_BALANCE_AMOUNT"],
                a["TOTAL_CASH_ADVANCE_USAGE_AMOUNT"]
            )
        )

        # 3️⃣ Pandas로 변환
        pdf = joined_df.to_pandas()
        
        # 세션 종료
        session.close()
        
        # 4️⃣ 위험도 계산
        # 0으로 나누는 오류 방지
        pdf["TOTAL_BALANCE_AMOUNT"] = pdf["TOTAL_BALANCE_AMOUNT"].replace(0, 1)
        
        pdf["Loan_Risk_Score"] = (
            pdf["TOTAL_NON_BANK_BALANCE_AMOUNT"] + pdf["TOTAL_CASH_ADVANCE_USAGE_AMOUNT"]
        ) / pdf["TOTAL_BALANCE_AMOUNT"]

        # 5️⃣ GeoDataFrame 변환 - 지오메트리 단순화 추가
        pdf["geometry"] = pdf["DISTRICT_GEOM"].apply(
            lambda x: shape(json.loads(x)).simplify(tolerance=0.0001)
        )
        
        gdf = gpd.GeoDataFrame(
            pdf[['ADM_CD', 'DISTRICT_KOR_NAME', 'Loan_Risk_Score', 'geometry']], 
            geometry="geometry", 
            crs="EPSG:4326"
        )
        
        return gdf
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {str(e)}")
        return None

# 프로그레스 바 표시
with st.spinner("데이터를 불러오는 중입니다..."):
    gdf = load_data()

if gdf is not None:
    # 자치구 선택 옵션 추가
    district_names = sorted(gdf['DISTRICT_KOR_NAME'].str.split().str[0].unique())
    selected_district = st.selectbox(
        "자치구 선택 (전체 데이터를 보려면 '전체'를 선택하세요)",
        ['전체'] + district_names
    )
    
    # 필터링된 데이터
    if selected_district != '전체':
        filtered_gdf = gdf[gdf['DISTRICT_KOR_NAME'].str.startswith(selected_district)]
    else:
        filtered_gdf = gdf
    
    # 데이터 요약 통계
    st.subheader("데이터 요약")
    st.write(f"선택된 행정동 수: {len(filtered_gdf)}")
    st.write(f"평균 대출 위험도: {filtered_gdf['Loan_Risk_Score'].mean():.4f}")
    st.write(f"최대 대출 위험도: {filtered_gdf['Loan_Risk_Score'].max():.4f}")
    
    # 6️⃣ Folium 지도 생성
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11 if selected_district == '전체' else 12)

    # 7️⃣ Choropleth 추가 - 단순화된 방식으로
    # GeoJSON 직접 생성 대신 simplified_json 사용
    simplified_json = json.loads(filtered_gdf.to_json())
    
    choropleth = folium.Choropleth(
        geo_data=simplified_json,
        name="Loan Risk Score",
        data=filtered_gdf,
        columns=["ADM_CD", "Loan_Risk_Score"],
        key_on="feature.properties.ADM_CD",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="대출 위험도 지수",
        highlight=True
    ).add_to(m)
    
    # 각 지역에 팝업 추가 - 간소화된 방식으로
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color': '#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.5}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color': '#000000', 
                                    'fillOpacity': 0.25, 
                                    'weight': 0.5}
    
    # 상위 10개 위험 지역 마커 표시
    if st.checkbox("상위 10개 위험 지역 마커 표시", value=True):
        top_risk = filtered_gdf.nlargest(10, 'Loan_Risk_Score')
        for _, row in top_risk.iterrows():
            centroid = row.geometry.centroid
            folium.Marker(
                location=[centroid.y, centroid.x],
                popup=f"{row['DISTRICT_KOR_NAME']} - 위험도: {row['Loan_Risk_Score']:.2f}",
                tooltip=row['DISTRICT_KOR_NAME'],
                icon=folium.Icon(color='red', icon='warning-sign')
            ).add_to(m)

    # Streamlit에 지도 표시 - st_folium 사용
    st.subheader(f"{'서울시' if selected_district == '전체' else selected_district} 대출 위험도 지도")
    st_folium(m, width=700, height=500)
    
    # 데이터 테이블 표시
    if st.checkbox("데이터 테이블 보기", value=False):
        st.dataframe(
            filtered_gdf[['DISTRICT_KOR_NAME', 'Loan_Risk_Score']]
            .sort_values('Loan_Risk_Score', ascending=False)
            .reset_index(drop=True)
        )
        
    # 위험도 상위 5개 / 하위 5개 지역 막대 차트
    if st.checkbox("위험도 상위/하위 지역 차트", value=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("위험도 상위 5개 지역")
            top5 = filtered_gdf.nlargest(5, 'Loan_Risk_Score')
            st.bar_chart(top5.set_index('DISTRICT_KOR_NAME')['Loan_Risk_Score'])
            
        with col2:
            st.subheader("위험도 하위 5개 지역")
            bottom5 = filtered_gdf.nsmallest(5, 'Loan_Risk_Score')
            st.bar_chart(bottom5.set_index('DISTRICT_KOR_NAME')['Loan_Risk_Score'])
else:
    st.error("데이터를 불러올 수 없습니다. Snowflake 연결 설정을 확인하세요.")