import streamlit as st

# --- [1. 설정 및 단위 변환 로직] ---
st.set_page_config(page_title="바람의나라 분노 계산기", layout="centered")

# [폰트 크기 및 제목 한 줄 고정 스타일 적용]
st.markdown("""
    <style>
    .main-title {
        font-size: clamp(1.2rem, 5vw, 2rem); /* 화면 너비에 따라 폰트 크기 자동 조절 */
        font-weight: bold;
        text-align: center;
        white-space: nowrap; /* 줄바꿈 방지 */
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 20px;
        color: #31333F;
    }
    /* 체크박스 위치 정밀 조정 */
    .checkbox-container {
        padding-top: 36px;
    }
    </style>
    """, unsafe_allow_html=True)

def format_korean_unit_refined(number):
    """숫자를 '억 만 천' 단위로 변환하고 백의 자리 이하는 절삭"""
    num = int(number)
    if num < 1000:
        return "0 (1,000 미만)"
    
    eok = num // 100000000
    man = (num % 100000000) // 10000
    cheon = (num % 10000) // 1000 
    
    result = []
    if eok > 0: result.append(f"{eok}억")
    if man > 0: result.append(f"{man}만")
    if cheon > 0: result.append(f"{cheon}천")
        
    return " ".join(result) if result else "0"

# --- [2. 웹 UI 구성] ---
# 제목 부분에 위에서 정의한 스타일 클래스 적용
st.markdown('<p class="main-title">🏹 바람의나라 분노 대미지 시뮬레이터</p>', unsafe_allow_html=True)
st.markdown("---")

# 상단 레이아웃 (나의 스펙 vs 상대방 스펙)
col_my, col_opp = st.columns(2, gap="large")

with col_my:
    st.subheader("👤 나의 스펙")
    hp = st.number_input("나의 최대 체력(HP)", min_value=0, value=1000000, step=10000, key="hp_input")
    mp = st.number_input("나의 최대 마력(MP)", min_value=0, value=1000000, step=10000, key="mp_input")
    my_ignore = st.number_input("나의 직타저항무시 (%)", min_value=0.0, value=0.0, step=0.1, key="ignore_input") / 100
    my_atk = st.number_input("나의 대인공격 (%)", min_value=0.0, value=0.0, step=0.1, key="atk_input") / 100
    
    # 마치피해 & 불멸주작 나란히 배치 (비율 최적화)
    m_col1, m_col2 = st.columns([1.8, 1.2]) 
    with m_col1:
        my_crit_rate = st.number_input("나의 마치피해량증가 (%)", min_value=0.0, value=0.0, step=0.1, key="crit_input") / 100
    with m_col2:
        # 스타일 시트를 이용한 정밀한 높이 맞춤
        st.markdown('<div class="checkbox-container"></div>', unsafe_allow_html=True)
        is_phoenix = st.checkbox("불멸주작 시동", value=False, key="phoenix_check")

with col_opp:
    st.subheader("🎯 상대방 스펙")
    opp_res = st.number_input("상대방 직타저항 (%)", min_value=0.0, value=0.0, step=0.1, key="res_input") / 100
    opp_def = st.number_input("상대방 대인방어 (%)", min_value=0.0, value=0.0, step=0.1, key="def_input") / 100

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

with st.expander("계산 상세 정보 확인"):
    st.write(f"- **기본 위력 계수**: {base_power:,.2f}")
    st.write(f"- **직타/대인 효율**: {res_factor * attack_factor * defense_factor:,.4f}")
    st.write(f"- **마치피해 증폭(A)**: {crit_factor_a:,.4f}")
    if is_phoenix:
        st.write(f"- **불멸주작 증폭(B)**: {1 + (0.6 * crit_factor_a):,.4f}")
    st.info("※ 백 단위 이하는 계산기 정책에 따라 절삭 표기됩니다.")
