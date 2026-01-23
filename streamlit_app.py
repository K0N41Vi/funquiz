```python
import streamlit as st
import random

# =====================
# 雑学クイズデータ（増量版）
# =====================
quiz = [
    {"id": 1, "question": "日本で一番面積が大きい都道府県は【　】である。", "answer": "北海道", "hints": ["都でも府でもない", "2位の約4倍", "本州とトンネルで接続"]},
    {"id": 2, "question": "光の速さは約【　】km/秒である。", "answer": "300000", "hints": ["1秒で地球7周", "音より圧倒的に速い", "物理定数"]},
    {"id": 3, "question": "タコの心臓の数は【　】個である。", "answer": "3", "hints": ["人間より多い", "血液が青い理由と関係", "1つは全身用ではない"]},
    {"id": 4, "question": "雷の音が遅れて聞こえるのは【　】の伝わる速さが遅いためである。", "answer": "音", "hints": ["空気の振動", "真空では伝わらない", "光とは桁違い"]},
    {"id": 5, "question": "人間の体で一番硬い部分は【　】である。", "answer": "歯", "hints": ["骨ではない", "エナメル質", "噛むため"]},
    {"id": 6, "question": "富士山の標高は約【　】mである。", "answer": "3776", "hints": ["3000m以上", "日本最高峰", "語呂合わせが有名"]},
    {"id": 7, "question": "ペンギンは【　】ことができない。", "answer": "飛ぶ", "hints": ["翼はある", "泳ぎは得意", "鳥類"]},
    {"id": 8, "question": "世界で一番話者数が多い言語は【　】語である。", "answer": "中国", "hints": ["英語ではない", "人口が多い国", "漢字を使う"]},
    {"id": 9, "question": "血液型を最初に発見したのは【　】人である。", "answer": "オーストリア", "hints": ["ヨーロッパ", "20世紀初頭", "医学者"]},
    {"id": 10, "question": "人は一生で約【　】回まばたきをする。", "answer": "100000000", "hints": ["1億回", "無意識", "目を守る"]},
]

# =====================
# 初期化
# =====================
if "unused" not in st.session_state:
    st.session_state.unused = quiz.copy()
    random.shuffle(st.session_state.unused)
    st.session_state.current = st.session_state.unused.pop()
    st.session_state.hint_level = 0
    st.session_state.history = []
    st.session_state.wrong = []
    st.session_state.answered = False

# =====================
# UI
# =====================
st.title("🧠 雑学クイズ")

st.subheader("問題")
st.write(st.session_state.current["question"])

answer = st.text_input("答えを入力", key="answer")

if st.button("ヒント"):
    hl = st.session_state.hint_level
    if hl < len(st.session_state.current["hints"]):
        st.warning(st.session_state.current["hints"][hl])
        st.session_state.hint_level += 1

if st.button("回答"):
    correct = answer.strip() == st.session_state.current["answer"]
    st.session_state.history.append((st.session_state.current, correct))
    if not correct and st.session_state.current not in st.session_state.wrong:
        st.session_state.wrong.append(st.session_state.current)
    st.session_state.answered = True

if st.session_state.answered:
    if answer.strip() == st.session_state.current["answer"]:
        st.success("⭕ 正解")
    else:
        st.error(f"❌ 不正解：正解は {st.session_state.current['answer']}")

    if st.button("次の問題へ"):
        if not st.session_state.unused:
            st.session_state.unused = quiz.copy()
            random.shuffle(st.session_state.unused)
        st.session_state.current = st.session_state.unused.pop()
        st.session_state.hint_level = 0
        st.session_state.answered = False
        st.session_state.pop("answer", None)
```
