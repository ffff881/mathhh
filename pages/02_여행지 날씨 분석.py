import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 이집트 주요 도시 리스트
EGYPT_CITIES = [
    "카이로 날씨", 
    "룩소르 날씨", 
    "아스완 날씨", 
    "후르가다 날씨", 
    "알렉산드리아 날씨"
]

def get_weather_data_from_google(city_query):
    """
    Google 검색 결과를 스크래핑하여 날씨 데이터를 가져오는 함수
    """
    # Google 검색 URL 생성
    # 쿼리 문자열을 URL 인코딩하여 한글 검색을 지원합니다.
    encoded_query = urllib.parse.quote(city_query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    # 웹 스크래핑 시 봇으로 인식되지 않도록 User-Agent 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Google 날씨 위젯에서 데이터를 추출합니다.
        # 이 선택자(Selector)는 Google의 HTML 구조에 따라 달라질 수 있습니다.
        location = soup.find("div", id="wob_loc")
        time_desc = soup.find("div", id="wob_dts") # 시간과 날씨 설명
        temp_div = soup.find("span", id="wob_tm") # 현재 온도
        
        # 추가 정보 추출 (습도, 풍속 등)
        # 이 정보는 다른 위치에 있을 수 있으며, ID로 직접 찾기 어려울 수 있습니다.
        # 일반적인 div 클래스에서 찾도록 시도합니다.
        
        # "강수량", "습도", "풍속"을 포함하는 컨테이너
        # *주의*: 이 클래스 선택자는 가장 불안정한 부분입니다.
        details_container = soup.find("div", class_="wob_gbox") 
        
        details = {}
        if details_container:
            # key-value 쌍을 찾기 (예: '강수량: 1%', '습도: 70%', '풍속: 15 km/h')
            for item in details_container.find_all('div', class_="wtsrph"):
                key_elements = item.find_all('span', class_="wob_tbu")
                value_elements = item.find_all('span')
                
                if len(key_elements) >= 1 and len(value_elements) >= 2:
                    key = key_elements[0].text.strip()
                    # 두 번째 span 요소가 값에 해당하는 경우가 많습니다.
                    value = value_elements[1].text.strip()
                    details[key] = value

        
        # 추출된 데이터가 유효한지 확인하고 반환
        if location and temp_div:
            # 추출된 텍스트에서 불필요한 공백 제거
            location_text = location.text.strip()
            temp_text = temp_div.text.strip()
            time_desc_text = time_desc.text.strip() if time_desc else 'N/A'
            
            # 날씨 상태 추출 (ex: 맑음, 흐림)
            weather_status_span = soup.find("span", id="wob_dc")
            weather_status = weather_status_span.text.strip() if weather_status_span else 'N/A'
            
            return {
                "location": location_text,
                "current_time_desc": time_desc_text,
                "temperature": f"{temp_text} °C",
                "status": weather_status,
                "details": details
            }
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"웹 요청 중 오류 발생: {e}")
        return None
    except Exception as e:
        # 스크래핑 실패 (HTML 구조 변경 가능성이 높음)
        st.error(f"스크래핑 중 오류 발생. (HTML 구조 변경 가능성): {e}")
        return None


def display_weather_scraped(city_name, data):
    """
    Streamlit에 스크래핑된 날씨 정보를 표시하는 함수
    """
    st.subheader(f"✨ {city_name} 날씨")
    
    if data:
        st.write(f"**현재 시각:** {data['current_time_desc']}")
        st.write(f"**현재 온도:** {data['temperature']}")
        st.write(f"**날씨 상태:** {data['status']}")
        
        if data['details']:
            st.markdown("**세부 정보:**")
            col1, col2, col3 = st.columns(3)
            # 세부 정보를 3열로 나누어 표시
            detail_list = list(data['details'].items())
            
            if len(detail_list) > 0: col1.write(f"**{detail_list[0][0]}:** {detail_list[0][1]}")
            if len(detail_list) > 1: col2.write(f"**{detail_list[1][0]}:** {detail_list[1][1]}")
            if len(detail_list) > 2: col3.write(f"**{detail_list[2][0]}:** {detail_list[2][1]}")

    else:
        st.warning(f"**{city_name}**의 날씨 정보를 가져오는 데 실패했습니다.")
    
    st.markdown("---")


# Streamlit 앱 구성
st.title("🇪🇬 이집트 주요 도시 날씨 정보 (스크래핑)")
st.caption("🚨 이 앱은 Google 검색 결과를 스크래핑합니다. 웹사이트 구조 변경 시 작동이 멈출 수 있습니다.")
st.markdown("---")

# 모든 도시의 날씨 정보 표시
for city_query in EGYPT_CITIES:
    data = get_weather_data_from_google(city_query)
    display_weather_scraped(city_query.split(' ')[0], data) # 도시 이름만 표시

st.caption("데이터 출처: Google 검색 결과 스크래핑")
