import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from font import set_korean_font
from population_data import load_gender_population_summary  # ✅ 성별 인구수 로딩

# ✅ 한글 폰트 설정
set_korean_font()

st.title("👥 성별 인구 분포 시각화")

# ✅ 데이터 로드
gender_df = load_gender_population_summary()
st.success("✅ 성별 인구수 데이터 로드 성공")

# ✅ 데이터 표
st.subheader("📋 성별 인구 테이블")
st.dataframe(gender_df)

# ✅ 그래프
st.subheader("📊 성별 인구수 비교 그래프")
fig, ax = plt.subplots(figsize=(8, 5))
x = gender_df["SGG"]
male = gender_df["MALE_POP"]
female = gender_df["FEMALE_POP"]

bar_width = 0.35
x_index = range(len(x))

ax.bar(x_index, male, width=bar_width, label="남성", color="skyblue")
ax.bar([i + bar_width for i in x_index], female, width=bar_width, label="여성", color="lightpink")

ax.set_xticks([i + bar_width / 2 for i in x_index])
ax.set_xticklabels(x)
ax.set_ylabel("인구 수")
ax.set_title("서울 주요 구 성별 인구 수")
ax.legend()

st.pyplot(fig)
