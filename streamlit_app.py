import streamlit as st
import json
import os
import random
from datetime import datetime

# ==============================
# データ保存設定
# ==============================
DATA_FILE = "quiz_history.json"

# ==============================
# クイズデータ（増量版）
# ==============================
QUIZ_DATA = [
    {
        "id": 1,
        "question": "ペンギンは実は何類の動物？",
        "choices": ["哺乳類", "両生類", "鳥類", "爬虫類"],
        "answer": "鳥類",
        "hint": "空は飛べないが、分類は飛べる生き物と同じである。"
    },
    {
        "id": 2,
        "question": "雷が光ってから音が聞こえる理由は？",
        "choices": ["光が遅い", "音が遅い", "距離の錯覚", "空気の屈折"],
        "answer": "音が遅い",
        "hint": "光と音、速さを比べてみると一方は桁違いに速い。"
    },
    {
        "id": 3,
        "question": "人間の体で一番硬い部分は？",
        "choices": ["骨", "歯", "爪", "頭蓋骨"],
        "answer": "歯",
        "hint": "毎日使っているが、実は鉱物に近い性質を持つ。"
    },
    {
        "id": 4,
        "question": "1円玉の素材は何？",
        "choices": ["銅", "アルミニウム", "鉄", "ニッケル"],
        "answer": "アルミニウム",
        "hint": "とても軽く、水に浮く金属である。"
    },
    {
        "id": 5,
        "question": "日本で一番面積が大きい湖は？",
        "choices": ["霞ヶ浦", "琵琶湖", "猪苗代湖", "中海"],
        "answer": "琵琶湖",
        "hint": "関西地方にあり、古くから歌にも詠まれている。"
    },
    {
        "id": 6,
        "question": "人は一生で平均何回くらい瞬きをする？",
        "choices": ["約10万回", "約100万回", "約1億回", "約10億回"],
        "answer": "約1億回",
        "hint": "1分あたりの回数を人生の時間で考えてみる。"
    },
    {
        "id": 7,
        "question": "タコの心臓はいくつある？",
        "choices": ["1つ", "2つ", "3つ", "4つ"],
        "answer": "3つ",
        "hint": "エラ用と全身用で役割が分かれている。"
    },
    {
        "id": 8,
        "question": "エッフェル塔は夏と冬で高さが変わる。その理由は？",
        "choices": ["地盤沈下", "金属の熱膨張", "風圧", "観測誤差"],
        "answer": "金属の熱膨張",
        "hint": "温度で長さが変わる物質の性質が関係している。"
    },
    {
        "id": 9,
        "question": "人間の血液の色が赤い理由は？",
        "choices": ["酸素", "鉄分", "糖分", "二酸化炭素"],
        "answer": "鉄分",
        "hint": "酸素と結びつく金属元素が含まれている。"
    },
    {
        "id": 10,
        "question": "富士山が噴火すると、火山灰が最初に大量に降る可能性が高い都市は？",
        "choices": ["名古屋", "大阪", "東京", "仙台"],
        "answer": "東京",
        "hint": "偏西風の影響を強く受ける位置にある。"
    }
]

# ==============================
# 履歴読み込み・保存
# ==============================

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# ==============================
# 初期化
# ==============================
if "history" not in st.session_state:
    st.session_state.history = load_history()

if "unused_questions" not in st.session_state:
    st.session_state.unused_questions = QUIZ_DATA.copy()
    random.shuffle(st.session_state.unused_questions)

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

# ==============================
# タイトル
# ==============================
st.title("🧠 雑学クイズアプリ")

mode = st.radio("モードを選択", ["通常クイズ", "復習モード", "間違えた問題一覧"])

# ==============================
# 通常クイズ
# ==============================
if mode == "通常クイズ":
    if st.session_state.current_quiz is None:
        if not st.session_state.unused_questions:
            st.success("すべての問題を出題しました！")
        else:
            st.session_state.current_quiz = st.session_state.unused_questions.pop()

    quiz = st.session_state.current_quiz

    if quiz:
        st.subheader(quiz["question"])
        choice = st.radio("選択肢", quiz["choices"], key=quiz["id"])

        if st.button("ヒントを見る"):
            st.info(quiz["hint"])

        if st.button("回答する"):
            correct = choice == quiz["answer"]
            st.session_state.history.append({
                "id": quiz["id"],
                "question": quiz["question"],
                "your_answer": choice,
                "correct_answer": quiz["answer"],
                "correct": correct,
                "time": datetime.now().isoformat()
            })
            save_history(st.session_state.history)

            if correct:
                st.success("正解！")
            else:
                st.error(f"不正解。正解は「{quiz['answer']}」")

            st.session_state.current_quiz = None

# ==============================
# 復習モード
# ==============================
elif mode == "復習モード":
    wrong_ids = {h["id"] for h in st.session_state.history if not h["correct"]}
    review_quizzes = [q for q in QUIZ_DATA if q["id"] in wrong_ids]

    if not review_quizzes:
        st.info("復習する問題はありません")
    else:
        quiz = random.choice(review_quizzes)
        st.subheader(quiz["question"])
        choice = st.radio("選択肢", quiz["choices"], key=f"review_{quiz['id']}")

        if st.button("回答する（復習）"):
            if choice == quiz["answer"]:
                st.success("正解！")
            else:
                st.error(f"不正解。正解は「{quiz['answer']}」")

# ==============================
# 間違えた問題一覧
# ==============================
elif mode == "間違えた問題一覧":
    wrong = [h for h in st.session_state.history if not h["correct"]]

    if not wrong:
        st.info("間違えた問題はありません")
    else:
        for h in wrong:
            st.markdown(f"- **{h['question']}**（正解：{h['correct_answer']}）")
