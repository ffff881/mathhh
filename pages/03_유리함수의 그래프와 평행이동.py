import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 배경색 설정 (RGB 203,147,160)
st.markdown(
    """
    <style>
    body { background-color: rgb(203,147,160); }
    .stApp { background-color: rgb(203,147,160); }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💗 유리함수의 그래프와 평행이동 (디지털 교과서)")

st.markdown("""
이 단원에서는 **유리함수**의 그래프가 어떻게 변하는지를 학습합니다.  
직접 그래프를 조작하면서 함수의 특징을 탐구해 봅시다.
""")

# ------------------------
# 1️⃣ y = a/x
# ------------------------
st.header("1️⃣ 함수 y = a/x 의 그래프")

a = st.slider("a 값 조절", -5.0, 5.0, 1.0, 0.1)
x = np.linspace(-10, 10, 800)
y = np.where(x != 0, a / x, np.nan)

fig, ax = plt.subplots(figsize=(6,6))
ax.plot(x, y, label=f"y = {a}/x")
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.markdown("""
- a > 0이면 1,3사분면 / a < 0이면 2,4사분면  
- |a|가 클수록 그래프가 더 가파르게 보입니다.
""")

# ------------------------
# 2️⃣ y = (ax + b)/(cx + d)
# ------------------------
st.header("2️⃣ 함수 y = (ax + b) / (cx + d)의 그래프")

a2 = st.slider("a", -5.0, 5.0, 1.0, 0.1)
b2 = st.slider("b", -10.0, 10.0, 0.0, 0.5)
c2 = st.slider("c (0 가능)", -5.0, 5.0, 1.0, 0.1)
d2 = st.slider("d", -10.0, 10.0, 0.0, 0.5)

# 화면 표시 범위
xmin, xmax = -10, 10
ymin, ymax = -10, 10

fig2, ax2 = plt.subplots(figsize=(6,6))

# c = 0 인 경우(일차함수 형태) 처리
if abs(c2) < 1e-9:
    if abs(d2) < 1e-9:
        st.error("⚠️ c = 0 이고 d = 0 이면 함수가 정의되지 않습니다.")
        # 빈 플롯만 표시
        ax2.text(0.5, 0.5, "함수 불가", transform=ax2.transAxes, ha='center')
    else:
        # y = (a/d) x + (b/d)
        slope = a2 / d2
        intercept = b2 / d2
        x_line = np.linspace(xmin, xmax, 400)
        y_line = slope * x_line + intercept
        # 화면 밖의 값은 nan으로 만들어 이상 연결 방지(여기선 불필요하지만 일관성 유지)
        y_line = np.where(np.abs(y_line) > 1e6, np.nan, y_line)
        ax2.plot(x_line, y_line, color='green', label=f"y = {slope:.2f}x + {intercept:.2f}")
        st.info("✅ c = 0 이므로 함수는 일차함수 형태입니다.")
else:
    # 일반적인 유리함수: 분모 = c2*x + d2
    asym_x = -d2 / c2  # 세로점근선 위치
    # 만약 점근선이 화면 범위 안에 있으면 구간을 둘로 나눠서 그림
    eps = 1e-3
    # 구간 왼쪽: xmin .. asym_x - delta, 오른쪽: asym_x + delta .. xmax
    delta = max(0.01, (xmax - xmin) * 1e-3)
    x_left = np.linspace(xmin, min(asym_x - delta, xmax), 500)
    x_right = np.linspace(max(asym_x + delta, xmin), xmax, 500)

    # 계산 시 분모가 0에 가까운 값 제외하고 계산
    def safe_compute(x_arr):
        denom = c2 * x_arr + d2
        # denom가 0에 가깝거나 계산 결과가 너무 큰 경우 np.nan으로 처리
        y_arr = np.full_like(x_arr, np.nan, dtype=float)
        mask = np.abs(denom) > 1e-8
        y_tmp = (a2 * x_arr[mask] + b2) / denom[mask]
        # 화면 범위를 벗어나는 값은 np.nan 으로 바꿔 연결선 방지
        y_tmp = np.where(np.abs(y_tmp) > 1e6, np.nan, y_tmp)
        y_tmp = np.where((y_tmp < ymin*100) | (y_tmp > ymax*100), np.nan, y_tmp)
        y_arr[mask] = y_tmp
        return y_arr

    # 왼쪽/오른쪽 각각 계산 및 플롯 (점근선 근처에서 선 연결 안 됨)
    if len(x_left) > 0:
        y_left = safe_compute(x_left)
        ax2.plot(x_left, y_left, color='tomato')
    if len(x_right) > 0:
        y_right = safe_compute(x_right)
        ax2.plot(x_right, y_right, color='tomato')

    # 점근선(세로/가로) 표시 — 화면 범위에 있을 때만
    if xmin < asym_x < xmax:
        ax2.axvline(asym_x, color='gray', linestyle='--', label=f"x = {asym_x:.2f} (수직점근선)")
    # 가로 점근선 y = a/c
    horiz = a2 / c2
    if ymin < horiz < ymax:
        ax2.axhline(horiz, color='purple', linestyle='--', label=f"y = {horiz:.2f} (수평점근선)")
    else:
        # 그래도 보여주기 위해 점선(범위 밖이면 레이블 없이)
        ax2.axhline(horiz, color='purple', linestyle='--', alpha=0.5)

ax2.axhline(0, color='black', linewidth=1)
ax2.axvline(0, color='black', linewidth=1)
ax2.set_xlim(xmin, xmax)
ax2.set_ylim(ymin, ymax)
ax2.set_aspect('equal')
ax2.grid(True)
ax2.legend(loc='upper right')
st.pyplot(fig2)

st.markdown("""
👉 **그래프 특징 정리**
- 수직점근선 : c x + d = 0 → x = -d/c (화면 범위 내에 있으면 점선으로 표시)
- 수평점근선 : y = a/c
- 세로점근선 근처에서는 그래프를 왼쪽/오른쪽으로 나눠 별도 그려 연결선을 방지합니다.
""")

# ------------------------
# 3️⃣ 퀴즈 (생략되지 않음, 기존과 동일한 형태로 유지)
# ------------------------
st.header("3️⃣ 학습 확인 퀴즈")

with st.form("quiz_form"):
    q1 = st.radio("① y = a/x 에서 a가 음수일 때 그래프는 어느 사분면에 있나요?",
                  ["1, 3사분면", "2, 4사분면", "x축 위"], index=None)

    q2 = st.radio("② y = (ax + b)/(cx + d) 에서 수직점근선은 어디에 있나요?",
                  ["x = -d/c", "y = a/c", "x = 0"], index=None)

    q3 = st.radio("③ y = (ax + b)/(cx + d) 의 수평점근선은?",
                  ["y = a/b", "y = a/c", "y = -d/c"], index=None)

    submit = st.form_submit_button("✅ 답안 제출")

if submit:
    score = 0
    if q1 == "2, 4사분면":
        score += 1
    if q2 == "x = -d/c":
        score += 1
    if q3 == "y = a/c":
        score += 1

    st.subheader(f"🎯 결과: {score}/3 점")
    if score == 3:
        st.success("완벽합니다! 유리함수의 점근선을 정확히 이해했습니다.")
    elif score == 2:
        st.info("좋아요! 한 문제만 더 복습해 봅시다.")
    else:
        st.warning("조금 더 복습이 필요해요. 그래프 변화를 다시 관찰해 보세요.")

st.markdown("""
---
✅ **정리**
- 세로점근선 근처에서는 그래프를 좌/우로 나눠서 그려야 연결선이 생기지 않습니다.  
- c = 0일 경우에는 일차함수 형태가 됨을 유념하세요.
""")
