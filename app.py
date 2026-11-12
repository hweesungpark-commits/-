import streamlit as st

# --- [1. 설정 및 스타일 세팅] ---
st.set_page_config(page_title="바람의나라 분노 계산기", layout="centered")

# 실시간 반응형 UI 및 디자인 커스텀
st.markdown("""
    <style>
    /* 제목 폰트 크기 자동 조절 및 줄바꿈 방지 */
    .main-title {
        font-size: clamp(1.1rem, 4.5vw, 1.8rem); 
        font-weight: bold;
        text-align: center;
        white-space: nowrap; 
        color: #31333F;
        margin-bottom: 20px;
    }
    /* "Press Enter to apply" 안내 문구 강제 삭제 */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    /* 입력창 간격 및 여백 최적화 */
    .stNumberInput {
        margin-bottom: -10px;
    }
    .checkbox-container {
        padding-top: 36px;
    }
    /* 라벨 강조 */
    label {
        font-size: 14px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

def format_korean_unit_refined(number):
    """숫자를 '억 만 천' 단위로 변환하고 백 단위 이하는 절삭"""
    num = int(number)
    if num < 1000: return "0"
    eok = num // 100000000
    man = (num % 100000000) // 10000
    cheon = (num % 10000) // 1000 
    result = []
    if eok > 0: result.append(f"{eok}억")
    if man > 0: result.append(f"{man}만")
    if cheon > 0: result.append(f"{cheon}천")
    return " ".join(result) if result else "0"

# --- [2. 웹 UI 구성 및 디폴트 스펙 설정] ---
st.markdown('<p class="main-title">🏹 바람의나라 분노 대미지 시뮬레이터</p>', unsafe_allow_html=True)
st.markdown("---")

col_my, col_opp = st.columns(2, gap="large")

with col_my:
    st.subheader("👤 나의 스펙")
    hp = st.number_input("나의 최대 체력(HP)", min_value=0, value=10000000, step=100000, key="hp_v")
    mp = st.number_input("나의 최대 마력(MP)", min_value=0, value=10000000, step=100000, key="mp_v")
    my_ignore = st.number_input("나의 직타저항무시 (%)", min_value=0.0, value=0.0, step=0.1, key="ign_v") / 100
    my_atk = st.number_input("나의 대인공격 (%)", min_value=0.0, value=40.0, step=0.1, key="atk_v") / 100

with col_opp:
    st.subheader("🎯 상대방 스펙")
    opp_res = st.number_input("상대방 직타저항 (%)", min_value=0.0, value=70.0, step=0.1, key="res_v") / 100
    opp_def = st.number_input("상대방 대인방어 (%)", min_value=0.0, value=40.0, step=0.1, key="dfn_v") / 100
    
    # 공유 링크 버튼 섹션
    st.write("---")
    st.write("🔗 **링크 공유하기**")
    share_url = "https://8fxmjdf792zw36g25tutgf.streamlit.app/" 
    if st.button("계산기 주소 복사하기"):
        st.success("아래 주소를 복사해서 공유하세요!")
        st.code(share_url, language=None)

st.markdown("---") 

# --- [3. 계산 로직] ---
# 기본 분노 위력 공식
base_power = (hp + (mp * 2)) / 3.267974
res_factor = 1 - opp_res + my_ignore
attack_factor = 1 + my_atk
defense_factor = 1 - opp_def

# 최종 대미지 계산 (인게임 비교 결과에 맞춰 최종 나누기 2 반영)
final_damage = (base_power * res_factor * attack_factor * defense_factor) / 2

# --- [4. 결과 출력 섹션] ---
st.subheader("🔥 최종 계산 대미지")
t_final = format_korean_unit_refined(final_damage)
st.error(f"### {t_final}") 

# 푸터 정보
st.caption("제작자: 빅딕@연  |  최종수정날짜: 2026.03.27")

# 상세 데이터 확인용 익스팬더
with st.expander("계산 상세 정보 확인"):
    st.write(f"- **기본 위력 계수**: {base_power:,.2f}")
    st.write(f"- **직타/대인 효율**: {res_factor * attack_factor * defense_factor:,.4f}")
    st.info("※ 백 단위 이하는 계산기 정책에 따라 절삭 표기됩니다.")
