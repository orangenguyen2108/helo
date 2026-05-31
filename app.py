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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --navy: #0f172a; --navy-light: #1e293b; --gold: #f59e0b;
    --gold-light: #fcd34d; --text: #e2e8f0; --muted: #94a3b8;
}
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--navy) !important; color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] { background-color: var(--navy-light) !important; border-right: 1px solid rgba(245,158,11,0.2); }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--gold) !important; }
.stTextArea textarea {
    background-color: var(--navy-light) !important; color: var(--text) !important;
    border: 1px solid rgba(245,158,11,0.3) !important; border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 15px !important;
}
.stTextArea textarea:focus { border-color: var(--gold) !important; box-shadow: 0 0 0 2px rgba(245,158,11,0.2) !important; }
.stButton > button {
    background: linear-gradient(135deg, #f59e0b, #d97706) !important; color: #0f172a !important;
    font-weight: 700 !important; border: none !important; border-radius: 8px !important;
    padding: 0.6rem 2rem !important; font-size: 15px !important; transition: all 0.2s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 20px rgba(245,158,11,0.4) !important; }
.score-card { background: var(--navy-light); border: 1px solid rgba(245,158,11,0.25); border-radius: 12px; padding: 16px 20px; text-align: center; margin-bottom: 8px; }
.score-card .label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--muted); margin-bottom: 4px; }
.score-card .value { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 700; }
.band-badge {
    display: inline-block; background: linear-gradient(135deg, #f59e0b, #d97706); color: #0f172a;
    font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 700;
    padding: 12px 28px; border-radius: 12px; margin: 8px 0;
}
.section-box { background: var(--navy-light); border-left: 3px solid var(--gold); border-radius: 0 10px 10px 0; padding: 16px 20px; margin: 12px 0; }
.section-box h4 { color: var(--gold-light) !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px !important; }
.tip-box { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3); border-radius: 10px; padding: 12px 16px; margin: 6px 0; font-size: 14px; color: #6ee7b7; }
.word-chip { display: inline-block; background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.4); color: #93c5fd; border-radius: 20px; padding: 3px 12px; margin: 3px; font-size: 13px; }
hr { border-color: rgba(245,158,11,0.15) !important; }
.header-hero { background: linear-gradient(135deg, rgba(245,158,11,0.08) 0%, rgba(15,23,42,0) 60%); border: 1px solid rgba(245,158,11,0.15); border-radius: 16px; padding: 28px 32px; margin-bottom: 24px; }
[data-testid="stMarkdownContainer"] p { color: var(--text); line-height: 1.7; }
</style>
""", unsafe_allow_html=True)


# ── Gemini via REST ───────────────────────────────────────────────────────────
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

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
    if score >= 7.5: return "#10b981"
    elif score >= 6.5: return "#3b82f6"
    elif score >= 5.5: return "#f59e0b"
    else: return "#ef4444"


# ── Prompts ───────────────────────────────────────────────────────────────────
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


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✍️ IELTS Writing Coach")
    st.markdown("---")
    st.markdown("🔑 **Gemini API Key (Free)**")
    st.markdown("<small>Lấy tại [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)</small>", unsafe_allow_html=True)
    api_key = st.text_input("", type="password", placeholder="AIza...", label_visibility="collapsed")
    if api_key:
        st.session_state["api_key"] = api_key
        st.success("API key set ✓")
    st.markdown("---")
    st.markdown("### 📚 Tính năng")
    st.markdown("""
- 🎯 Chấm band score (4 tiêu chí)
- ❌ Phát hiện lỗi ngữ pháp
- 💬 Gợi ý từ vựng nâng band
- 📝 Sample answer Band 8-9
- 🏗️ Phân tích cấu trúc bài
- 🚀 Band-boosting phrases
""")
    st.markdown("---")
    for b, c in [("9","#10b981"),("8","#10b981"),("7","#3b82f6"),("6","#f59e0b"),("5","#ef4444")]:
        st.markdown(f'<div style="margin:4px 0"><span style="background:{c};color:white;border-radius:4px;padding:2px 10px;font-weight:700">Band {b}</span></div>', unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-hero">
  <h1 style="margin:0;font-size:2.2rem">IELTS Writing Coach</h1>
  <p style="color:#94a3b8;margin:8px 0 0;font-size:15px">Powered by Google Gemini (Free) • Chấm bài • Sửa lỗi • Band score</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Chấm bài", "📖 Sample Answer", "📚 Vocab & Tips"])


# ── Tab 1: Chấm bài ───────────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        task_type = st.selectbox("Task Type", ["Task 2 (Essay)", "Task 1 (Academic)", "Task 1 (General)"])
    with col2:
        wct = "250+" if "Task 2" in task_type else "150+"
        st.markdown(f"<br><span style='color:#94a3b8;font-size:13px'>📌 Tối thiểu: <b style='color:#f59e0b'>{wct} words</b></span>", unsafe_allow_html=True)

    question = st.text_area("📌 Câu hỏi / Đề bài", height=100, placeholder="Dán đề IELTS vào đây...")
    essay = st.text_area("✍️ Bài viết của bạn", height=280, placeholder="Viết hoặc dán bài vào đây...")

    wc = len(essay.split()) if essay.strip() else 0
    if essay.strip():
        wc_color = "#10b981" if wc >= (250 if "Task 2" in task_type else 150) else "#ef4444"
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
                st.markdown(f'<div style="text-align:center;margin:16px 0"><div style="font-size:12px;text-transform:uppercase;letter-spacing:2px;color:#94a3b8">Overall Band Score</div><div class="band-badge">{overall}</div></div>', unsafe_allow_html=True)

                cols = st.columns(4)
                for i, (label, key_name) in enumerate([("Task Achievement","task_achievement"),("Coherence & Cohesion","coherence_cohesion"),("Lexical Resource","lexical_resource"),("Grammatical Range","grammatical_range")]):
                    score = result.get(key_name, 0)
                    with cols[i]:
                        st.markdown(f'<div class="score-card"><div class="label">{label}</div><div class="value" style="color:{band_color(score)}">{score}</div></div>', unsafe_allow_html=True)

                ft1, ft2, ft3, ft4 = st.tabs(["💬 Nhận xét", "❌ Lỗi ngữ pháp", "📈 Từ vựng", "✅ Điểm mạnh/yếu"])
                with ft1:
                    st.markdown(f'<div class="section-box"><h4>Detailed Feedback</h4>{result.get("detailed_feedback","")}</div>', unsafe_allow_html=True)
                with ft2:
                    errors = result.get("grammar_errors", [])
                    if errors:
                        for e in errors:
                            st.markdown(f'''<div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:12px 16px;margin:8px 0">
                              <div style="color:#ef4444;text-decoration:line-through">"{e.get('original','')}"</div>
                              <div style="color:#10b981;margin:4px 0">✓ "{e.get('correction','')}"</div>
                              <div style="color:#94a3b8;font-size:13px">{e.get('explanation','')}</div>
                            </div>''', unsafe_allow_html=True)
                    else:
                        st.success("Không có lỗi ngữ pháp nghiêm trọng!")
                with ft3:
                    for v in result.get("vocabulary_suggestions", []):
                        st.markdown(f'''<div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);border-radius:8px;padding:12px 16px;margin:8px 0">
                          <span style="color:#94a3b8;text-decoration:line-through">{v.get('basic','')}</span>
                          <span style="color:#94a3b8"> → </span>
                          <span style="color:#93c5fd;font-weight:600">{v.get('advanced','')}</span>
                          <div style="color:#64748b;font-size:13px;font-style:italic;margin-top:4px">{v.get('example','')}</div>
                        </div>''', unsafe_allow_html=True)
                with ft4:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**💪 Strengths**")
                        for s in result.get("strengths", []):
                            st.markdown(f'<div class="tip-box">✓ {s}</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown("**🎯 Cần cải thiện**")
                        for w in result.get("weaknesses", []):
                            st.markdown(f'<div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);border-radius:8px;padding:10px 14px;margin:6px 0;font-size:14px;color:#fcd34d">• {w}</div>', unsafe_allow_html=True)
            elif result is None:
                st.error("Không parse được kết quả. Thử lại nhé!")


# ── Tab 2: Sample Answer ──────────────────────────────────────────────────────
with tab2:
    st.markdown("### 📖 Bài mẫu Band 8-9")
    task_type2 = st.selectbox("Task Type", ["Task 2 (Essay)", "Task 1 (Academic)", "Task 1 (General)"], key="tt2")
    question2 = st.text_area("📌 Đề bài", height=120, placeholder="Nhập đề IELTS...", key="q2")

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
                st.markdown("#### 🏗️ Phân tích cấu trúc")
                for section, exp in result.get("structure_breakdown", {}).items():
                    st.markdown(f'<div style="background:var(--navy-light);border-radius:8px;padding:12px 16px;margin:6px 0"><span style="color:#f59e0b;font-weight:600;text-transform:capitalize">{section.replace("_"," ")}: </span><span style="color:#cbd5e1">{exp}</span></div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### 🔑 Key Phrases")
                    for p in result.get("key_phrases", []):
                        st.markdown(f'<span class="word-chip">"{p}"</span>', unsafe_allow_html=True)
                with c2:
                    st.markdown("#### 💡 Band 9 Tips")
                    for t in result.get("band_9_tips", []):
                        st.markdown(f'<div class="tip-box">💡 {t}</div>', unsafe_allow_html=True)


# ── Tab 3: Vocab & Tips ───────────────────────────────────────────────────────
with tab3:
    st.markdown("### 📚 Từ vựng & Cấu trúc theo chủ đề")
    topic = st.text_input("🔍 Chủ đề", placeholder="VD: Technology, Environment, Education...")

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
                st.markdown("#### 🔤 Từ vựng chủ đề")
                for item in result.get("topic_vocabulary", []):
                    colls = ''.join([f'<span class="word-chip">{c}</span>' for c in item.get('collocations',[])])
                    st.markdown(f'''<div style="background:var(--navy-light);border:1px solid rgba(245,158,11,0.2);border-radius:10px;padding:14px 18px;margin:8px 0">
                      <span style="color:#f59e0b;font-weight:700;font-size:16px">{item.get('word','')}</span>
                      <span style="color:#64748b;font-size:13px;margin-left:8px">{item.get('definition','')}</span>
                      <div style="color:#94a3b8;font-size:13px;font-style:italic;margin:6px 0">"{item.get('example','')}"</div>
                      <div>{colls}</div>
                    </div>''', unsafe_allow_html=True)

                st.markdown("#### 🔗 Linking Words")
                lcols = st.columns(2)
                for i, (cat, words) in enumerate(result.get("linking_words", {}).items()):
                    with lcols[i % 2]:
                        st.markdown(f"**{cat.replace('_',' ').title()}**")
                        st.markdown(' '.join([f'<span class="word-chip">{w}</span>' for w in words]), unsafe_allow_html=True)

                st.markdown("#### 🏗️ Sentence Structures")
                for s in result.get("common_structures", []):
                    st.markdown(f'<div class="section-box"><h4>{s.get("use","")}</h4><div style="color:#e2e8f0;font-style:italic">"{s.get("structure","")}"</div></div>', unsafe_allow_html=True)

                st.markdown("#### 🚀 Band-Boosting Phrases")
                for phrase in result.get("band_boosters", []):
                    st.markdown(f'<span class="word-chip" style="background:rgba(245,158,11,0.1);border-color:rgba(245,158,11,0.4);color:#fcd34d">✦ {phrase}</span>', unsafe_allow_html=True)
