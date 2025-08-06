import streamlit as st
import json
import os

# 데이터 파일
DATA_FILE = "user_data.json"

# 경험치 → 레벨 변환 함수
def get_level(exp):
    return exp // 100

# 데이터 로드
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# 데이터 저장
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# 랭킹 계산
def get_rankings(data):
    rankings = []
    for username, user_data in data.items():
        rankings.append((username, get_level(user_data['exp'])))
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings

# Streamlit 인터페이스
st.title("🔥 미션 랭킹 시스템")

# 사용자 입력
username = st.text_input("닉네임을 입력하세요", max_chars=20)

if username:
    data = load_data()
    
    # 사용자 최초 접속 처리
    if username not in data:
        data[username] = {"exp": 0}
        save_data(data)

    st.success(f"환영합니다, {username}님!")

    # 미션 수행 버튼
    if st.button("✅ 미션 수행"):
        data[username]["exp"] += 30  # 미션당 경험치 +30
        save_data(data)
        st.success("경험치를 획득했습니다! 🔥")

    # 현재 경험치 및 레벨
    user_exp = data[username]["exp"]
    user_level = get_level(user_exp)
    st.write(f"🧪 현재 경험치: {user_exp}")
    st.write(f"🏅 현재 레벨: {user_level}")

    # 랭킹 보여주기
    st.subheader("🏆 랭킹")
    rankings = get_rankings(data)
    for rank, (user, level) in enumerate(rankings, start=1):
        st.write(f"{rank}위: {user} - Lv.{level}")
