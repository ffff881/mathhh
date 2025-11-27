import streamlit as st
import random
from PIL import Image

st.set_page_config(page_title="유리함수 문제집", page_icon="📘", layout="centered")

# 💗 배경색 적용 (RGB(203,147,160))
page_bg = """
<style>
    [data-testid="stAppViewContainer"] {
        background-color: rgb(203, 147, 160);  /* 메인 배경 */
    }
    [data-testid="stHeader"] {
        background-color: rgb(188, 130, 143);  /* 헤더 부분 */
    }
    [data-testid="stSidebar"] {
        background-color: rgb(216, 165, 177);  /* 사이드바 부분 */
    }
    /* 카드 스타일 느낌으로 문제 영역 강조 */
    div[data-testid="stVerticalBlock"] > div {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 10px 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 이미지 경로 (images 폴더 아래에 IMG_0019.png 를 넣어주세요)
GANADI_PATH = "images/IMG_0019.png"

st.title("📗 유리식 문제집 (고1 수준)")
st.write("유리식의 성질 · 연산 · 유리함수 성질 문제 총 15문제 — 객관식 보기 5개")

# -----------------------
# 유리식 연산 문제 생성: 결과가 정수(1~100)로 떨어지도록 반복 생성
# -----------------------
def generate_rational_operation():
    for _ in range(500):
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        c = random.randint(1, 12)
        d = random.randint(1, 12)
        op = random.choice(["+", "-", "*", "/"])

        if op == "+":
            expr = f"({a}/{b}) + ({c}/{d})"
            num = a * d + b * c
            den = b * d
        elif op == "-":
            expr = f"({a}/{b}) - ({c}/{d})"
            num = a * d - b * c
            den = b * d
        elif op == "*":
            expr = f"({a}/{b}) × ({c}/{d})"
            num = a * c
            den = b * d
        else:
            expr = f"({a}/{b}) ÷ ({c}/{d})"
            num = a * d
            den = b * c

        if den == 0:
            continue
        if num % den != 0:
            continue
        value = num // den
        if 1 <= value <= 100:
            return expr, str(value)
    return "(1/1) + (1/1)", "2"

# -----------------------
# 객관식 개념 문제 (고1 공통수학 수준)
# -----------------------
concept_problems = [
    ("유리식의 정의로 가장 알맞은 것은?", "두 다항식의 나눗셈 꼴",
     ["두 다항식의 나눗셈 꼴", "항상 정수만으로 이루어진 식", "분모가 없는 식", "상수 함수만 해당", "항상 1차식"]),
    ("유리함수 f(x)=1/x의 정의역에서 제외되는 값은?", "x=0",
     ["x=1", "x=0", "모든 실수", "x=-1", "정의역에 제외되는 값이 없다"]),
    ("유리식의 곱셈을 할 때 올바른 규칙은?", "분자끼리 곱하고 분모끼리 곱한다",
     ["분자끼리 곱하고 분모끼리 곱한다", "분자를 통분한다", "항상 통분 후 더한다", "분모끼리 더한다", "분모를 없앤다"]),
    ("유리함수의 수직점근선이 생기는 이유는?", "분모가 0이 되는 x 값 때문",
     ["분자가 0이 되는 x 값 때문", "함수값이 무한대일 때", "항상 y=0 때문", "그래프가 교차할 때", "분모가 1일 때"]),
    ("수평점근선의 의미로 옳은 것은?", "x → ±∞ 일 때 y가 가까워지는 직선",
     ["x → ±∞ 일 때 y가 가까워지는 직선", "항상 y=0인 직선", "그래프가 반드시 지나는 직선", "수직선 형태", "존재할 수 없다"]),
    ("유리식의 덧셈에서 통분을 하는 이유는?", "분모를 동일하게 만들어 더하기 위해",
     ["분모를 동일하게 만들어 더하기 위해", "분자를 0으로 만들기 위해", "항상 약분하기 위해", "곱셈을 쉽게 하기 위해", "함수의 값을 바꾸기 위해"]),
    ("다음 중 유리함수가 아닌 것은?", "f(x)=3x+2",
     ["f(x)=1/x", "f(x)=(x+1)/(x-2)", "f(x)=3x+2", "f(x)=(x^2+1)/(x+3)", "f(x)=(2x-1)/(x^2+1)"]),
    ("유리함수 그래프의 일반적 모양은?", "쌍곡선",
     ["쌍곡선", "직선", "포물선", "원", "곡선 없음"]),
]

# -----------------------
# 문제 조합 만들기
# -----------------------
problems = []
for q, ans, opts in concept_problems:
    problems.append((q, ans, opts.copy()))

for _ in range(6):
    expr, correct = generate_rational_operation()
    wrongs = set()
    while len(wrongs) < 4:
        w = str(random.randint(1, 100))
        if w != correct:
            wrongs.add(w)
    options = list(wrongs) + [correct]
    random.shuffle(options)
    problems.append((f"다음을 계산하시오: {expr}", correct, options))

problems.append(("유리함수에서 분모가 0이면 어떤 일이 일어나나요?", "정의되지 않는다",
                 ["정의된다", "무한히 커진다", "정의되지 않는다", "항상 0이 된다", "함수값이 1이 된다"]))

assert len(problems) == 15, f"문제 개수 오류: {len(problems)} (기대값 15)"

# -----------------------
# 문제 출력 및 채점
# -----------------------
st.markdown("## 🧮 문제 풀이 (총 15문제)")
score = 0

ganadi_img = None
try:
    ganadi_img = Image.open(GANADI_PATH)
except Exception:
    ganadi_img = None

for i, (q, answer, opts) in enumerate(problems, start=1):
    st.write(f"### {i}. {q}")
    choice = st.radio(f"문제 {i} 답 선택:", opts, key=f"q{i}")

    if choice:
        if choice == answer:
            st.success("정답이야! 🎉")
            score += 1
        else:
            st.error("응 아니야 😅")
            if ganadi_img:
                st.image(ganadi_img, caption="가나디: 응 아니야!", use_column_width=False)
            else:
                st.warning(f"오답일 때 표시할 이미지({GANADI_PATH})를 찾을 수 없습니다. "
                           "images/IMG_0019.png 파일을 프로젝트의 images 폴더에 넣어주세요.")

st.markdown("---")
st.write(f"### ✅ 총 {len(problems)}문제 중 정답: {score}문제")

if score == len(problems):
    st.balloons()
    st.success("완벽해요! 유리식 달인입니다 🌟")
elif score >= 10:
    st.info("잘했어요! 조금만 더 연습해요 💪")
else:
    st.warning("복습이 필요해요. 다시 한번 풀어볼까요? 📘")
