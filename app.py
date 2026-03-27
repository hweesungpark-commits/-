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
    .checkbox-container {
        padding-top: 36px;
    }
    /* 입력창 아래 여백 줄여서 더 촘촘하게 */
    .stNumberInput {
        margin-bottom: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

def format_korean_unit_refined(number):
    num = int(number)
    if num < 1000: return "0 (1,000 미만)"
    eok = num // 100000000
    man = (num % 100000000) // 10000
    cheon = (num % 10000) // 1000 
    result = []
    if eok > 0: result.append(f"{eok}억")
    if man > 0: result.append(f"{man}만")
    if cheon > 0: result.append(f"{cheon}천")
    return " ".join(result) if result else "0"

# --- [2. 웹 UI 구성] ---
st.markdown('<p class="main-title">🏹 바람의나라 분노 대미지 시뮬레이터</p>', unsafe_allow_html=True)
st.markdown("---")

col_my, col_opp = st.columns(2, gap="large")

with col_my:
    st.subheader("👤 나의 스펙")
    # value가 변경되는 즉시 스크립트가 상단부터 하단까지 재실행됩니다.
    hp = st.number_input("나의 최대 체력(HP)", min_value=0, value=1000000, step=10000)
    mp = st.number_input("나의 최대 마력(MP)", min_value=0, value=1000000, step=10000)
    my_ignore = st.number_input("나의 직타저항무시 (%)", min_value=0.0, value=0.0, step=0.1) / 100
    my_atk = st.number_input("나의 대인공격 (%)", min_value=0.0, value=0.0, step=0.1) / 100
    
    m_col1, m_col2 = st.columns([1.7, 1.3]) 
    with m_col1:
        my_crit_rate = st.number_input("나의 마치피해량증가 (%)", min_value=0.0, value=0.0, step=0.1) / 100
    with m_col2:
        st.markdown('<div class="checkbox-container"></div>', unsafe_allow_html=True)
        # 체크박스는 클릭하는 순간 즉시 대미지가 업데이트됩니다.
        is_phoenix = st.checkbox("불멸주작 시동", value=False)

with col_opp:
    st.subheader("🎯 상대방 스펙")
    opp_res = st.number_input("상대방 직타저항 (%)", min_value=0.0, value=0.0, step=0.1) / 100
    opp_def = st.number_input("상대방 대인방어 (%)", min_value=0.0, value=0.0, step=0.1) / 100

st.markdown("---") 

# --- [3. 계산 로직] (입력값이 바뀔 때마다 여기가 실시간으로 재계산됨) ---
base_power = (hp + (mp * 2)) / 3.267974
res_factor = 1 - opp_res + my_ignore
attack_factor = 1 + my_atk
defense_factor = 1 - opp_def
crit_factor_a = 1 + (my_crit_rate / 2)
final_damage = base_power * res_factor * attack_factor * defense_factor * crit_factor_a

if is_phoenix:
    crit_factor_b = 1 + (0.6 * crit_factor_a)
    final_damage *= crit_factor_b

# --- [4. 결과 출력] ---
readable_dmg = format_korean_unit_refined(final_damage)

st.subheader("🔥 최종 계산 대미지")
# 실시간으로 변하는 숫자가 더 돋보이도록 크게 출력
st.error(f"### {readable_dmg}") 

st.caption("제작자: 빅딕@연  |  최종수정날짜: 2026.03.27")

with st.expander("계산 상세 정보 확인"):
    st.write(f"- **기본 위력 계수**: {base_power:,.2f}")
    st.write(f"- **직타/대인 효율**: {res_factor * attack_factor * defense_factor:,.4f}")
    st.write(f"- **마치피해 증폭(A)**: {crit_factor_a:,.4f}")
    if is_phoenix:
        st.write(f"- **불멸주작 증폭(B)**: {1 + (0.6 * crit_factor_a):,.4f}")
