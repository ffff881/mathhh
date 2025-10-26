import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit 앱의 제목 설정
st.title('이차함수 $y=ax^2$ 그래프 탐구 앱 🧐')

st.markdown("""
이 앱을 통해 이차함수의 기본형 $y=ax^2$의 그래프를 탐구할 수 있습니다.
- **계수 $a$** 값을 변경하여 그래프의 모양이 어떻게 달라지는지 확인해 보세요.
""")

# 계수 a를 조정하는 슬라이더 생성
# -10부터 10까지, 초기값은 1, 스텝은 0.1로 설정합니다.
a = st.slider(
    '계수 $a$ 값 선택:',
    min_value=-5.0,
    max_value=5.0,
    value=1.0,
    step=0.1
)

st.write(f'선택된 이차함수: **$y = {a:.1f}x^2$**')

# 그래프를 그릴 x 값 범위 설정 (NumPy 사용)
x = np.linspace(-10, 10, 400) # -10부터 10까지 400개의 점

# y 값 계산
y = a * x**2

# Matplotlib을 사용하여 그래프 그리기
fig, ax = plt.subplots()
ax.plot(x, y, label=f'$y={a:.1f}x^2$', color='blue')

# 그래프 설정
ax.set_title('이차함수 그래프')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.grid(True)
ax.axhline(0, color='black', linewidth=0.5) # x축
ax.axvline(0, color='black', linewidth=0.5) # y축
ax.set_ylim(-10, 10) # y축 범위 고정
ax.set_xlim(-10, 10) # x축 범위 고정
ax.legend()
ax.set_aspect('equal', adjustable='box') # x, y 축 스케일 동일하게 설정

# Streamlit에 Matplotlib 그래프 표시
st.pyplot(fig)

# 귀납적 관찰을 위한 설명 섹션
st.header('📈 귀납적 관찰 결과')
st.markdown("""
1.  **볼록성 확인:**
    * $a$가 **양수** ($a>0$)일 때: 그래프는 아래로 볼록합니다. (포물선이 위로 열림)
    * $a$가 **음수** ($a<0$)일 때: 그래프는 위로 볼록합니다. (포물선이 아래로 열림)
2.  **그래프의 폭 확인:**
    * $|a|$의 **절댓값**이 커질수록: 그래프의 폭은 **좁아집니다**. (y축에 가까워집니다)
    * $|a|$의 **절댓값**이 작아질수록: 그래프의 폭은 **넓어집니다**. (x축에 가까워집니다)
""")
