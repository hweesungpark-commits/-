import streamlit as st

# --- [1. 설정 및 단위 변환 로직] ---
st.set_page_config(page_title="바람의나라 분노 계산기", layout="centered")

def format_korean_unit(number):
    num = int(number)
    if num < 10000: return f"{num}"
    eok = num // 100000000
    man = (num % 100000000) // 10000
    rem = num % 10000
    
    result = ""
    if eok > 0: result += f"{eok}억 "
    if man > 0: result += f"{man}만 "
    if rem > 0 or result == "": result += f"{rem}"
    return result.strip()

# --- [2. 웹 UI 구성] ---
st.title("🏹 바람의나라 분노 대미지 시뮬레이터")
st.markdown("---")

# 입력 항목 레이아웃 (2열 구성)
col1, col2 = st.columns(2)

with col1:
    hp = st.number_input("1. 현재 체력(HP)", min_value=0, value=1000000, step=10000)
    my_ignore = st.number_input("3. 내 직타저항무시 (%)", min_value=0.0, value=0.0, step=0.1) / 100
    my_crit_rate = st.number_input("5. 내 마치피해량증가 (%)", min_value=0.0, value=0.0, step=0.1) / 100
    opp_def = st.number_input("7. 상대 대인방어 (%)", min_value=0.0, value=0.0, step=0.1) / 100

with col2:
    mp = st.number_input("2. 현재 마력(MP)", min_value=0, value=1000000, step=10000)
    my_atk = st.number_input("4. 내 대인공격 (%)", min_value=0.0, value=0.0, step=0.1) / 100
    opp_res = st.number_input("6. 상대 직타저항 (%)", min_value=0.0, value=0.0, step=0.1) / 100
    is_phoenix = st.checkbox("8. 불멸주작 보유 여부", value=False)

st.markdown("---")

# --- [3. 계산 로직] ---
# 기본 위력 및 상수
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
readable_dmg = format_korean_unit(final_damage)

st.subheader("🔥 최종 계산 대미지")
st.error(f"### {readable_dmg}") # 강조를 위해 빨간색 박스 형태로 출력

st.info(f"""
**계산 상세 정보:**
- 기본 위력 계수: {base_power:,.2f}
- 직타/대인 효율: {res_factor * attack_factor * defense_factor:,.4f}
- 마치피해 증폭(A): {crit_factor_a:,.4f}
- 불멸주작 증폭(B): {1 + (0.6 * crit_factor_a) if is_phoenix else 1.0:,.4f}
""")