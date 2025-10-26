import streamlit as st
import pandas as pd

# 1. 데이터 정의: 시대별 작품 정보 및 이미지 URL
# 공개적으로 접근 가능한 Wikimedia Commons 등의 링크를 사용했습니다.
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
        "설명": "극적인 명암 대비(키아로스쿠로)와 사실적인 묘사가 특징인 바로크 회화의 정수입니다. 카라바조가 자신의 자화상을 골리앗의 머리에 투영한 것으로 알려져 있습니다. 로마 보르게세 미술관 소장.",
        "이미지_URL": "https://upload.wikimedia.org/wikipedia/commons/f/ff/David_with_the_Head_of_Goliath-Caravaggio_%281610%29.jpg"
    },
    "인상주의 (Impressionism)": {
        "작품": "해돋이 인상 (Impression, soleil levant)",
        "작가": "클로드 모네 (Claude Monet)",
        "연도": "1872년",
        "설명": "이 작품의 제목은 인상주의라는 명칭의 유래가 되었습니다. 실내 스튜디오가 아닌 야외에서 순간적인 빛과 색채의 느낌을 포착하려는 화가들의 노력을 상징합니다. 파리 마르모탕 모네 미술관 소장.",
        "이미지_URL": "https://upload.wikimedia.org/wikipedia/commons/5/59/Monet_-_Impression%2C_Soleil_Levant.jpg"
    },
    "팝 아트 (Pop Art)": {
        "작품": "마릴린 디프트 (Marilyn Diptych)",
        "작가": "앤디 워홀 (Andy Warhol)",
        "연도": "1962년",
        "설명": "실크스크린 기법을 사용하여 대중 문화의 아이콘인 마릴린 먼로를 반복적으로 표현한 작품입니다. 대량 생산과 유명인의 덧없는 이미지를 동시에 풍자하고 있습니다.",
        "이미지_URL": "https://upload.wikimedia.org/wikipedia/en/2/22/Andy_Warhol%2C_Marilyn_Diptych%2C_Tate.jpg"
    }
}

# 2. Streamlit 앱 설정
st.set_page_config(
    page_title="시기별 대표 미술 작품", 
    layout="wide" # 넓은 레이아웃 사용
)

st.title("🎨 시기별 대표 미술 작품과 역사 이야기")
st.markdown("---")

# 3. 사이드바에 시대 선택 박스 배치
selected_period = st.sidebar.selectbox(
    "🏛️ 시대 또는 양식을 선택하세요:",
    list(ART_DATA.keys())
)

# 4. 선택된 시대의 작품 정보 표시 (오류 수정된 부분)
if selected_period in ART_DATA:
    data = ART_DATA[selected_period]
    
    st.header(f"**{selected_period}**")
    
    # 텍스트와 이미지를 나란히 배치하기 위해 컬럼 사용 (오류 발생 지점)
    # col_text와 col_image 변수 이름을 정확히 일치시켜 NameError 방지
    col_text, col_image = st.columns([2, 3]) # 텍스트: 2, 이미지: 3 비율

    with col_text:
        st.subheader(f"작품명: **{data['작품']}**")
        st.markdown(f"**🎨 작가:** {data['작가']}")
        st.markdown(f"**📅 제작 연도:** {data['연도']}")
        st.divider()
        st.markdown("### 작품 설명 및 시대적 배경")
        st.write(data["설명"])
        
        # 이미지 출처 표기 (선택 사항)
        st.caption(f"이미지 출처: Wikimedia Commons")

    with col_image:
        # st.image를 사용하여 이미지 URL을 통해 작품을 표시합니다.
        st.image(
            data["이미지_URL"], 
            caption=f"'{data['작품']}' - {data['작가']}", 
            use_column_width=True # 컬럼 폭에 맞게 이미지 크기 조정
        )

# 5. 앱 실행 안내
st.sidebar.markdown("---")
st.sidebar.info("✅ **앱 실행 방법:**\n터미널에서 `streamlit run art_history_app.py`를 실행하세요.")
