import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# --- 설정 (Configuration) ---

# 2024년 기준 미국 시가총액 상위 기업 티커 (상위 10개)
TICKERS = [
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 
    'META', 'BRK-B', 'LLY', 'AVGO', 'TSLA'
]
# 기업 이름 매핑
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
# 약 10년 전 (365일 * 10)
start_date = end_date - timedelta(days=3650) 

# --- 데이터 가져오기 (Data Fetching) ---

@st.cache_data(ttl=timedelta(hours=4)) # 데이터 캐싱 설정 (4시간 유효)
def load_data(tickers, start, end):
    """
    yfinance를 사용하여 지정된 티커들의 수정 종가 데이터를 안전하게 가져옵니다.
    KeyError 방지 로직이 포함되어 있습니다.
    """
    st.info(f"데이터를 다운로드 중입니다: {start} 부터 {end}")
    
    # yf.download는 MultiIndex DataFrame을 반환합니다.
    data = yf.download(tickers, start=start, end=end, progress=False)
    
    if data.empty:
        st.error("지정된 기간 동안의 주가 데이터를 가져오지 못했습니다. 티커 또는 기간을 확인해주세요.")
        return pd.DataFrame()

    # 데이터프레임의 컬럼 레벨이 2개이고 'Adj Close'가 첫 번째 레벨에 있는지 확인
    if isinstance(data.columns, pd.MultiIndex):
        if 'Adj Close' in data.columns.get_level_values(0):
            # 'Adj Close' 데이터만 선택합니다. (KeyError 방지)
            adj_close_data = data['Adj Close']
            
            # 모든 값이 NaN인 컬럼(다운로드 실패한 티커)을 제거합니다.
            adj_close_data = adj_close_data.dropna(axis=1, how='all')
            
            # 모든 데이터가 제거되었는지 최종 확인
            if adj_close_data.empty:
                 st.error("성공적으로 데이터를 다운로드한 티커가 없습니다. 티커 목록을 확인해주세요.")
                 return pd.DataFrame()
                 
            return adj_close_data
        else:
            # MultiIndex이지만 'Adj Close'가 없는 경우
            st.error("다운로드된 데이터에서 'Adj Close' 컬럼을 찾을 수 없습니다. (데이터 구조 오류)")
            return pd.DataFrame()
    else:
        # 단일 티커만 다운로드했거나, 예상치 못한 형식인 경우
        if 'Adj Close' in data.columns:
            return data[['Adj Close']]
        else:
            st.error("다운로드된 데이터 형식이 예상과 다릅니다. 'Adj Close' 컬럼을 찾을 수 없습니다.")
            return pd.DataFrame()


# --- Streamlit 앱 실행 (Streamlit App) ---

st.set_page_config(
    page_title="미국 시가총액 상위 10개 기업 주가 변동",
    layout="wide"
)

st.title("💰 미국 주식 시가총액 상위 10개 기업 주가 변동")
st.markdown(f"**기간:** {start_date.strftime('%Y년 %m월 %d일')} ~ {end_date.strftime('%Y년 %m월 %d일')} (최근 10년)")

# 데이터 로드 (Streamlit의 spinner로 로딩 표시)
with st.spinner("주가 데이터를 로딩 중입니다..."):
    stock_data = load_data(TICKERS, start_date, end_date)

# 데이터 유효성 검사 및 시각화
if not stock_data.empty:
    
    # 1. 주가 변동 (원화폐 가치)
    st.subheader("1. 주가 변동 (원화폐 가치)")
    st.line_chart(stock_data.rename(columns=TICKER_NAMES))
    
    # 2. 정규화된 수익률 데이터 계산 (모든 주가를 시작 시점의 100으로 설정)
    normalized_data = (stock_data / stock_data.iloc[0]) * 100
    
    st.subheader("2. 정규화된 주가 변동 (시작 시점=100)")
    st.info("이 차트는 **10년간의 상대적인 수익률**을 비교합니다. 시작 시점의 주가를 100으로 설정했습니다.")
    st.line_chart(normalized_data.rename(columns=TICKER_NAMES))
    
    # 3. 데이터 테이블
    st.subheader("데이터 테이블 (수정 종가)")
    display_data = stock_data.copy()
    display_data.index = display_data.index.strftime('%Y-%m-%d')
    display_data.rename(columns=TICKER_NAMES, inplace=True)
    st.dataframe(display_data.tail(10)) # 최근 10개 행만 표시
    
    st.markdown("---")
    st.caption("데이터 출처: Yahoo Finance (`yfinance` 라이브러리) | 시가총액 기준 상위 10개 기업 목록은 시점에 따라 다를 수 있습니다.")
