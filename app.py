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
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --paper: #F6F3ED;
    --surface: #FFFFFF;
    --ink: #232A2E;
    --ink-soft: #6B7480;
    --rule: #DDD7CB;
    --primary: #1F5C5B;
    --primary-dark: #163F3F;
    --primary-tint: #E7EFEE;
    --red-pen: #B33A2E;
    --red-pen-tint: #FBEEEC;
    --gold: #B8902E;
    --gold-tint: #F7F0DE;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--paper) !important;
    color: var(--ink) !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--rule);
}
h1, h2, h3 {
    font-family: 'Source Serif 4', serif !important;
    color: var(--ink) !important;
    font-weight: 600 !important;
}
.stTextArea textarea, .stTextInput input {
    background-color: var(--surface) !important;
    color: var(--ink) !important;
    border: 1px solid var(--rule) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(31,92,91,0.12) !important;
}
.stButton > button {
    background: var(--primary) !important;
    color: #fff !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 2rem !important;
    font-size: 15px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: var(--primary-dark) !important;
    transform: translateY(-1px) !important;
}
.stSelectbox > div > div {
    background-color: var(--surface) !important;
    color: var(--ink) !important;
    border-color: var(--rule) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent !important;
    border-bottom: 1px solid var(--rule) !important;
    gap: 28px !important;
    padding: 0 0 0 2px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important;
    color: var(--ink-soft) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    padding: 0 0 10px 0 !important;
    background-color: transparent !important;
}
.stTabs [aria-selected="true"] {
    background-color: transparent !important;
    color: var(--primary) !important;
    border-bottom: 2px solid var(--primary) !important;
}
[data-testid="stMarkdownContainer"] p { color: var(--ink); line-height: 1.7; }
hr { border-color: var(--rule) !important; }

/* Letterhead header */
.header-hero {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-bottom: 3px solid var(--primary);
    border-radius: 10px 10px 4px 4px;
    padding: 26px 32px;
    margin-bottom: 22px;
}
.header-hero .eyebrow {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: var(--primary);
    font-weight: 600;
    margin-bottom: 8px;
}
.header-hero h1 {
    margin: 0;
    font-size: 2.1rem;
    font-family: 'Source Serif 4', serif;
}
.header-hero p {
    color: var(--ink-soft);
    margin: 8px 0 0;
    font-size: 14px;
}

/* Band seal */
.band-seal-wrap { text-align: center; margin: 18px 0 24px; }
.band-seal-wrap .eyebrow {
    font-size: 11px; text-transform: uppercase; letter-spacing: 2.5px;
    color: var(--ink-soft); margin-bottom: 12px; font-weight: 600;
}
.band-seal {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 124px; height: 124px;
    border-radius: 50%;
    border: 3px double var(--primary);
    background: var(--primary-tint);
    font-family: 'Source Serif 4', serif;
    font-size: 44px;
    font-weight: 700;
    color: var(--primary);
    transform: rotate(-4deg);
}

/* Test Report Form style score row */
.trf-row {
    display: flex;
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 10px;
    overflow: hidden;
    margin: 18px 0;
}
.trf-cell {
    flex: 1;
    text-align: center;
    padding: 16px 8px;
    border-right: 1px solid var(--rule);
}
.trf-cell:last-child { border-right: none; }
.trf-cell .label {
    font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px;
    color: var(--ink-soft); margin-bottom: 6px; font-weight: 600;
}
.trf-cell .value {
    font-family: 'Source Serif 4', serif;
    font-size: 28px; font-weight: 700;
}

/* Section box */
.section-box {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 8px;
    padding: 16px 18px;
    margin: 10px 0;
    color: var(--ink);
}
.section-box h4 {
    color: var(--ink-soft) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0 0 10px 0 !important;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--rule);
    font-weight: 600 !important;
}

/* Strength / weakness / tip items */
.feedback-item {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 14px;
}
.feedback-item.positive { border-left: 3px solid var(--primary); }
.feedback-item.gold { border-left: 3px solid var(--gold); }

/* Red-pen grammar correction card */
.redpen-card {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-left: 3px solid var(--red-pen);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
}
.redpen-original { color: var(--red-pen); text-decoration: line-through; font-size: 14px; }
.redpen-correction { color: var(--primary); font-weight: 600; margin-top: 4px; font-size: 14px; }
.redpen-note { color: var(--ink-soft); font-size: 13px; margin-top: 6px; font-style: italic; }

/* Vocabulary upgrade row */
.vocab-row {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
}
.vocab-words { font-size: 15px; }
.vocab-basic { color: var(--ink-soft); text-decoration: line-through; }
.vocab-arrow { color: var(--ink-soft); margin: 0 8px; }
.vocab-advanced { color: var(--primary); font-weight: 600; }
.vocab-example { color: var(--ink-soft); font-size: 13px; font-style: italic; margin-top: 4px; }

