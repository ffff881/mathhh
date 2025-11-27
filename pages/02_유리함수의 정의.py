import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 배경색: RGB(203,147,160)
st.markdown(
    """
    <style>
    .stApp {
        background-color: rgb(203,147,160);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("유리함수 개념")

# 1️⃣ 정의
st.header("유리함수의 정의")
st.write("""
유리함수는 두 다항식의 비로 정의되는 함수입니다.

$$ f(x) = \\frac{P(x)}{Q(x)} $$

여기서 P(x), Q(x)는 다항식이고, Q(x) ≠ 0 입니다.
""")

# 2️⃣ 성질
st.header("유리함수의 성질")
st.write("""
- 정의역: 분모가 0이 아닌 모든 실수  
- 그래프에는 수직, 수평, 사선 점근선이 나타날 수 있음  
- 분자의 차수와 분모의 차수에 따라 그래프 형태가 달라집니다
""")

# 3️⃣ 기본형 그래프
st.header("유리함수 기본형 그래프 예시")

x_vals = np.linspace(-10,10,400)

# 예시 1: f(x) = 1/x
x1 = x_vals[x_vals != 0]
y1 = 1 / x1
plt.figure(figsize=(6,4))
plt.plot(x1, y1, label='f(x) = 1/x')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.title("f(x) = 1/x")
plt.grid(True)
plt.legend()
st.pyplot(plt)

# 예시 2: f(x) = (x+1)/(x-1)
x2 = x_vals[x_vals != 1]
y2 = (x2 + 1)/(x2 - 1)
plt.figure(figsize=(6,4))
plt.plot(x2, y2, label='f(x) = (x+1)/(x-1)')
plt.axhline(1, color='green', linestyle='--', label='y=1')
plt.axvline(1, color='red', linestyle='--', label='x=1')
plt.title("f(x) = (x+1)/(x-1)")
plt.grid(True)
plt.legend()
st.pyplot(plt)
