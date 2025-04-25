import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from font import set_korean_font
from department_data import load_department_store_data

# ✅ 한글 폰트 적용
set_korean_font()

# ✅ 제목
st.title("🛍️ 백화점별 방문자 수 분석 (기간 선택 가능)")

# ✅ 날짜 범위 선택
st.subheader("📅 분석 기간 설정")
start_date, end_date = st.date_input(
    "기간 선택",
    value=(pd.to_datetime("2021-01-01"), pd.to_datetime("2024-12-31")),
    min_value=pd.to_datetime("2021-01-01"),
    max_value=pd.to_datetime("2024-12-31")
)

# ✅ 분석 대상 백화점 고정
dep_names = ['더현대서울', '롯데백화점_본점', '신세계_강남']

# ✅ 데이터 로딩
df = load_department_store_data(str(start_date), str(end_date), dep_names)
st.success("✅ 데이터 로드 성공")

# ✅ 데이터 표 출력
st.subheader("📋 방문자 수 테이블")
st.dataframe(df)

# ✅ 그래프 시각화
st.subheader("📊 방문자 수 막대 그래프")
fig, ax = plt.subplots(figsize=(8, 5))

x = df["DEP_NAME"]
y = df["TOTAL_VISITORS"]

ax.bar(x, y, color="#4c72b0")
ax.set_title(f"{start_date} ~ {end_date} 방문자 수")
ax.set_ylabel("방문자 수")
ax.set_xlabel("백화점명")
ax.tick_params(axis='x', labelrotation=0)

st.pyplot(fig)
