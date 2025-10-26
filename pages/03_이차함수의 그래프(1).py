import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title('이차함수 $y=ax^2$ 그래프 탐구 앱 🧐')

st.markdown("""
**[탐구 방법]**
1.  아래 **슬라이더를 움직여 계수 $a$ 값을 변경**해 보세요.
2.  그래프의 **볼록한 방향**과 **폭**이 어떻게 변하는지 관찰하세요.
3.  탐구 후, 아래 **[탐구 결과 확인]** 섹션에 답을 입력하고 확인 버튼을 누르세요.
""")

# --- 그래프 섹션 ---

# 계수 a를 조정하는 슬라이더 생성
a = st.slider(
    '계수 $a$ 값 선택:',
    min_value=-5.0,
    max_value=5.0,
    value=1.0,
    step=0.1,
    format='%.1f' # 소수점 첫째 자리까지 표시
)

st.subheader(f'현재 함수: $y = {a:.1f}x^2$')

# 그래프를 그릴 x 값 범위 설정
x = np.linspace(-10, 10, 400)
y = a * x**2

# Matplotlib을 사용하여 그래프 그리기
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, color='blue')

# 그래프 설정
ax.set_title('이차함수 $y=ax^2$ 그래프')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.grid(True, linestyle='--', alpha=0.6)
ax.axhline(0, color='black', linewidth=1) # x축
ax.axvline(0, color='black', linewidth=1) # y축
ax.set_ylim(-10, 10) # y축 범위 고정
ax.set_xlim(-10, 10) # x축 범위 고정
# ax.set_aspect('equal', adjustable='box') # 스케일을 동일하게 유지할 경우

st.pyplot(fig)

# --- 탐구 결과 확인 섹션 ---

st.header('✅ 탐구 결과 확인')

# 1. 볼록성 확인 (객관식 - st.radio)
st.subheader('1. 볼록한 방향')
st.markdown('계수 $a$가 양수($a>0$)일 때, 그래프는 어느 방향으로 볼록한가요?')
selected_convexity = st.radio(
    '선택하세요:',
    ('위로 볼록', '아래로 볼록', '볼록하지 않음'),
    key='convexity_quiz'
)

# 2. 그래프 폭 확인 (주관식 - st.text_input)
st.subheader('2. 그래프의 폭')
st.markdown('$|a|$의 값이 **커질수록** 그래프의 폭은 어떻게 되나요?')
selected_width = st.text_input(
    '답을 입력하세요 (예: 좁아진다):',
    key='width_quiz'
)

# 확인 버튼
if st.button('결과 확인'):
    # 볼록성 정답 확인
    correct_convexity = '아래로 볼록'
    if selected_convexity == correct_convexity:
        st.success('✅ 1번 정답입니다! $a>0$일 때, 포물선은 아래로 볼록합니다.')
    else:
        st.error('❌ 1번 오답입니다. $a>0$일 때 그래프를 다시 관찰해 보세요.')

    # 그래프 폭 정답 확인 (띄어쓰기와 대소문자 무시)
    correct_width_keywords = ['좁아진다', '좁아짐', '좁아', '가늘어진다']
    submitted_width_clean = selected_width.replace(' ', '').lower()
    
    is_width_correct = any(keyword in submitted_width_clean for keyword in correct_width_keywords)

    if is_width_correct:
        st.success('✅ 2번 정답입니다! $|a|$가 커질수록 폭은 좁아집니다. ')
    elif submitted_width_clean in ['넓어진다', '넓어짐', '넓어', '두꺼워진다']:
        st.warning('❌ 2번 오답입니다. $|a|$가 **작아질수록** 폭이 넓어집니다. $|a|$가 **커질 때**의 변화를 다시 관찰해 보세요.')
    else:
        st.error('❌ 2번 오답입니다. $|a|$의 값 변화에 따른 그래프의 폭 변화를 다시 관찰해 보세요.')

st.markdown('---')
st.caption('이 앱은 이차함수의 기본형 $y=ax^2$의 성질을 귀납적으로 학습하기 위해 제작되었습니다.')
