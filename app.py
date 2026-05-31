import streamlit as st
import requests
import json
import re

st.set_page_config(
    page_title="IELTS Writing Coach",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #fff8f4 !important;
    color: #5a2d0c !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #fff2eb !important;
    border-right: 1px solid #f5d0bb;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #c96a3a !important;
}
.stTextArea textarea {
    background-color: #fff !important;
    color: #5a2d0c !important;
    border: 1px solid #f5c4a0 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}
.stTextArea textarea:focus {
    border-color: #e8724a !important;
    box-shadow: 0 0 0 2px rgba(232,114,74,0.15) !important;
}
.stTextInput input {
    background-color: #fff !important;
    color: #5a2d0c !important;
    border: 1px solid #f5c4a0 !important;
    border-radius: 8px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #e8724a, #d4552e) !important;
    color: #fff !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 15px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(232,114,74,0.35) !important;
}
.stSelectbox > div > div {
    background-color: #fff !important;
    color: #5a2d0c !important;
    border-color: #f5c4a0 !important;
}
.stTabs [data-baseweb="tab-list"] {
    background-color: #fff2eb !important;
    border-radius: 20px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 16px !important;
    color: #c96a3a !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background-color: #e8724a !important;
    color: #fff !important;
}
[data-testid="stMarkdownContainer"] p { color: #5a2d0c; line-height: 1.7; }
hr { border-color: #f5d0bb !important; }

.header-hero {
    background: linear-gradient(135deg, #fff0e8 0%, #fff8f4 100%);
    border: 1px solid #f5d0bb;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.score-card {
    background: #fff;
    border: 1px solid #f5d0bb;
    border-radius: 12px;
    padding: 14px 10px;
    text-align: center;
    margin-bottom: 8px;
}
.score-card .label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; color: #e8956a; margin-bottom: 4px; }
.score-card .value { font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 600; }
.band-badge {
    display: inline-block;
    background: linear-gradient(135deg, #e8724a, #d4552e);
    color: #fff;
    font-family: 'Playfair Display', serif;
    font-size: 48px;
    font-weight: 600;
    padding: 10px 28px;
    border-radius: 14px;
    margin: 8px 0;
}
.section-box {
    background: #fff;
    border-left: 3px solid #e8724a;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 10px 0;
    color: #5a2d0c;
}
.section-box h4 {
    color: #c96a3a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px !important;
    font-weight: 500 !important;
}
.tip-box {
    background: #f0faf4;
    border: 1px solid #b8e0c8;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 14px;
    color: #2e6b4a;
}
.warn-box {
    background: #fff8ed;
    border: 1px solid #f5d7a0;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 14px;
    color: #8b5e10;
}
.word-chip {
    display: inline-block;
    background: #fff0e8;
    border: 1px solid #f5c4a0;
    color: #c96a3a;
    border-radius: 20px;
    padding: 3px 12px;
    margin: 3px;
    font-size: 13px;
}
.error-box {
    background: #fff5f5;
    border: 1px solid #f5c0c0;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
}
.vocab-box {
    background: #f5f8ff;
    border: 1px solid #c8d8f5;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)


GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def call_gemini(system_prompt: str, user_prompt: str, api_key: str) -> str:
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 2048}
    }
    resp = requests.post(GEMINI_URL, params={"key": api_key}, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

def parse_json_safe(text: str):
    try:
        text = re.sub(r"```json|```", "", text).strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return None

def band_color(score):
    if score >= 7.5: return "#2e6b4a"
    elif score >= 6.5: return "#e8724a"
    elif score >= 5.5: return "#d4a017"
    else: return "#c0392b"


SCORE_SYSTEM = """You are an expert IELTS examiner with 15+ years of experience.
Evaluate the essay strictly according to official IELTS band descriptors.
Return ONLY a valid JSON object — no markdown, no extra text:
{
  "overall_band": 6.5,
  "task_achievement": 6,
  "coherence_cohesion": 7,
  "lexical_resource": 6,
  "grammatical_range": 6,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
  "grammar_errors": [
    {"original": "wrong phrase", "correction": "correct phrase", "explanation": "why"}
  ],
  "vocabulary_suggestions": [
    {"basic": "common word", "advanced": "better word", "example": "example sentence"}
  ],
  "detailed_feedback": "2-3 paragraph detailed feedback"
}"""

SAMPLE_SYSTEM = """You are an expert IELTS writing tutor. Write a Band 8-9 model answer.
Return ONLY a valid JSON object:
{
  "sample_answer": "full essay text",
  "structure_breakdown": {
    "introduction": "explanation",
    "body_paragraphs": "explanation",
    "conclusion": "explanation"
  },
  "key_phrases": ["phrase 1", "phrase 2", "phrase 3", "phrase 4", "phrase 5"],
  "band_9_tips": ["tip 1", "tip 2", "tip 3", "tip 4"]
}"""

VOCAB_SYSTEM = """You are an IELTS vocabulary expert.
Return ONLY a valid JSON object:
{
  "topic_vocabulary": [
    {"word": "word", "definition": "meaning", "example": "sentence", "collocations": ["c1", "c2"]}
  ],
  "linking_words": {
    "addition": ["furthermore", "moreover"],
    "contrast": ["however", "nevertheless"],
    "cause_effect": ["consequently", "as a result"],
    "emphasis": ["notably", "in particular"]
  },
  "common_structures": [
    {"structure": "It is widely acknowledged that...", "use": "introducing a common belief"}
  ],
  "band_boosters": ["phrase 1", "phrase 2", "phrase 3", "phrase 4", "phrase 5"]
}"""


with st.sidebar:
    st.markdown("<h2 style='font-family:Playfair Display,serif;color:#c96a3a;margin-bottom:4px'>✍️ IELTS Coach</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#e8956a;font-size:13px;margin-bottom:16px'>Powered by Google Gemini</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#c96a3a;font-size:13px;font-weight:500;margin-bottom:4px'>🔑 Gemini API Key (Free)</p>", unsafe_allow_html=True)
    st.markdown("<small style='color:#e8956a'>Lấy tại <a href='https://aistudio.google.com/app/apikey' style='color:#e8724a'>aistudio.google.com</a></small>", unsafe_allow_html=True)
    api_key = st.text_input("", type="password", placeholder="AIza...", label_visibility="collapsed")
    if api_key:
        st.session_state["api_key"] = api_key
        st.success("API key set ✓")
    st.markdown("---")
    st.markdown("<p style='color:#c96a3a;font-size:13px;font-weight:500'>📚 Tính năng</p>", unsafe_allow_html=True)
    for feat in ["🎯 Chấm band score (4 tiêu chí)", "✏️ Phát hiện lỗi ngữ pháp", "💬 Gợi ý từ vựng nâng band", "📝 Sample answer Band 8-9", "🏗️ Phân tích cấu trúc bài", "🚀 Band-boosting phrases"]:
        st.markdown(f"<p style='color:#8b4a2a;font-size:13px;margin:4px 0'>{feat}</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='color:#c96a3a;font-size:13px;font-weight:500'>📊 Band Scale</p>", unsafe_allow_html=True)
    for label, bg, fg in [("Band 8-9","#d4edda","#2e6b4a"),("Band 6-7","#fff3cd","#856404"),("Band 4-5","#fde2d8","#a03020")]:
        st.markdown(f'<span style="background:{bg};color:{fg};border-radius:6px;padding:3px 12px;font-size:12px;font-weight:500">{label}</span>', unsafe_allow_html=True)


st.markdown("""
<div class="header-hero">
  <h1 style="margin:0;font-size:2rem;font-family:'Playfair Display',serif;color:#c96a3a">IELTS Writing Coach</h1>
  <p style="color:#e8956a;margin:6px 0 0;font-size:14px">Chấm bài • Sửa lỗi ngữ pháp • Gợi ý từ vựng • Band score dự đoán</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Chấm bài", "📖 Sample Answer", "📚 Vocab & Tips"])


with tab1:
    col1, col2 = st.columns(2)
    with col1:
        task_type = st.selectbox("Task Type", ["Task 2 (Essay)", "Task 1 (Academic)", "Task 1 (General)"])
    with col2:
        wct = "250+" if "Task 2" in task_type else "150+"
        st.markdown(f"<br><span style='color:#e8956a;font-size:13px'>📌 Tối thiểu: <b style='color:#e8724a'>{wct} words</b></span>", unsafe_allow_html=True)

    question = st.text_area("📌 Câu hỏi / Đề bài", height=90, placeholder="Dán đề IELTS vào đây...")
    essay = st.text_area("✍️ Bài viết của bạn", height=260, placeholder="Viết hoặc dán bài vào đây...")

    wc = len(essay.split()) if essay.strip() else 0
    if essay.strip():
        wc_color = "#2e6b4a" if wc >= (250 if "Task 2" in task_type else 150) else "#c0392b"
        st.markdown(f"<span style='color:{wc_color};font-size:13px'>Số từ: <b>{wc}</b></span>", unsafe_allow_html=True)

    if st.button("🎯 Chấm bài ngay", use_container_width=True):
        key = st.session_state.get("api_key", "")
        if not key:
            st.error("Vui lòng nhập Gemini API key ở sidebar.")
        elif not question.strip() or not essay.strip():
            st.warning("Hãy nhập đầy đủ đề bài và bài viết.")
        else:
            with st.spinner("Đang chấm bài..."):
                try:
                    prompt = f"Task: IELTS Writing {task_type}\nQuestion: {question}\nEssay:\n{essay}\nWord count: ~{wc}"
                    raw = call_gemini(SCORE_SYSTEM, prompt, key)
                    result = parse_json_safe(raw)
                except Exception as e:
                    st.error(f"Lỗi API: {e}")
                    result = None

            if result:
                st.markdown("---")
                overall = result.get("overall_band", 0)
                st.markdown(f'<div style="text-align:center;margin:14px 0"><div style="font-size:11px;text-transform:uppercase;letter-spacing:2px;color:#e8956a">Overall Band Score</div><div class="band-badge">{overall}</div></div>', unsafe_allow_html=True)

                cols = st.columns(4)
                for i, (label, kn) in enumerate([("Task Achievement","task_achievement"),("Coherence","coherence_cohesion"),("Lexical","lexical_resource"),("Grammar","grammatical_range")]):
                    score = result.get(kn, 0)
                    with cols[i]:
                        st.markdown(f'<div class="score-card"><div class="label">{label}</div><div class="value" style="color:{band_color(score)}">{score}</div></div>', unsafe_allow_html=True)

                ft1, ft2, ft3, ft4 = st.tabs(["💬 Nhận xét", "✏️ Lỗi ngữ pháp", "📈 Từ vựng", "✅ Điểm mạnh/yếu"])
                with ft1:
                    st.markdown(f'<div class="section-box"><h4>Detailed Feedback</h4>{result.get("detailed_feedback","")}</div>', unsafe_allow_html=True)
                with ft2:
                    errors = result.get("grammar_errors", [])
                    if errors:
                        for e in errors:
                            st.markdown(f'''<div class="error-box">
                              <div style="color:#c0392b;text-decoration:line-through;margin-bottom:4px">"{e.get('original','')}"</div>
                              <div style="color:#2e6b4a;margin-bottom:4px">✓ "{e.get('correction','')}"</div>
                              <div style="color:#8b6a5a;font-size:13px">{e.get('explanation','')}</div>
                            </div>''', unsafe_allow_html=True)
                    else:
                        st.success("Không có lỗi ngữ pháp nghiêm trọng!")
                with ft3:
                    for v in result.get("vocabulary_suggestions", []):
                        st.markdown(f'''<div class="vocab-box">
                          <span style="color:#8b6a8a;text-decoration:line-through">{v.get('basic','')}</span>
                          <span style="color:#aaa"> → </span>
                          <span style="color:#6a5acd;font-weight:500">{v.get('advanced','')}</span>
                          <div style="color:#7a8aaa;font-size:13px;font-style:italic;margin-top:4px">{v.get('example','')}</div>
                        </div>''', unsafe_allow_html=True)
                with ft4:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("<b style='color:#c96a3a'>💪 Điểm mạnh</b>", unsafe_allow_html=True)
                        for s in result.get("strengths", []):
                            st.markdown(f'<div class="tip-box">✓ {s}</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown("<b style='color:#c96a3a'>🎯 Cần cải thiện</b>", unsafe_allow_html=True)
                        for w in result.get("weaknesses", []):
                            st.markdown(f'<div class="warn-box">• {w}</div>', unsafe_allow_html=True)
            elif result is None:
                st.error("Không parse được kết quả. Thử lại nhé!")


with tab2:
    st.markdown("<h3 style='color:#c96a3a;font-family:Playfair Display,serif'>Bài mẫu Band 8-9</h3>", unsafe_allow_html=True)
    task_type2 = st.selectbox("Task Type", ["Task 2 (Essay)", "Task 1 (Academic)", "Task 1 (General)"], key="tt2")
    question2 = st.text_area("📌 Đề bài", height=110, placeholder="Nhập đề IELTS...", key="q2")

    if st.button("✨ Tạo bài mẫu", use_container_width=True):
        key = st.session_state.get("api_key", "")
        if not key:
            st.error("Vui lòng nhập Gemini API key ở sidebar.")
        elif not question2.strip():
            st.warning("Hãy nhập đề bài trước.")
        else:
            with st.spinner("Đang tạo bài mẫu Band 8-9..."):
                try:
                    raw = call_gemini(SAMPLE_SYSTEM, f"Task: {task_type2}\nQuestion: {question2}", key)
                    result = parse_json_safe(raw)
                except Exception as e:
                    st.error(f"Lỗi API: {e}")
                    result = None

            if result:
                st.markdown("---")
                st.markdown(f'<div class="section-box"><h4>Sample Answer (Band 8-9)</h4>{result.get("sample_answer","").replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
                st.markdown("<b style='color:#c96a3a'>🏗️ Phân tích cấu trúc</b>", unsafe_allow_html=True)
                for section, exp in result.get("structure_breakdown", {}).items():
                    st.markdown(f'<div style="background:#fff;border:1px solid #f5d0bb;border-radius:8px;padding:10px 14px;margin:6px 0"><span style="color:#e8724a;font-weight:500;text-transform:capitalize">{section.replace("_"," ")}: </span><span style="color:#5a2d0c">{exp}</span></div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("<b style='color:#c96a3a'>🔑 Key Phrases</b>", unsafe_allow_html=True)
                    for p in result.get("key_phrases", []):
                        st.markdown(f'<span class="word-chip">"{p}"</span>', unsafe_allow_html=True)
                with c2:
                    st.markdown("<b style='color:#c96a3a'>💡 Band 9 Tips</b>", unsafe_allow_html=True)
                    for t in result.get("band_9_tips", []):
                        st.markdown(f'<div class="tip-box">💡 {t}</div>', unsafe_allow_html=True)


with tab3:
    st.markdown("<h3 style='color:#c96a3a;font-family:Playfair Display,serif'>Từ vựng & Cấu trúc theo chủ đề</h3>", unsafe_allow_html=True)
    topic = st.text_input("🔍 Chủ đề", placeholder="VD: Technology, Environment, Education, Health...")

    if st.button("📚 Lấy từ vựng", use_container_width=True):
        key = st.session_state.get("api_key", "")
        if not key:
            st.error("Vui lòng nhập Gemini API key ở sidebar.")
        elif not topic.strip():
            st.warning("Nhập chủ đề trước nhé.")
        else:
            with st.spinner("Đang tổng hợp từ vựng..."):
                try:
                    raw = call_gemini(VOCAB_SYSTEM, f"Topic: {topic}", key)
                    result = parse_json_safe(raw)
                except Exception as e:
                    st.error(f"Lỗi API: {e}")
                    result = None

            if result:
                st.markdown("---")
                st.markdown("<b style='color:#c96a3a'>🔤 Từ vựng chủ đề</b>", unsafe_allow_html=True)
                for item in result.get("topic_vocabulary", []):
                    colls = ''.join([f'<span class="word-chip">{c}</span>' for c in item.get('collocations',[])])
                    st.markdown(f'''<div style="background:#fff;border:1px solid #f5d0bb;border-radius:10px;padding:12px 16px;margin:8px 0">
                      <span style="color:#e8724a;font-weight:600;font-size:16px">{item.get('word','')}</span>
                      <span style="color:#c4956a;font-size:13px;margin-left:8px">{item.get('definition','')}</span>
                      <div style="color:#a07050;font-size:13px;font-style:italic;margin:5px 0">"{item.get('example','')}"</div>
                      <div>{colls}</div>
                    </div>''', unsafe_allow_html=True)

                st.markdown("<b style='color:#c96a3a'>🔗 Linking Words</b>", unsafe_allow_html=True)
                lcols = st.columns(2)
                for i, (cat, words) in enumerate(result.get("linking_words", {}).items()):
                    with lcols[i % 2]:
                        st.markdown(f"<p style='color:#e8724a;font-weight:500;margin-bottom:4px'>{cat.replace('_',' ').title()}</p>", unsafe_allow_html=True)
                        st.markdown(' '.join([f'<span class="word-chip">{w}</span>' for w in words]), unsafe_allow_html=True)

                st.markdown("<b style='color:#c96a3a'>🏗️ Sentence Structures</b>", unsafe_allow_html=True)
                for s in result.get("common_structures", []):
                    st.markdown(f'<div class="section-box"><h4>{s.get("use","")}</h4><div style="color:#5a2d0c;font-style:italic">"{s.get("structure","")}"</div></div>', unsafe_allow_html=True)

                st.markdown("<b style='color:#c96a3a'>🚀 Band-Boosting Phrases</b>", unsafe_allow_html=True)
                for phrase in result.get("band_boosters", []):
                    st.markdown(f'<span class="word-chip" style="background:#fff0e8;border-color:#e8956a;color:#c96a3a">✦ {phrase}</span>', unsafe_allow_html=True)