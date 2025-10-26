import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# --- 설정 (Configuration) ---

# 2024년 기준 미국 시가총액 상위 기업 티커 (상위 10개)
# 이 목록은 시간이 지남에 따라 변동될 수 있습니다.
# 티커: Apple (AAPL), Microsoft (MSFT), NVIDIA (NVDA), Alphabet (GOOGL), Amazon (AMZN), Meta Platforms (META), Berkshire Hathaway (BRK-B), Eli Lilly (LLY), Broadcom (AVGO), Tesla (TSLA)
TICKERS = [
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 
    'META', 'BRK-B', 'LLY', 'AVGO', 'TSLA'
]
# 기업 이름 매핑 (차트 범례를 더 명확하게 하기 위해)
TICKER_NAMES = {
    'AAPL': 'Apple', 
    'MSFT': 'Microsoft', 
    'NVDA': 'NVIDIA', 
    'GOOGL': 'Alphabet (Google)', 
    'AMZN': 'Amazon', 
    'META': 'Meta Platforms', 
    'BRK-B': 'Berkshire Hathaway', 
    'LLY': 'Eli Lilly', 
    'AVGO': 'Broadcom', 
    'TSLA': 'Tesla'
}

# 기간 설정 (최근 10년)
end_date = date.today()
start_date = end_date - timedelta(days=10*365) # 대략 10년 전

# --- 데이터 가져오기 (Data Fetching) ---

@st.cache_data
def load_data(tickers, start, end):
    """
    yfinance를 사용하여 지정된 티커들의 수정 종가 데이터를 가져옵니다.
    """
    data = yf.download(tickers, start=start, end=end)['Adj Close']
    return data

# --- Streamlit 앱 (Streamlit App) ---

st.set_page_config(
    page_title="미국 시가총액 상위 10개 기업 주가 변동",
    layout="wide"
)

st.title("💰 미국 주식 시가총액 상위 10개 기업 주가 변동")
st.markdown(f"**기간:** {start_date.strftime('%Y년 %m월 %d일')} ~ {end_date.strftime('%Y년 %m월 %d일')} (최근 10년)")

# 데이터 로드
stock_data = load_data(TICKERS, start_date, end_date)

# 데이터 유효성 검사
if stock_data.empty:
    st.error("지정된 기간 동안의 주가 데이터를 가져오지 못했습니다. 티커 또는 기간을 확인해주세요.")
else:
    # --- 시각화 데이터 준비: 정규화 ---
    
    # 1. 시가총액 상위 기업 주가 데이터 표시 (원화폐 가치)
    st.subheader("1. 주가 변동 (원화폐 가치)")
    st.line_chart(stock_data.rename(columns=TICKER_NAMES))
    
    # 2. 정규화된 수익률 데이터 계산 (모든 주가를 시작 시점의 100%로 설정)
    # 이는 각 기업의 '성장률'을 비교하는 데 유용합니다.
    normalized_data = (stock_data / stock_data.iloc[0]) * 100
    
    st.subheader("2. 정규화된 주가 변동 (시작 시점=100)")
    st.info("이 차트는 **10년간의 상대적인 수익률**을 비교합니다. 시작 시점의 주가를 100으로 설정했습니다.")
    st.line_chart(normalized_data.rename(columns=TICKER_NAMES))

    st.subheader("데이터 테이블 (수정 종가)")
    # 인덱스(날짜) 포맷 변경 및 티커 이름을 기업 이름으로 변경하여 표시
    display_data = stock_data.copy()
    display_data.index = display_data.index.strftime('%Y-%m-%d')
    display_data.rename(columns=TICKER_NAMES, inplace=True)
    st.dataframe(display_data.head()) # 상위 5개 행만 표시
    
    st.markdown("---")
    st.markdown("데이터 출처: **Yahoo Finance** (`yfinance` 라이브러리)")
