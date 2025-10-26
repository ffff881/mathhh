import streamlit as st
import pandas as pd

# 1. 데이터 정의: 시대별 작품 정보 및 이미지 URL (공개 이미지 링크 사용)
ART_DATA = {
    "르네상스 (Renaissance)": {
        "작품": "모나리자 (Mona Lisa)",
        "작가": "레오나르도 다빈치",
        "연도": "1503년 ~ 1506년경",
        "설명": "인본주의와 과학적 관찰이 결합된 르네상스 회화의 최고 걸작입니다. '스푸마토(sfumato)' 기법을 사용해 미묘하고 신비로운 미소를 완성했습니다. 현재 프랑스 루브르 박물관에 소장되어 있습니다.",
        "이미지_URL": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg"
    },
    "바로크 (Baroque)": {
        "작품": "골리앗의 머리를 든 다비드 (David with the Head of Goliath)",
        "작가": "카라바조 (Caravaggio)",
        "연도": "1605년경",
        "설명": "극적인 명암 대비(키아로스쿠로)와 사실적인 묘사가 특징인 바로크 회화의 정수입니다. 카라바조가 자신의 자화상을 골리앗의 머리에 투영한 것으로 알려져 있습니다.",
        "이미지_URL": "https://upload.wikimedia.org/wikipedia/commons/f/ff/David_with_the_Head_of_Goliath-Caravaggio_%281610%29.jpg"
    },
    "팝 아트 (Pop Art)": {
        "작품": "마릴린 디프트 (Marilyn Diptych)",
        "작가": "앤디 워홀 (Andy Warhol)",
        "연도": "1962년",
        "설명": "실크스크린 기법을 사용하여 대중 문화의 아이콘인 마릴린 먼로를 반복적으로 표현한 작품입니다. 대량 생산과 유명인의 덧없는 이미지를 동시에 풍자하고 있습니다.",
        "이미지_URL": "https://upload.wikimedia.org/wikipedia/en/2/22/Andy_Warhol%2C_Marilyn_Diptych%2C_Tate.jpg"
    }
}

# 2. Streamlit 앱 구성 시작
st.set_page_config(
    page_title="시기별 대표 미술 작품", 
    layout="wide"
)

st.title("🎨 시기별 대표 미술 작품과 역사 이야기")
st.markdown("이 앱은 Streamlit을 사용하여 주요 미술 사조의 대표 작품과 배경 지식을 보여줍니다.")
st.divider()

# 3. 사이드바에 시대 선택 박스 배치
# selectbox의 옵션은 ART_DATA의 키(Key) 값, 즉 시대 이름이 됩니다.
selected_period = st.sidebar.selectbox(
    "🏛️ 시대 또는 양식을 선택하세요:",
    list(ART_DATA.keys())
)

# 4. 선택된 시대의 작품 정보 표시
if selected_period in ART_DATA:
    data = ART_DATA[selected_period]
    
    st.header(f"시대: {selected_period}")
    
    # 텍스트와 이미지를 나란히 배치하기 위해 컬럼 사용
    # [2:3] 비율로, 텍스트가 더 많은 공간을 차지하도록 설정
    col_text, col_
