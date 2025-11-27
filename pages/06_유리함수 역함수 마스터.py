import streamlit as st
import random
from sympy import symbols, simplify, Function, Eq
import numpy as np
import matplotlib.pyplot as plt

# -----------------
# 1. 앱 설정 및 제목
# -----------------
st.set_page_config(page_title="유리함수의 역함수 마스터 🎓 (V3)", layout="centered")
st.title("유리함수의 역함수 마스터 🎓")
st.markdown("---")

# -----------------
# 2. 개념 학습 섹션
# -----------------
st.header("1. 유리함수의 역함수 개념 학습")

st.markdown("""
유리함수 $f(x) = \frac{ax + b}{cx + d}$ ($c \neq 0, ad - bc \neq 0$)의 역함수 $f^{-1}(x)$는 다음 공식으로 쉽게 구합니다.
""")

# 공식 표시
st.latex(r'''
f^{-1}(x) = \frac{-dx + b}{cx - a}
''')


st.markdown("""
🔑 **핵심:** 원래 함수의 분자 $x$ 계수 **$a$**와 분모 상수항 **$d$**의 **위치와 부호를 서로 바꿉니다.**
""")
st.markdown("---")

# -----------------
# 3. 문제 생성 함수 및 상태 관리
# -----------------

def generate_problem():
    """역함수 문제가 될 수 있는 계수 (a, b, c, d)를 생성하고 세션 상태에 저장합니다."""
    while True:
        # 무작위 계수 생성 (-5 ~ 5, 0 포함 가능)
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.choice([x for x in range(-5, 6) if x != 0]) # c는 0이 아니어야 함
        d = random.randint(-5, 5)
        
        # 역함수 존재 조건: ad - bc != 0
        if (a * d - b * c) != 0:
            break
            
    # 세션 상태에 문제 저장
    st.session_state.problem_a = a
    st.session_state.problem_b = b
    st.session_state.problem_c = c
    st.session_state.problem_d = d
    st.session_state.checked = False # 채점 여부 초기화
    
    # **사용자 입력 값 초기화** (새 문제 시 이전 값 제거)
    st.session_state.user_inv_a = 0
    st.session_state.user_inv_b = 0
    st.session_state.user_inv_c = 1 # 분모 x 계수는 0이 아니어야 하므로 1로 초기화
    st.session_state.user_inv_d = 0


# 초기 문제 생성 및 입력값 초기화 (앱 시작 시)
if 'problem_a' not in st.session_state:
    generate_problem()
# 초기 실행 시 입력 위젯 값이 세션 상태에 연결되어 있도록 보장
if 'user_inv_a' not in st.session_state:
    st.session_state.user_inv_a = 0
    st.session_state.user_inv_b = 0
    st.session_state.user_inv_c = 1 
    st.session_state.user_inv_d = 0


# -----------------
# 4. 문제 풀이 섹션
# -----------------

st.header("2. 역함수 문제 풀이")
st.subheader("아래 함수의 역함수 $f^{-1}(x)$를 구하시오.")

# 현재 문제 표시
a = st.session_state.problem_a
b = st.session_state.problem_b
c = st.session_state.problem_c
d = st.session_state.problem_d

st.latex(f'''
f(x) = \frac{{{a}x + {b}}}{{{c}x + {d}}}
''')

st.markdown("---")

# -----------------
# 5. 사용자 입력 및 채점 로직
# -----------------

# SymPy를 사용하여 수학적 검증을 위한 함수 정의
x = symbols('x')

def check_answer():
    """사용자 입력과 정답을 SymPy를 사용하여 비교하고 채점합니다."""
    st.session_state.checked = True
    
    # 정답 계수
    inv_a_true = -d
    inv_b_true = b
    inv_c_true = c
    inv_d_true = -a
    
    # 사용자 입력 계수 (세션 상태에서 바로 가져옴)
    user_a = st.session_state.user_inv_a
    user_b = st.session_state.user_inv_b
    user_c = st.session_state.user_inv_c
    user_d = st.session_state.user_inv_d

    is_correct = False
    
    # C=0 예외 처리 (분모가 상수가 되어 유리함수 형태를 벗어남)
    if user_c == 0:
        st.error("❌ **오답입니다.** 역함수 $f^{-1}(x)$가 유리함수 형태를 유지하려면, 분모 $x$ 계수 (C)는 0이 아니어야 합니다.")
        st.session_state.checked = False
        return

    # 1. 정답 함수 정의 (SymPy Expression)
    true_inverse_func = (inv_a_true * x + inv_b_true) / (inv_c_true * x + inv_d_true)
    
    # 2. 사용자 함수 정의 (SymPy Expression)
    try:
        user_inverse_func = (user_a * x + user_b) / (user_c * x + user_d)
        
        # 3. 두 함수의 상등 비교 (SymPy simplify를 사용하여 상수배 관계까지 허용)
        difference = simplify(user_inverse_func - true_inverse_func)
        
        # difference가 0이면 두 함수는 수학적으로 동일
        is_correct = (difference == 0)
        
    except Exception:
        is_correct = False
        
    
    # -----------------
    # 채점 결과 및 피드백 표시
    # -----------------
    if is_correct:
        st.success("🎉 **정답입니다!** 역함수 공식을 완벽하게 이해했어요.")
        # 정답일 때만 그래프 표시 트리거
        st.session_state.show_graph = True 
    else:
        st.error("❌ **오답입니다.** 다시 한번 공식을 확인하고 풀어보세요.")
        st.session_state.show_graph = False # 오답 시 그래프 숨기기
        st.markdown("---")
        st.subheader("📝 정답 해설")
        st.markdown(f"""
        주어진 함수 $f(x) = \\frac{{{a}x + {b}}}{{{c}x + {d}}}$ 에 대해
        * **$a = {a}$** 와 **$d = {d}$** 의 위치와 부호를 바꿉니다.
        * 바꾼 값: $-d = {-d}$, $-a = {-a}$
        
        따라서 정답 계수는 $A={inv_a_true}, B={inv_b_true}, C={inv_c_true}, D={inv_d_true}$ 이며,
        역함수는 다음과 같습니다.
        $$f^{-1}(x) = \\frac{{({inv_a_true}) x + {inv_b_true}}}{{{inv_c_true} x + {inv_d_true}}}$$
        """)


