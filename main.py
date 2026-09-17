import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)


# -----------------------------
# 제목
# -----------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 그래프로 살펴봅니다."
)


# -----------------------------
# 데이터 불러오기
# -----------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df


df = load_data()


# -----------------------------
# 데이터 전처리
# -----------------------------

# 장르가 여러 개 적혀 있는 경우 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 빈 값 처리
df["genre_first"] = df["genre_first"].replace("", "미상")


# -----------------------------
# 그래프 1
# -----------------------------
st.divider()

st.header("📊 그래프 1. 장르별 영화 편수")

genre_count = (
    df["genre_first"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]


fig = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="percent",
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

fig.update_layout(
    height=550,
    font=dict(size=16),
    legend_title_text="장르"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------
# 그래프로 알 수 있는 것
# -----------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "이 기간에 박스오피스 10위권에 든 영화는 어떤 장르가 많고, "
    "각 장르가 전체 영화에서 어느 정도의 비율을 차지하는지 알 수 있다."
)


# -----------------------------
# 데이터 확인
# -----------------------------
st.divider()

st.header("📋 사용한 데이터")

st.write(f"전체 영화 수: **{len(df)}편**")

st.dataframe(
    df[
        [
            "movieNm",
            "openDt",
            "genre_first",
            "nation",
            "first_scrn",
            "first_show",
            "first_week_audi",
            "total_audi",
            "days_in_top10"
        ]
    ].rename(
        columns={
            "movieNm": "영화명",
            "openDt": "개봉일",
            "genre_first": "장르",
            "nation": "제작 국가",
            "first_scrn": "개봉일 스크린수",
            "first_show": "개봉일 상영횟수",
            "first_week_audi": "개봉 첫 주 관객",
            "total_audi": "총 관객",
            "days_in_top10": "10위권 머문 날수"
        }
    ),
    use_container_width=True,
    hide_index=True
)
