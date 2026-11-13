import streamlit as st
import base64


SUBJECT_WEIGHTS = {
    "국어": {"mid": 0.30, "final": 0.30, "perf": 0.40},
    "영어": {"mid": 0.25, "final": 0.25, "perf": 0.50},
    "수학": {"mid": 0.30, "final": 0.30, "perf": 0.40},
    "과학": {"mid": 0.30, "final": 0.30, "perf": 0.40},
    "역사": {"mid": 0.30, "final": 0.30, "perf": 0.40},
    "도덕": {"mid": 0.30, "final": 0.30, "perf": 0.40},
    "한문": {"mid": 0.30, "final": 0.30, "perf": 0.40},
}


TEXTS = {
    "page_title": "치이카와 성적 계산기(베타)",
    "main_title": "한강민이 만든 성취도 계산기(베타)",
    "sub_title": "과목을 선택하고 점수를 입력하시오. (2개 이상 입력 시 목표 점수 계산)",
    "select_subject": "1. 과목 선택",
    "weight_info": "반영 비율: 중간 {mid}% / 기말 {final}% / 수행 {perf}%",
    "weight_warning": "관리자가 아직 이 과목의 반영 비율을 설정하지 않았습니다.",
    "input_guide": "2. 점수 입력 (100점 만점 기준, 미응시/미정 과목은 체크 해제)",
    "mid_label": "중간고사",
    "final_label": "기말고사",
    "perf_label": "수행평가",
    "calc_button": "결과 확인",
    "err_less_than_2": "최소 2개 이상의 점수를 입력해야 계산할 수 있습니다.",
    "err_weight_zero": "계산하려는 항목의 반영 비율이 0%로 설정되어 있습니다.",
    "res_all_title": "예상 최종 성적 결과",
    "res_all_score": "환산 총점: **{total:.2f}점** (반올림: {rounded}점)",
    "res_all_grade": "예상 성취도: **{grade} 등급**",
    "res_target_title": "[{target_name}] 목표 성취도별 필요 점수",
    "grade_achievable": "- **성취도 {grade}** ({cut}점 이상): **{req_score:.1f}점** 이상 필요",
    "grade_already": "- **성취도 {grade}** ({cut}점 이상): **달성 확정** (0점 받아도 가능)",
    "grade_impossible": "- **성취도 {grade}** ({cut}점 이상): **달성 불가** (100점 만점 받아도 {max_possible:.1f}점)",
    "feedback_text": "오류 제보 및 개선 의견 보내기 (구글폼)",
    "feedback_url": "https://forms.gle/mHbY6hAJNQpotsDS8",

}


GRADE_CUTOFFS = [
    ("A", 89.5),
    ("B", 79.5),
    ("C", 69.5),
    ("D", 59.5),
    ("E", 0.0),
]

 
def get_grade(score):
    for grade, cutoff in GRADE_CUTOFFS:
        if score >= cutoff:
            return grade
    return "E"

