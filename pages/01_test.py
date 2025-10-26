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
start_date = end_date - timedelta(days=365 * 10) # 대략 10년 전

# --- 데이터 가져오기 (Data Fetching) ---

@st.cache_data(ttl=timedelta(hours=4)) # 데이터 캐싱 설정 (4시간 유효)
def load_data(tickers, start, end):
    """
    yfinance를 사용하여 지정된 티커들의 수정 종가 데이터를 안전하게 가져옵니다.
    KeyError 및 데이터 구조 오류 방지 로직이 포함되어 있습니다.
    """
    st.info(f"데이터 다운로드 시도: {start} 부터 {end}")
    
    # progress=False: yfinance 메시지 출력을 줄임
    # ignore_tz=True: 시간대 문제를 방지 (날짜 인덱스 처리 단순화)
    data = yf.download(tickers, start=start, end=end, progress=False, ignore_tz=True)
    
    if data.empty:
        st.error("지정된 기간 동안의 주가 데이터를 가져오지 못했습니다. 티커 또는 기간을 확인해주세요.")
        return pd.DataFrame()

    adj_close_data = pd.DataFrame()
    
    # 1. MultiIndex (다중 티커) 처리
    if isinstance(data.columns, pd.MultiIndex):
        if 'Adj Close' in data.columns.get_level_values(0):
            # 표준 MultiIndex 구조에서 'Adj Close' 레벨 선택
            adj_close_data = data['Adj Close']
        else:
            # MultiIndex이지만 'Adj Close'가 없는 경우 (드문 오류 처리)
            # 모든 컬럼 이름을 문자열로 평탄화 (예: ('Close', 'AAPL') -> 'Close, AAPL')
            data.columns = [', '.join(col).strip() for col in data.columns.values]
            
            # 'Adj Close'를 포함하는 컬럼만 선택
            adj_close_cols = [col for col col in data.columns if 'Adj Close' in col]
            adj_close_data = data[adj_close_cols]
            
            # 컬럼 이름을 티커만 남도록 정리 (예: 'Adj Close, AAPL' -> 'AAPL')
            new_columns = [col.split(', ')[-1] for col in adj_close_data.columns]
            adj_close_data.columns = new_columns
    
    # 2. 단일 Index (단일 티커) 처리
    elif 'Adj Close' in data.columns:
        # 단일 티커만 다운로드된 경우
        adj_close_data = data[['Adj Close']]
        # 다운로드 성공한 티커의 컬럼 이름을 설정 (yfinance에서 항상 'Adj Close'로 반환될 때)
        # 이 경우 모든 티커가 실패하고 하나만 남았을 가능성이 높습니다.
        if len(adj_close_data.columns) == 1:
            # 어떤 티커가 성공했는지 확실하지 않으므로, 데이터가 비어있지 않으면 그대로 진행
            pass 
        
    else:
        st.error(f"예상치 못한 데이터 구조 오류가 발생했습니다. 컬럼: {data.columns.tolist()}")
        return pd.DataFrame()

    # 3. 최종 정리 및 검증
    # 모든 값이 NaN인 컬럼(데이터가 없는 티커)을 제거합니다.
    adj_close_data = adj_close_data.dropna(axis=1, how='all')
    
    if adj_close_data.empty:
        st.error("성공적으로 데이터를 다운로드한 티커가 없습니다. 티커 목록을 확인해주세요.")
        return pd.DataFrame()

    return adj_close_data


# --- Streamlit 앱 실행 (Streamlit App) ---

st.set_page_config(
    page_title="미국 시가총액 상위 10개 기업 주가 변동",
    layout="wide"
)

st.title("💰 미국 주식 시가총액 상위 10개 기업 주가 변동")
st.markdown(f"**기간:** {start_date.strftime('%Y년 %m월 %d일')} ~ {end_date.strftime('%Y년 %m월 %d일')} (최근 10년)")

# 데이터 로드
with st.spinner("주가 데이터를 로딩 중입니다..."):
    stock_data = load_data(TICKERS, start_date, end_date)

# 데이터 유효성 검사 및 시각화
if not stock_data.empty:
    
    # 1. 주가 변동 (원화폐 가치)
    st.subheader("1. 주가 변동 (원화폐 가치)")
    st.line_chart(stock_data.rename(columns=TICKER_NAMES))
    
    # 2. 정규화된 수익률 데이터 계산 (모든 주가를 시작 시점의 100으로 설정)
    # 첫 번째 유효한 행을 기준으로 정규화
    first_valid_row = stock_data.iloc[stock_data.first_valid_index()]
    normalized_data = (stock_data / first_valid_row) * 100
    
    st.subheader("2. 정규화된 주가 변동 (시작 시점=100)")
    st.info("이 차트는 **10년간의 상대적인 수익률**을 비교합니다. 각 기업의 주가를 첫 유효 거래일을 100으로 설정했습니다.")
    st.line_chart(normalized_data.rename(columns=TICKER_NAMES))
    
    # 3. 데이터 테이블
    st.subheader("데이터 테이블 (수정 종가)")
    display_data = stock_data.copy()
    display_data.index = display_data.index.strftime('%Y-%m-%d')
    display_data.rename(columns=TICKER_NAMES, inplace=True)
    st.dataframe(display_data.tail(10)) # 최근 10개 행만 표시
    
    st.markdown("---")
    st.caption("데이터 출처: Yahoo Finance (`yfinance` 라이브러리) | 시가총액 기준 상위 10개 기업 목록은 시점에 따라 다를 수 있습니다.")