st.subheader("🔑 정답 입력")
st.markdown("$$f^{-1}(x) = \\frac{A x + B}{C x + D}$$ 일 때, 정수 계수 A, B, C, D의 값을 입력하세요.")

col1, col2 = st.columns(2)
with col1:
    user_inv_a = st.number_input("분자 $x$ 계수 (A):", key="user_inv_a", value=st.session_state.user_inv_a, format="%d")
    user_inv_b = st.number_input("분자 상수항 (B):", key="user_inv_b", value=st.session_state.user_inv_b, format="%d")

with col2:
    user_inv_c = st.number_input("분모 $x$ 계수 (C):", key="user_inv_c", value=st.session_state.user_inv_c, format="%d")
    user_inv_d = st.number_input("분모 상수항 (D):", key="user_inv_d", value=st.session_state.user_inv_d, format="%d")


col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    st.button("✅ 정답 확인", on_click=check_answer)

with col_btn2:
    # 새 문제 버튼 클릭 시 그래프 숨김
    st.button("🔄 새 문제", on_click=lambda: (generate_problem(), setattr(st.session_state, 'show_graph', False)))


# -----------------
# 6. 그래프 시각화 섹션 (새로 추가)
# -----------------

if 'show_graph' not in st.session_state:
    st.session_state.show_graph = False


if st.session_state.checked and st.session_state.show_graph:
    st.markdown("---")
    st.header("3. 함수와 역함수의 그래프 비교")

    # 계수 정의
    a, b, c, d = st.session_state.problem_a, st.session_state.problem_b, st.session_state.problem_c, st.session_state.problem_d
    
    # 정답 역함수 계수
    inv_a, inv_b, inv_c, inv_d = -d, b, c, -a

    # 점근선 계산
    va_f = -d / c  # f(x)의 세로 점근선
    ha_f = a / c   # f(x)의 가로 점근선

    va_inv = -inv_d / inv_c # f^-1(x)의 세로 점근선 (ha_f와 같음)
    ha_inv = inv_a / inv_c  # f^-1(x)의 가로 점근선 (va_f와 같음)
    
    # 함수 정의 (그래프용)
    def func_f(x):
        return (a * x + b) / (c * x + d)

    def func_inv(x):
        return (inv_a * x + inv_b) / (inv_c * x + inv_d)

    # 그래프 범위 설정
    x_min = min(va_f, va_inv) - 5
    x_max = max(va_f, va_inv) + 5
    
    # 🌟 x 값 생성 (점근선 주변 분리) 🌟
    # f(x)의 점근선(va_f) 기준
    x1_f = np.linspace(x_min, va_f - 0.1, 300)
    x2_f = np.linspace(va_f + 0.1, x_max, 300)
    
    # f^-1(x)의 점근선(va_inv) 기준
    x1_inv = np.linspace(x_min, va_inv - 0.1, 300)
    x2_inv = np.linspace(va_inv + 0.1, x_max, 300)
    
    # y 값 계산
    y1_f = func_f(x1_f)
    y2_f = func_f(x2_f)
    
    y1_inv = func_inv(x1_inv)
    y2_inv = func_inv(x2_inv)

    # Matplotlib 그리기
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 1. f(x) 그래프
    ax.plot(x1_f, y1_f, label=r'$f(x)$', color='blue')
    ax.plot(x2_f, y2_f, color='blue')

    # 2. f^-1(x) 그래프
    ax.plot(x1_inv, y1_inv, label=r'$f^{-1}(x)$', color='orange')
    ax.plot(x2_inv, y2_inv, color='orange')

    # 3. 점근선 표시
    ax.axvline(va_f, color='blue', linestyle='--', linewidth=1, alpha=0.6, label=r'$f(x)$ VA')
    ax.axhline(ha_f, color='blue', linestyle='--', linewidth=1, alpha=0.6, label=r'$f(x)$ HA')
    
    ax.axvline(va_inv, color='orange', linestyle=':', linewidth=1, alpha=0.6, label=r'$f^{-1}(x)$ VA')
    ax.axhline(ha_inv, color='orange', linestyle=':', linewidth=1, alpha=0.6, label=r'$f^{-1}(x)$ HA')
    
    # 4. y=x 대칭선
    ax.plot([-10, 10], [-10, 10], color='gray', linestyle='-.', linewidth=1, alpha=0.5, label='$y=x$')
    
    # 그래프 설정
    ax.set_title(r'$f(x)$와 $f^{-1}(x)$ 그래프')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-10, 10)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(loc='lower right')
    ax.set_aspect('equal', adjustable='box') # x, y 축 비율 맞추기

    st.pyplot(fig)
