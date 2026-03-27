import streamlit as st

# --- [1. 설정 및 단위 변환 로직] ---
st.set_page_config(page_title="바람의나라 분노 계산기", layout="centered")

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
st.title("🏹 바람의나라 분노 대미지 시뮬레이터")
st.markdown("---")

# 상단 레이아웃 (나의 스펙 vs 상대방 스펙)
col_my, col_opp = st.columns(2, gap="large")

with col_my:
    st.subheader("👤 나의 스펙")
    hp = st.number_input("나의 최대 체력(HP)", min_value=0, value=1000000, step=10000, key="hp_input")
    mp = st.number_input("나의 최대 마력(MP)", min_value=0, value=1000000, step=10000, key="mp_input")
    my_ignore = st.number_input("나의 직타저항무시 (%)", min_value=0.0, value=0.0, step=0.1, key="ignore_input") / 100
    my_atk = st.number_input("나의 대인공격 (%)", min_value=0.0, value=0.0, step=0.1, key="atk_input") / 100
    
    # [요청사항] 마치피해 칸 크기 조절 및 불멸주작 나란히 배치
    # 비율을 3:1 혹은 4:1 정도로 주어 입력칸의 가독성을 확보합니다.
    m_col1, m_col2 = st.columns([3, 1]) 
    with m_col1:
        my_crit_rate = st.number_input("나의 마치피해량증가 (%)", min_value=0.0, value=0.0, step=0.1, key="crit_input") / 100
    with m_col2:
        st.write("##") # 높이 맞춤용
        is_phoenix = st.checkbox("불멸주작", value=False, key="phoenix_check")

with col_opp:
    st.subheader("🎯 상대방 스펙")
    # [요청사항] 직타저항과 대인방어 순서 교체
    opp_res = st.number_input("상대방 직타저항 (%)", min_value=0.0, value=0.0, step=0.1, key="res_input") / 100
    opp_def = st.number_input("상대방 대인방어 (%)", min_value=0.0, value=0.0, step=0.1, key="def_input") / 100

st.markdown("---") 

# --- [3. 계산 로직] ---
base_power = (hp + (mp * 2)) / 3.267974
res_factor = 1 - opp_res + my_ignore
attack_factor = 1 + my_atk
defense_factor = 1 - opp_def

# 마치피해 계수 A / 불멸주작 계수 B
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
