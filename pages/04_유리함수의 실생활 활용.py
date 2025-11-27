import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --------------------- 기본 설정 ---------------------
st.set_page_config(page_title="유리함수 실생활 | 공통수학Ⅱ", page_icon="📘", layout="wide")

# --------------------- CSS ---------------------
st.markdown("""
<style>
/* 🎨 RGB(203,147,160) 기반 핑크 배경 */
.stApp { 
    background-color: rgb(203,147,160);
}

/* 카드 스타일 */
.card{
    background:#ffffffdd;
    border:1px solid #f1c4cc;
    border-radius:14px;
    padding:18px 22px;
    box-shadow:0 6px 18px rgba(100,0,50,0.1);
    margin-bottom:14px;
}

/* 제목 */
h1.title{ text-align:center; color:#6a0f2f; font-weight:800; }
h3.section{ color:#661a35; margin-top:6px; }

/* 수식 강조 */
.mathbox{
    background:#fff6f8;
    border-left:4px solid #d97b94;
    padding:12px 14px;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# --------------------- 제목 ---------------------
st.markdown('<h1 class="title">공통수학Ⅱ — 유리함수의 실생활 활용</h1>', unsafe_allow_html=True)

# --------------------- 도입 ---------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.write("""
교과서의 “**블록체인 전문가, 함수 암호로 정보를 보호하다**” 내용처럼  
**유리함수는 실생활에서도 비율과 역비례 관계를 표현하는 데** 자주 쓰인다.

보안을 강화하기 위해 데이터를 암호화하면 계산 속도가 느려지고,  
서버 수를 늘리면 전체 계산 속도가 빨라진다.  
이 관계가 바로 **유리함수의 구조**로 나타난다.
""")
st.markdown('</div>', unsafe_allow_html=True)

# --------------------- 개념 ---------------------
st.markdown('<h3 class="section">1️⃣ 왜 유리함수일까?</h3>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.write("""
암호화된 데이터를 여러 대의 서버에서 처리한다고 할 때,  
- 암호화 때문에 계산이 느려지는 정도를 **s (배)**,  
- 전체 해야 할 계산량을 **W**,  
- 서버 한 대의 처리속도를 **r**,  
- 서버의 수를 **x**라고 하면,  

총 걸리는 시간은 아래처럼 계산된다:
""")
st.markdown('<div class="mathbox">', unsafe_allow_html=True)
st.latex(r"T(x) = \frac{s \times W}{r \times x}")
st.markdown('</div>', unsafe_allow_html=True)

st.write("""
| 기호 | 의미 |
|:--:|:--|
| \(T(x)\) | 총 처리 시간 |
| \(s\) | 암호화로 인한 느려짐(배수) |
| \(W\) | 전체 연산량 |
| \(r\) | 서버 1대 처리속도 |
| \(x\) | 서버(노드) 수 |

이 식은 **유리함수**이며, \(x\)가 커질수록 \(T(x)\)는 작아지는 **역비례 관계**를 보여준다.
""")
st.markdown('</div>', unsafe_allow_html=True)

# --------------------- 그래프 ---------------------
st.markdown('<h3 class="section">2️⃣ 그래프로 보기</h3>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

s = st.slider("암호화 느려짐 정도 s (배)", 1, 100, 20, 1)
W = st.slider("전체 연산량 W", 100, 1000, 400, 50)
r = st.slider("서버 1대 처리속도 r", 10, 200, 50, 5)

x = np.linspace(1, 200, 400)
T = (s * W) / (r * x)

fig, ax = plt.subplots()
ax.plot(x, T)
ax.set_xlabel("서버 수 x (대)")
ax.set_ylabel("처리 시간 T")
ax.set_title("🔒 암호화된 데이터 처리 시간 — 유리함수 관계")
ax.grid(True, alpha=0.3)
st.pyplot(fig)

st.markdown("""
<div class="mathbox">
<b>그래프 해석:</b><br>
서버 수 \(x\)가 많아질수록 시간 \(T(x)\)는 짧아진다.<br>
즉, “서버 수 ↑ → 시간 ↓”은 **역비례** 관계이다.<br>
보안을 강화(암호화 배수 ↑)하면 \(T(x)\) 전체가 위로 올라가 느려진다.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------- 정리 ---------------------
st.markdown('<h3 class="section">3️⃣ 정리</h3>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.write("""
| 실생활 예시 | 유리함수 형태 | 의미 |
|:--|:--|:--|
| 🚗 속력과 시간 | \(T = \\dfrac{d}{x}\) | 속력이 빠를수록 시간은 짧아짐 |
| 💧 농도 희석 | \(C = \\dfrac{pV_0}{V_0 + x}\) | 물을 더 넣을수록 농도 낮아짐 |
| 👷 작업 분담 | \(T = \\dfrac{W}{x}\) | 사람이 많을수록 시간 줄어듦 |
| 🔒 암호화 데이터 처리 | \(T = \\dfrac{sW}{r x}\) | 서버가 많을수록 빨라지고, 보안이 강할수록 느려짐 |

📖 유리함수는 이렇게 **분모에 변수가 있는 역비례 현상**을 표현할 때 쓰인다.
""")
st.markdown('</div>', unsafe_allow_html=True)

# --------------------- 푸터 ---------------------
st.markdown(
    '<div style="text-align:center;color:#4b0f25;margin-top:10px;">'
    '© 공통수학Ⅱ — 유리함수의 실생활 활용 (블록체인/보안 사례, RGB(203,147,160) 테마)'
    '</div>', unsafe_allow_html=True
)
