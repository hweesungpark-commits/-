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
    /* "Press Enter to apply" 안내 문구를 완전히 박멸하는 CSS */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    /* 입력창 간격 조정 */
    .stNumberInput {
        margin-bottom: -10px;
    }
    .checkbox-container {
        padding-top: 36px;
    }
    </style>
    """, unsafe_allow_html=True)

def format_korean_unit_refined(number):
    """숫자를 '억 만 천' 단위로 변환하고 백의 자리 이하는 절삭"""
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

# --- [2. 웹 UI 구성 및 기본값(Default) 설정] ---
st.markdown('<p class="main-title">🏹 바람의나라 분노 대미지 시뮬레이터</p>', unsafe_allow_html=True)
st.markdown("---")

col_my, col_opp = st.columns(2, gap="large")

with col_my:
    st.subheader("👤 나의 스펙")
    # 요청하신 기본값 적용: 체력 1천만, 마력 1천만, 직타무시 0, 대인공격 40, 마치피해 10
    hp = st.number_input("나의 최대 체력(HP)", min_value=0, value=10000000, step=100000, key="hp_v")
    mp = st.number_input("나의 최대 마력(MP)", min_value=0, value=10000000, step=100000, key="mp_v")
    my_ignore = st.number_input("나의 직타저항무시 (%)", min_value=0.0, value=0.0, step=0.1, key="ign_v") / 100
    my_atk = st.number_input("나의 대인공격 (%)", min_value=0.0, value=40.0, step=0.1, key="atk_v") / 100
    
    m_col1, m_col2 = st.columns([1.8, 1.2]) 
    with m_col1:
        my_crit_rate = st.number_input("나의 마치피해량증가 (%)", min_value=0.0, value=10.0, step=0.1, key="crit_v") / 100
    with m_col2:
        st.markdown('<div class="checkbox-container"></div>', unsafe_allow_html=True)
        # 기본값: 체크 해제
        is_phoenix = st.checkbox("불멸주작 시동", value=False, key="phx_v")

with col_opp:
    st.subheader("🎯 상대방 스펙")
    # 요청하신 기본값 적용: 상대 직타 70, 상대 대방 40
    opp_res = st.number_input("상대방 직타저항 (%)", min_value=0.0, value=70.0, step=0.1, key="res_v") / 100
    opp_def = st.number_input("상대방 대인방어 (%)", min_value=0.0, value=40.0, step=0.1, key="dfn_v") / 100

st.markdown("---") 

# --- [3. 계산 로직] ---
base_power = (hp + (mp * 2)) / 3.267974
res_factor = 1 - opp_res + my_ignore
attack_factor = 1 + my_atk
defense_factor = 1 - opp_def
crit_factor_a = 1 + (my_crit_rate / 2)
final_damage = base_power * res_factor * attack_factor * defense_factor * crit_factor_a

if is_phoenix:
    # 불멸주작 시동 시 증폭 계산
    final_damage *= (1 + (0.6 * crit_factor_a))

# --- [4. 결과 출력] ---
readable_dmg = format_korean_unit_refined(final_damage)
st.subheader("🔥 최종 계산 대미지")
st.error(f"### {readable_dmg}") 

st.caption("제작자: 빅딕@연  |  최종수정날짜: 2026.03.27")

with st.expander("계산 상세 정보 확인"):
    st.write(f"- 기본 위력 계수: {base_power:,.2f}")
    st.write(f"- 직타/대인 효율: {res_factor * attack_factor * defense_factor:,.4f}")
    st.write(f"- 마치피해 증폭(A): {crit_factor_a:,.4f}")
    if is_phoenix:
        st.write(f"- 불멸주작 증폭(B): {1 + (0.6 * crit_factor_a):,.4f}")
    st.info("※ 백 단위 이하는 계산기 정책에 따라 절삭 표기됩니다.")
