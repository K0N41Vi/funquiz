import streamlit as st
import random

# =====================
# 雑学クイズデータ
# =====================
quiz = [
    {
        "id": 1,
        "question": "日本で一番面積が大きい都道府県は【　】である。",
        "answer": "北海道",
        "hints": [
            "都・府・県のいずれにも分類されない",
            "面積が2位の都道府県の約4倍ある",
            "新幹線で本州とつながっている"
        ]
    },
    {
        "id": 2,
        "question": "光の速さは約【　】km/秒である。",
        "answer": "300000",
        "hints": [
            "地球を1秒で7周以上できる速さ",
            "音速の約100万倍",
            "物理定数として扱われる"
        ]
    },
    {
        "id": 3,
        "question": "タコの心臓は【　】個ある。",
        "answer": "3",
        "hints": [
            "魚類より多い",
            "血液の循環方式が特殊",
            "1つは全身用ではない"
        ]
    },
    {
        "id": 4,
        "question": "雷が光ってから音が聞こえるのは【　】が遅いためである。",
        "answer": "音",
        "hints": [
            "真空中では伝わらない",
            "光と同時に発生している",
            "空気の振動として伝わる"
        ]
    }
]

# =====================
# 初期化
# =====================
if "current" not in st.session_state:
    st.session_state.current = random.choice(quiz)
    st.session_state.hint_level = 0
    st.session_state.history = []
    st.session_state.wrong_questions = []
    st.session_state.mode = "通常"
    st.session_state.answered = False
    st.session_state.result_message = ""

# =====================
# UI
# =====================
st.title("🧠 雑学クイズ")
st.caption("日常会話のネタになる雑学を、思考型クイズで覚える")

st.session_state.mode = st.radio(
    "モード選択",
    ["通常", "復習", "間違えた問題一覧"]
)

# =====================
# クイズ画面
# =====================
if st.session_state.mode in ["通常", "復習"]:

    q = st.session_state.current

    st.subheader("問題")
    st.write(q["question"])

    user_answer = st.text_input("答えを入力してください")

    col1, col2 = st.columns(2)

    # ヒントボタン
    with col1:
        if st.button("ヒントを見る"):
            if st.session_state.hint_level < len(q["hints"]):
                st.warning(
                    f"思考ヒント {st.session_state.hint_level + 1}："
                    f"{q['hints'][st.session_state.hint_level]}"
                )
                st.session_state.hint_level += 1
            else:
                st.info("これ以上ヒントはありません")

    # 回答ボタン
    with col2:
        if st.button("回答する"):
            correct = user_answer.strip() == q["answer"]

            # 履歴保存
            st.session_state.history.append({
                "question": q["question"],
                "your_answer": user_answer,
                "correct_answer": q["answer"],
                "result": correct
            })

            if correct:
                st.session_state.result_message = "⭕ 正解！"
            else:
                st.session_state.result_message = f"❌ 不正解。正解は「{q['answer']}」"

                # 間違えた問題を保存（重複防止）
                if q not in st.session_state.wrong_questions:
                    st.session_state.wrong_questions.append(q)

            st.session_state.answered = True

    # 結果表示
    if st.session_state.answered:
        if "⭕" in st.session_state.result_message:
            st.success(st.session_state.result_message)
        else:
            st.error(st.session_state.result_message)

        if st.button("次の問題へ"):
            if st.session_state.mode == "通常":
                st.session_state.current = random.choice(quiz)
            else:
                if st.session_state.wrong_questions:
                    st.session_state.current = random.choice(
                        st.session_state.wrong_questions
                    )

            st.session_state.hint_level = 0
            st.session_state.answered = False
            st.session_state.result_message = ""

# =====================
# 間違えた問題一覧
# =====================
if st.session_state.mode == "間違えた問題一覧":

    st.subheader("間違えた問題一覧")

    if not st.session_state.wrong_questions:
        st.write("間違えた問題はありません 🎉")
    else:
        for i, w in enumerate(st.session_state.wrong_questions, 1):
            st.write(f"{i}. {w['question']}")
            st.caption(f"正解：{w['answer']}")

# =====================
# 解答履歴
# =====================
with st.expander("📜 解答履歴を見る"):
    if not st.session_state.history:
        st.write("まだ解答履歴はありません")
    else:
        for h in st.session_state.history:
            mark = "⭕" if h["result"] else "❌"
            st.write(
                f"{mark} {h['question']} / "
                f"あなたの答え：{h['your_answer']}"
            )
