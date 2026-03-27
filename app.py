import streamlit as st
import re

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
    /* 입력창 라벨 폰트 */
    label { font-size: 14px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 실시간 텍스트를 숫자로 안전하게 변환하는 함수
def get_num(val):
    try:
        # 숫자와 소수점만 남기고 제거
        clean = re.sub(r'[^0-9.]', '', str(val))
        return float(clean) if clean else 0.0
    except:
        return 0.0

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

# --- [2. 웹 UI 구성] ---
st.markdown('<p class="main-title">🏹 바람의나라 분노 대미지 시뮬레이터</p>', unsafe_allow_html=True)
st.markdown("---")

col_my, col_opp = st.columns(2, gap="large")

with col_my:
    st.subheader("👤 나의 스펙")
    # key를 부여하고 text_input을 사용하면 엔터 없이도 값이 즉시 세션에 기록됩니다.
    hp_raw = st.text_input("나의 최대 체력(HP)", value="1000000", key="hp_t")
    mp_raw = st.text_input("나의 최대 마력(MP)", value="1000000", key="mp_t")
    ign_raw = st.text_input("나의 직타저항무시 (%)", value="0.0", key="ign_t")
    atk_raw = st.text_input("나의 대인공격 (%)", value="0.0", key="atk_t")
    
    m_col1, m_col2 = st.columns([1.8, 1.2]) 
    with m_col1:
        crit_raw = st.text_input("나의 마치피해량증가 (%)", value="0.0", key="crit_t")
    with m_col2:
        st.markdown('<div class="checkbox-container"></div>', unsafe_allow_html=True)
        is_phoenix = st.checkbox("불멸주작 시동", value=False, key="phx")

with col_opp:
    st.subheader("🎯 상대방 스펙")
    res_raw = st.text_input("상대방 직타저항 (%)", value="0.0", key="res_t")
    dfn_raw = st.text_input("상대방 대인방어 (%)", value="0.0", key="dfn_t")

# 실시간 텍스트 -> 숫자 변환
hp = get_num(hp_raw)
mp = get_num(mp_raw)
my_ignore = get_num(ign_raw) / 100
my_atk = get_num(atk_raw) / 100
my_crit_rate = get_num(crit_raw) / 100
opp_res = get_num(res_raw) / 100
opp_def = get_num(dfn_raw) / 100

st.markdown("---") 

# --- [3. 계산 로직] ---
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
st.error(f"### {readable_dmg}") 

st.caption("제작자: 빅딕@연  |  최종수정날짜: 2026.03.27")
