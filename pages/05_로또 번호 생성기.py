import streamlit as st
import random

# 최근 로또 당첨 번호 (1195회, 2025년 10월 25일 추첨 기준)
WINNING_NUMBERS = {3, 15, 27, 33, 34, 36}
BONUS_NUMBER = 37

def generate_lotto_numbers(count):
    """1부터 45까지 중 중복 없이 count개의 숫자를 무작위로 생성합니다."""
    return random.sample(range(1, 46), count)

def check_lotto_rank(numbers):
    """
    추천 번호와 당첨 번호를 비교하여 등수를 확인합니다.
    로또 6/45의 당첨 기준:
    1등: 6개 숫자 일치
    2등: 5개 숫자 일치 + 보너스 숫자 일치
    3등: 5개 숫자 일치
    4등: 4개 숫자 일치
    5등: 3개 숫자 일치
    낙첨: 2개 이하 숫자 일치
    """
    
    # 세트(set) 자료형을 사용하여 교집합(일치하는 숫자)을 찾습니다.
    recommended_set = set(numbers)
    
    # 당첨 번호 6개와 일치하는 개수
    match_count = len(recommended_set.intersection(WINNING_NUMBERS))
    
    # 보너스 번호 일치 여부
    is_bonus_match = BONUS_NUMBER in recommended_set

    rank = "낙첨 (2개 이하 일치)"
    
    if match_count == 6:
        rank = "🎉 1등 (6개 일치)"
    elif match_count == 5 and is_bonus_match:
        rank = "✨ 2등 (5개 + 보너스 일치)"
    elif match_count == 5:
        rank = "✅ 3등 (5개 일치)"
    elif match_count == 4:
        rank = "4등 (4개 일치)"
    elif match_count == 3:
        rank = "5등 (3개 일치)"
        
    return rank, match_count, is_bonus_match

# Streamlit 앱 구성
st.title("🍀 로또 번호 추천 및 당첨 확인 앱")

st.markdown("---")

# 추천 받을 번호 개수 입력
num_tickets = st.number_input(
    "몇 개의 로또 번호 조합을 추천받으시겠어요? (1~5)", 
    min_value=1, 
    max_value=5, 
    value=1, 
    step=1
)

# 번호 추천 버튼
if st.button("🔢 로또 번호 추천받기"):
    st.markdown(f"## 🎁 추천 결과 (총 {num_tickets}개 조합)")
    
    # 추천 번호 개수만큼 반복
    for i in range(1, num_tickets + 1):
        # 6개의 로또 번호 생성
        recommended_numbers = generate_lotto_numbers(6)
        
        # 오름차순으로 정렬하여 표시
        recommended_numbers.sort()
        
        st.subheader(f"조합 {i}: {' | '.join(map(str, recommended_numbers))}")
        
        # 등수 확인
        rank, match_count, is_bonus_match = check_lotto_rank(recommended_numbers)
        
        st.markdown(f"**당첨 확인:** {rank}")
        st.markdown(f"*(최근 당첨 번호 {WINNING_NUMBERS}, 보너스 번호 {BONUS_NUMBER} 기준)*")
        st.markdown(f"*일치하는 당첨 번호: **{match_count}개** ({'보너스 번호 일치' if is_bonus_match else '보너스 번호 불일치'})*")
        
        st.markdown("---")
        
st.sidebar.markdown(f"### 📢 **최근 로또 당첨 번호**")
st.sidebar.markdown(f"**1195회 (2025-10-25)**")
st.sidebar.markdown(f"**당첨 번호:** {list(WINNING_NUMBERS)}")
st.sidebar.markdown(f"**보너스 번호:** {BONUS_NUMBER}")
