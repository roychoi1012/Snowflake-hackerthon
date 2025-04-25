import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from font import set_korean_font
from department_data import load_department_store_data  # ✅ 함수만 임포트

# ✅ 한글 폰트 설정
set_korean_font()

# UI 타이틀
st.title("🛍️ 백화점별 방문자 수 분석")

# 날짜 필터
st.subheader("📅 날짜 범위 선택")
start_date = st.date_input("시작일", pd.to_datetime("2021-04-01"))
end_date = st.date_input("종료일", pd.to_datetime("2022-04-30"))

# 백화점 고정 리스트
dep_names = ['더현대서울', '롯데백화점_본점', '신세계_강남']

# ✅ 데이터 로드
df = load_department_store_data(str(start_date), str(end_date), dep_names)
st.success("✅ 데이터 로드 성공")

# ✅ 데이터 테이블 출력
st.subheader("📋 요약 테이블")
st.dataframe(df)

# ✅ 시각화
st.subheader("📊 방문자 수 막대 그래프")
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(df["DEP_NAME"], df["TOTAL_VISITORS"], color="#4c72b0")
ax.set_title("백화점별 방문자 수")
ax.set_xlabel("백화점명")
ax.set_ylabel("방문자 수")
ax.tick_params(axis='x', labelrotation=0)
st.pyplot(fig)
