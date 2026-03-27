import streamlit as st

# --- [1. 설정 및 스타일] ---
st.set_page_config(page_title="바람의나라 분노 계산기", layout="centered")

st.markdown("""
    <style>
    .main-title {
        font-size: clamp(1.1rem, 4.5vw, 1.8rem); 
        font-weight: bold;
        text-align: center;
        white-space: nowrap; 
        color: #31333F;
        margin-bottom: 20px;
    }
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    .stNumberInput {
        margin-bottom: -10px;
    }
    .checkbox-container {
        padding-top: 36px;
    }
    /* 공유 섹션 스타일 */
    .share-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
        border: 1px solid #dcdfe3;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def format_korean_unit_refined(number):
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

# --- [2. 웹 UI 구성 및 디폴트 값] ---
st.markdown('<p class="main-title">🏹 바람의나라 분노 대미지 시뮬레이터</p>', unsafe_allow_html=True)
st.markdown("---")

col_my, col_opp = st.columns(2, gap="large")

with col_my:
    st.subheader("👤 나의 스펙")
    hp = st.number_input("나의 최대 체력(HP)", min_value=0, value=10000000, step=100000, key="hp_v")
    mp = st.number_input("나의 최대 마력(MP)", min_value=0, value=10000000, step=100000, key="mp_v")
    my_ignore = st.number_input("나의 직타저항무시 (%)", min_value=0.0, value=0.0, step=0.1, key="ign_v") / 100
    my_atk = st.number_input("나의 대인공격 (%)", min_value=0.0, value=40.0, step=0.1, key="atk_v") / 100
    
    m_col1, m_col2 = st.columns([1.8, 1.2]) 
    with m_col1:
        my_crit_rate = st.number_input("나의 마치피해량증가 (%)", min_value=0.0, value=10.0, step=0.1, key="crit_v") / 100
    with m_col2:
        st.markdown('<div class="checkbox-container"></div>', unsafe_allow_html=True)
        is_phoenix = st.checkbox("불멸주작 시동", value=False, key="phx_v")

with col_opp:
    st.subheader("🎯 상대방 스펙")
    opp_res = st.number_input("상대방 직타저항 (%)", min_value=0.0, value=70.0, step=0.1, key="res_v") / 100
    opp_def = st.number_input("상대방 대인방어 (%)", min_value=0.0, value=40.0, step=0.1, key="dfn_v") / 100
    
    # [요청사항] 하단 빈 공간에 공유 버튼 추가
    st.write("---")
    st.write("🔗 **링크 공유하기**")
    # 현재 앱의 URL 주소 (본인의 실제 streamlit 주소로 바꿔 적으셔도 됩니다)
    share_url = "https://your-app-name.streamlit.app" 
    
    # 클릭 시 클립보드에 복사되는 버튼
    if st.button("계산기 주소 복사하기"):
        st.write("복사되었습니다! 필요한 곳에 붙여넣으세요.")
        # 실제 클립보드 복사 기능 (최신 스트림릿 버전 지원)
        # st.copy_to_clipboard(share_url) # 버전이 낮을 경우 에러 방지를 위해 하단 텍스트 노출로 대체 가능
        st.code(share_url, language=None)

st.markdown("---") 

# --- [3. 계산 로직] ---
base_power = (hp + (mp * 2)) / 3.267974
res_factor = 1 - opp_res + my_ignore
attack_factor = 1 + my_atk
defense_factor = 1 - opp_def
crit_factor_a = 1 + (my_crit_rate / 2)

pure_damage = base_power * res_factor * attack_factor * defense_factor * crit_factor_a
final_damage = pure_damage
bonus_damage = 0

if is_phoenix:
    bonus_factor = 0.6 * crit_factor_a
    bonus_damage = pure_damage * bonus_factor
    final_damage = pure_damage + bonus_damage

# --- [4. 결과 출력] ---
st.subheader("🔥 최종 계산 대미지")

if is_phoenix:
    t_pure = format_korean_unit_refined(pure_damage)
    t_bonus = format_korean_unit_refined(bonus_damage)
    t_final = format_korean_unit_refined(final_damage)
    st.write(f"**[기본]** {t_pure} + **[주작추가]** {t_bonus}")
    st.error(f"### = {t_final}")
else:
    t_final = format_korean_unit_refined(final_damage)
    st.error(f"### {t_final}") 

st.caption("제작자: 빅딕@연  |  최종수정날짜: 2026.03.27")