def main():
    
    st.set_page_config(
        page_title=TEXTS["page_title"],
        page_icon="🇷🇺",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    
   
   
    def get_base64_img(image_file):
        try:
            with open(image_file, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except FileNotFoundError:
            return ""

    img_base64 = get_base64_img("bg.png")


    st.markdown(f"""
        <style>
        * {{
            border-radius: 0px !important;
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif !important;
        }}
       
        .stApp, [data-testid="stAppViewContainer"] {{
            background-color: #ffffff !important;
            background-image: linear-gradient(rgba(255, 255, 255, 0.72), rgba(255, 255, 255, 0.72)), url("data:image/png;base64,{img_base64}");
            background-size: contain;        
            background-position: right bottom; 
            background-repeat: no-repeat;
            background-attachment: fixed;   
        }}
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
       
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            border: 1.5px solid #000000 !important;
            padding: 2rem 1.5rem !important;
            margin-top: 2rem !important;
            margin-bottom: 2rem !important;
        }}
        
        @media (max-width: 768px) {{
            .stApp, [data-testid="stAppViewContainer"] {{
                background-size: 75% auto;      
                background-position: center bottom; 
            }}
            .block-container {{
                margin-top: 1rem !important;
                padding: 1.2rem 1rem !important;
            }}
        }}
       
        p, span, label, pre, code, h1, h2, h3 {{
            color: #000000 !important;
        }}
        div[data-baseweb="select"] > div {{
            border: 1.5px solid #000000 !important;
            background-color: #f8f8f8 !important;
            color: #000000 !important;
        }}
        div[data-baseweb="input"] {{
            border: 1.5px solid #000000 !important;
            background-color: #ffffff !important;
        }}
        input {{
            background-color: #ffffff !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}
        button[data-testid="stNumberInputStepDown"], button[data-testid="stNumberInputStepUp"] {{
            background-color: #e0e0e0 !important;
            color: #000000 !important;
            border-left: 1px solid #000000 !important;
            pointer-events: auto !important;
        }}
        .stButton > button {{
            width: 100%;
            height: 45px;
            background-color: #e0e0e0 !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }}
        .stButton > button:hover {{
            background-color: #cccccc !important;
        }}
        .plain-box {{
            border: 1.5px solid #000000 !important;
            padding: 15px;
            background-color: #f4f4f4 !important;
            color: #000000 !important;
            margin-top: 10px;
            line-height: 1.8;
            font-size: 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"## {TEXTS['main_title']}")
    st.text(TEXTS["sub_title"])
    st.markdown("---")

    
    subject = st.selectbox(TEXTS["select_subject"], list(SUBJECT_WEIGHTS.keys()))
    weights = SUBJECT_WEIGHTS[subject]
    w_mid, w_final, w_perf = weights["mid"], weights["final"], weights["perf"]

    if w_mid + w_final + w_perf == 0:
        st.text(TEXTS["weight_warning"])
    else:
        st.text(TEXTS["weight_info"].format(
            mid=int(round(w_mid * 100)),
            final=int(round(w_final * 100)),
            perf=int(round(w_perf * 100))
        ))

    st.markdown("---")
    st.markdown(f"**{TEXTS['input_guide']}**")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        use_mid = st.checkbox(TEXTS["mid_label"], value=True)
    with col2:
        mid_score = st.number_input("중간 점수", min_value=0.0, max_value=100.0, value=0.0, step=0.5, disabled=not use_mid, label_visibility="collapsed")

    col3, col4 = st.columns([1, 2])
    with col3:
        use_final = st.checkbox(TEXTS["final_label"], value=False)
    with col4:
        final_score = st.number_input("기말", min_value=0.0, max_value=100.0, value=0.0, step=0.5, disabled=not use_final, label_visibility="collapsed")

    col5, col6 = st.columns([1, 2])
    with col5:
        use_perf = st.checkbox(TEXTS["perf_label"], value=True)
    with col6:
        perf_score = st.number_input("수행", min_value=0.0, max_value=100.0, value=0.0, step=0.5, disabled=not use_perf, label_visibility="collapsed")

    st.write("")

    
    if st.button(TEXTS["calc_button"]):
        checked_count = sum([use_mid, use_final, use_perf])

        if checked_count < 2:
            st.markdown(f"<div class='plain-box'><b>{TEXTS['err_less_than_2']}</b></div>", unsafe_allow_html=True)
            return


        if checked_count == 3:
            total_score = (mid_score * w_mid) + (final_score * w_final) + (perf_score * w_perf)
            rounded_score = int(total_score + 0.5)
            grade = get_grade(total_score)

            result_html = f"""
            <div class='plain-box'>
                <b>{TEXTS['res_all_title']}</b><br>
                {TEXTS['res_all_score'].format(total=total_score, rounded=rounded_score)}<br>
                <b>{TEXTS['res_all_grade'].format(grade=grade)}</b>
            </div>
            """
            st.markdown(result_html, unsafe_allow_html=True)

       
        elif checked_count == 2:
            current_score = 0.0
            target_weight = 0.0
            target_name = ""

            if use_mid:
                current_score += mid_score * w_mid
            else:
                target_weight = w_mid
                target_name = TEXTS["mid_label"]

            if use_final:
                current_score += final_score * w_final
            else:
                target_weight = w_final
                target_name = TEXTS["final_label"]

            if use_perf:
                current_score += perf_score * w_perf
            else:
                target_weight = w_perf
                target_name = TEXTS["perf_label"]

            if target_weight <= 0:
                st.markdown(f"<div class='plain-box'><b>{TEXTS['err_weight_zero']}</b></div>", unsafe_allow_html=True)
                return

            max_possible = current_score + (100.0 * target_weight)
            lines = [f"<b>{TEXTS['res_target_title'].format(target_name=target_name)}</b>"]

            for grade, cutoff in GRADE_CUTOFFS:
                if grade == "E":
                    lines.append(TEXTS["grade_already"].format(grade=grade, cut=cutoff))
                    continue

                needed = (cutoff - current_score) / target_weight

                if needed <= 0:
                    lines.append(TEXTS["grade_already"].format(grade=grade, cut=cutoff))
                elif needed > 100.0:
                    lines.append(TEXTS["grade_impossible"].format(grade=grade, cut=cutoff, max_possible=max_possible))
                else:
                    lines.append(TEXTS["grade_achievable"].format(grade=grade, cut=cutoff, req_score=needed))

            result_html = "<div class='plain-box'>" + "<br>".join(lines) + "</div>"
            st.markdown(result_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 10px;">
            <a href="{TEXTS['feedback_url']}" target="_blank" style="color: #000000; text-decoration: underline; font-weight: bold; font-size: 14px;">
                {TEXTS['feedback_text']}
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
