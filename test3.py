import streamlit as st
import json
import os

def mission_ranking_app():
    DATA_FILE = "user_data.json"

    # 내부 함수: 경험치 → 레벨
    def get_level(exp):
        return exp // 100

    # 내부 함수: 데이터 로드
    def load_data():
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    # 내부 함수: 데이터 저장
    def save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

    # 내부 함수: 랭킹 계산
    def get_rankings(data):
        rankings = [(username, get_level(user_data["exp"])) for username, user_data in data.items()]
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings

    # 앱 시작
    st.title("🔥 미션 랭킹 시스템")

    username = st.text_input("닉네임을 입력하세요", max_chars=20)

    if username:
        data = load_data()

        # 유저가 처음 접속했을 경우 초기화
        if username not in data:
            data[username] = {"exp": 0}
            save_data(data)

        st.success(f"환영합니다, {username}님!")

        # 미션 수행 버튼
        if st.button("✅ 미션 수행"):
            data[username]["exp"] += 30
            save_data(data)
            st.success("경험치를 획득했습니다! 🔥")

        # 현재 유저 정보 출력
        user_exp = data[username]["exp"]
        user_level = get_level(user_exp)

        st.write(f"🧪 현재 경험치: {user_exp}")
        st.write(f"🏅 현재 레벨: {user_level}")

        # 전체 랭킹 표시
        st.subheader("🏆 랭킹")
        rankings = get_rankings(data)
        for rank, (user, level) in enumerate(rankings, start=1):
            st.write(f"{rank}위: {user} - Lv.{level}")

# 앱 실행
if __name__ == "__main__":
    mission_ranking_app()