/* Topic vocabulary card */
.vocab-topic-card {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
}
.vocab-topic-card .word { color: var(--primary); font-weight: 700; font-size: 16px; font-family: 'Source Serif 4', serif; }
.vocab-topic-card .definition { color: var(--ink-soft); font-size: 13px; margin-left: 8px; }
.vocab-topic-card .example { color: var(--ink); font-size: 13px; font-style: italic; margin: 6px 0; }

/* Chips */
.chip {
    display: inline-block;
    background: var(--primary-tint);
    border: 1px solid var(--rule);
    color: var(--primary);
    border-radius: 6px;
    padding: 4px 12px;
    margin: 3px;
    font-size: 13px;
    font-family: 'Inter', sans-serif;
}
.chip.gold { background: var(--gold-tint); color: var(--gold); }

/* Sidebar feature list */
.sb-feature {
    color: var(--ink-soft);
    font-size: 13px;
    margin: 4px 0;
    padding-left: 10px;
    border-left: 2px solid var(--rule);
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
    if score >= 7.5: return "var(--primary)"
    elif score >= 6.5: return "#3D7A6E"
    elif score >= 5.5: return "var(--gold)"
    else: return "var(--red-pen)"


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
    st.markdown("<div style='color:var(--primary);font-size:11px;text-transform:uppercase;letter-spacing:2px;font-weight:600;margin-bottom:2px'>IELTS Writing</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-family:\"Source Serif 4\",serif;color:var(--ink);margin:0 0 4px 0'>✍️ Coach</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:var(--ink-soft);font-size:13px;margin-bottom:16px'>Powered by Google Gemini</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:var(--ink);font-size:13px;font-weight:600;margin-bottom:4px'>🔑 Gemini API Key (Free)</p>", unsafe_allow_html=True)
    st.markdown("<small style='color:var(--ink-soft)'>Lấy tại <a href='https://aistudio.google.com/app/apikey' style='color:var(--primary)'>aistudio.google.com</a></small>", unsafe_allow_html=True)
    api_key = st.text_input("", type="password", placeholder="AIza...", label_visibility="collapsed")
    if api_key:
        st.session_state["api_key"] = api_key
        st.success("API key set ✓")
    st.markdown("---")
    st.markdown("<p style='color:var(--ink);font-size:13px;font-weight:600;margin-bottom:6px'>📚 Tính năng</p>", unsafe_allow_html=True)
    for feat in ["🎯 Chấm band score (4 tiêu chí)", "✏️ Phát hiện lỗi ngữ pháp", "💬 Gợi ý từ vựng nâng band", "📝 Sample answer Band 8-9", "🏗️ Phân tích cấu trúc bài", "🚀 Band-boosting phrases"]:
        st.markdown(f"<div class='sb-feature'>{feat}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='color:var(--ink);font-size:13px;font-weight:600;margin-bottom:8px'>📊 Band Scale</p>", unsafe_allow_html=True)
    for label, var in [("Band 8-9", "primary"), ("Band 6-7", "gold"), ("Band 4-5", "red-pen")]:
        st.markdown(f'<span class="chip" style="background:var(--{var}-tint);color:var(--{var});margin-right:6px">{label}</span>', unsafe_allow_html=True)


st.markdown("""
<div class="header-hero">
  <div class="eyebrow">Writing Assessment</div>
  <h1>IELTS Writing Coach</h1>
  <p>Chấm bài • Sửa lỗi ngữ pháp • Gợi ý từ vựng • Band score dự đoán</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Chấm bài", "📖 Sample Answer", "📚 Vocab & Tips"])


with tab1:
    col1, col2 = st.columns(2)
    with col1:
        task_type = st.selectbox("Task Type", ["Task 2 (Essay)", "Task 1 (Academic)", "Task 1 (General)"])
    with col2:
        wct = "250+" if "Task 2" in task_type else "150+"
        st.markdown(f"<br><span style='color:var(--ink-soft);font-size:13px'>📌 Tối thiểu: <b style='color:var(--primary)'>{wct} words</b></span>", unsafe_allow_html=True)

    question = st.text_area("📌 Câu hỏi / Đề bài", height=90, placeholder="Dán đề IELTS vào đây...")
    essay = st.text_area("✍️ Bài viết của bạn", height=260, placeholder="Viết hoặc dán bài vào đây...")

    wc = len(essay.split()) if essay.strip() else 0
    if essay.strip():
        wc_color = "var(--primary)" if wc >= (250 if "Task 2" in task_type else 150) else "var(--red-pen)"
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
                st.markdown(f'''<div class="band-seal-wrap">
                  <div class="eyebrow">Overall Band Score</div>
                  <div class="band-seal">{overall}</div>
                </div>''', unsafe_allow_html=True)

                criteria = [("Task Achievement", "task_achievement"), ("Coherence & Cohesion", "coherence_cohesion"),
                             ("Lexical Resource", "lexical_resource"), ("Grammatical Range", "grammatical_range")]
                cells = ""
                for label, kn in criteria:
                    score = result.get(kn, 0)
                    cells += f'<div class="trf-cell"><div class="label">{label}</div><div class="value" style="color:{band_color(score)}">{score}</div></div>'
                st.markdown(f'<div class="trf-row">{cells}</div>', unsafe_allow_html=True)

                ft1, ft2, ft3, ft4 = st.tabs(["💬 Nhận xét", "✏️ Lỗi ngữ pháp", "📈 Từ vựng", "✅ Điểm mạnh/yếu"])
                with ft1:
                    st.markdown(f'<div class="section-box"><h4>Detailed Feedback</h4>{result.get("detailed_feedback","")}</div>', unsafe_allow_html=True)
                with ft2:
                    errors = result.get("grammar_errors", [])
                    if errors:
                        for e in errors:
                            st.markdown(f'''<div class="redpen-card">
                              <div class="redpen-original">{e.get('original','')}</div>
                              <div class="redpen-correction">→ {e.get('correction','')}</div>
                              <div class="redpen-note">{e.get('explanation','')}</div>
                            </div>''', unsafe_allow_html=True)
                    else:
                        st.success("Không có lỗi ngữ pháp nghiêm trọng!")
                with ft3:
                    for v in result.get("vocabulary_suggestions", []):
                        st.markdown(f'''<div class="vocab-row">
                          <div class="vocab-words">
                            <span class="vocab-basic">{v.get('basic','')}</span>
                            <span class="vocab-arrow">→</span>
                            <span class="vocab-advanced">{v.get('advanced','')}</span>
                          </div>
                          <div class="vocab-example">{v.get('example','')}</div>
                        </div>''', unsafe_allow_html=True)
                with ft4:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px'>💪 Điểm mạnh</p>", unsafe_allow_html=True)
                        for s in result.get("strengths", []):
                            st.markdown(f'<div class="feedback-item positive">✓ {s}</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px'>🎯 Cần cải thiện</p>", unsafe_allow_html=True)
                        for w in result.get("weaknesses", []):
                            st.markdown(f'<div class="feedback-item gold">→ {w}</div>', unsafe_allow_html=True)
            elif result is None:
                st.error("Không parse được kết quả. Thử lại nhé!")


with tab2:
    st.markdown("<h3 style='margin-top:0'>Bài mẫu Band 8-9</h3>", unsafe_allow_html=True)
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
                st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin:14px 0 8px'>🏗️ Phân tích cấu trúc</p>", unsafe_allow_html=True)
                for section, exp in result.get("structure_breakdown", {}).items():
                    st.markdown(f'<div class="section-box"><h4>{section.replace("_"," ").title()}</h4>{exp}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px'>🔑 Key Phrases</p>", unsafe_allow_html=True)
                    for p in result.get("key_phrases", []):
                        st.markdown(f'<span class="chip">"{p}"</span>', unsafe_allow_html=True)
                with c2:
                    st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px'>💡 Band 9 Tips</p>", unsafe_allow_html=True)
                    for t in result.get("band_9_tips", []):
                        st.markdown(f'<div class="feedback-item gold">💡 {t}</div>', unsafe_allow_html=True)


with tab3:
    st.markdown("<h3 style='margin-top:0'>Từ vựng & Cấu trúc theo chủ đề</h3>", unsafe_allow_html=True)
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
                st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px'>🔤 Từ vựng chủ đề</p>", unsafe_allow_html=True)
                for item in result.get("topic_vocabulary", []):
                    colls = ''.join([f'<span class="chip">{c}</span>' for c in item.get('collocations', [])])
                    st.markdown(f'''<div class="vocab-topic-card">
                      <span class="word">{item.get('word','')}</span>
                      <span class="definition">{item.get('definition','')}</span>
                      <div class="example">"{item.get('example','')}"</div>
                      <div>{colls}</div>
                    </div>''', unsafe_allow_html=True)

                st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin:18px 0 8px'>🔗 Linking Words</p>", unsafe_allow_html=True)
                lcols = st.columns(2)
                for i, (cat, words) in enumerate(result.get("linking_words", {}).items()):
                    with lcols[i % 2]:
                        st.markdown(f"<p style='color:var(--primary);font-weight:600;font-size:13px;margin-bottom:4px'>{cat.replace('_',' ').title()}</p>", unsafe_allow_html=True)
                        st.markdown(' '.join([f'<span class="chip">{w}</span>' for w in words]), unsafe_allow_html=True)

                st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin:18px 0 8px'>🏗️ Sentence Structures</p>", unsafe_allow_html=True)
                for s in result.get("common_structures", []):
                    st.markdown(f'<div class="section-box"><h4>{s.get("use","")}</h4><div style="color:var(--ink);font-style:italic">"{s.get("structure","")}"</div></div>', unsafe_allow_html=True)

                st.markdown("<p style='color:var(--ink);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin:18px 0 8px'>🚀 Band-Boosting Phrases</p>", unsafe_allow_html=True)
                for phrase in result.get("band_boosters", []):
                    st.markdown(f'<span class="chip gold">✦ {phrase}</span>', unsafe_allow_html=True)
