import streamlit as st
from graph.interview_graph import graph
from modules.evaluate_answer import evaluate_answer
from modules.final_report import generate_final_report

# ─────────────────────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Interviewer", page_icon="🎯", layout="centered")


# ─────────────────────────────────────────────────────────────
# 2. STYLES  (light + dark mode, mobile-friendly)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header  { visibility: hidden; }
.block-container { max-width: 660px !important; padding: 2rem 1.25rem 5rem !important; }

/* ── Colour tokens ── */
[data-theme="light"] {
    --ink:         #1a1a2e;
    --ink-soft:    #64748b;
    --surface:     #ffffff;
    --surface-2:   #f8f7ff;
    --border:      #e2e8f0;
    --purple:      #6366f1;
    --purple-dark: #4338ca;
    --purple-bg:   #eef2ff;
    --purple-txt:  #4338ca;
    --teal:        #0d9488;
    --teal-bg:     #f0fdfa;
    --teal-bd:     #99f6e4;
    --amber:       #d97706;
    --amber-bg:    #fffbeb;
    --amber-bd:    #fcd34d;
    --red:         #dc2626;
    --red-bg:      #fef2f2;
    --red-bd:      #fca5a5;
    --shadow:      0 2px 8px rgba(99,102,241,.08), 0 1px 2px rgba(0,0,0,.05);
    --shadow-lg:   0 8px 30px rgba(99,102,241,.12);
}
[data-theme="dark"] {
    --ink:         #e2e8f0;
    --ink-soft:    #94a3b8;
    --surface:     #16162a;
    --surface-2:   #1e1e35;
    --border:      #2d2d4e;
    --purple:      #818cf8;
    --purple-dark: #a5b4fc;
    --purple-bg:   #1e1b4b;
    --purple-txt:  #c7d2fe;
    --teal:        #2dd4bf;
    --teal-bg:     #042f2e;
    --teal-bd:     #0f766e;
    --amber:       #fbbf24;
    --amber-bg:    #1c1000;
    --amber-bd:    #92400e;
    --red:         #f87171;
    --red-bg:      #200a0a;
    --red-bd:      #7f1d1d;
    --shadow:      0 2px 8px rgba(0,0,0,.3);
    --shadow-lg:   0 8px 30px rgba(0,0,0,.4);
}

/* ── Step bar at the top ── */
.steps        { display:flex; align-items:center; margin-bottom:2.25rem; }
.step         { display:flex; align-items:center; gap:8px; }
.dot          { width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0; border:2px solid var(--border); background:var(--surface); color:var(--ink-soft); transition:all .25s; }
.dot.active   { background:var(--purple); border-color:var(--purple); color:#fff; box-shadow:0 0 0 5px color-mix(in srgb,var(--purple) 20%,transparent); }
.dot.done     { background:var(--teal);   border-color:var(--teal);   color:#fff; }
.step-lbl     { font-size:12px; font-weight:500; color:var(--ink-soft); }
.step-lbl.on  { color:var(--ink); font-weight:600; }
.line         { flex:1; height:2px; background:var(--border); margin:0 8px; max-width:72px; border-radius:2px; }
.line.done    { background:var(--teal); }

/* ── Hero (upload page) ── */
.hero         { text-align:center; padding:2rem 0 1rem; }
.hero-icon    { font-size:3.5rem; margin-bottom:.5rem; display:block; }
.hero h1      { font-family:'Sora',sans-serif; font-size:clamp(1.8rem,5vw,2.6rem); font-weight:700; color:var(--ink); margin:0 0 .5rem; line-height:1.2; }
.hero p       { color:var(--ink-soft); font-size:clamp(.9rem,2.5vw,1rem); margin:0 0 2rem; line-height:1.65; }

/* ── Feature row ── */
.features     { display:grid; grid-template-columns:repeat(3,1fr); gap:.75rem; margin:1.5rem 0; }
@media(max-width:480px){ .features{ grid-template-columns:1fr; } }
.feat         { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:1.1rem .9rem; text-align:center; box-shadow:var(--shadow); }
.feat-icon    { font-size:1.6rem; margin-bottom:.35rem; }
.feat-title   { font-family:'Sora',sans-serif; font-size:.85rem; font-weight:600; color:var(--ink); margin-bottom:.2rem; }
.feat-desc    { font-size:.78rem; color:var(--ink-soft); line-height:1.45; }

/* ── Upload drop-zone ── */
.drop-zone    { background:var(--surface-2); border:2px dashed var(--border); border-radius:16px; padding:2.25rem 1.5rem; text-align:center; transition:border-color .2s; margin-bottom:.5rem; }
.drop-zone:hover { border-color:var(--purple); }
.drop-zone p  { margin:.25rem 0 0; font-size:.85rem; color:var(--ink-soft); }

/* ── Info / success banners ── */
.info         { background:var(--purple-bg); border:1px solid var(--purple); border-radius:11px; padding:.85rem 1rem; font-size:.88rem; color:var(--purple-txt); margin-bottom:1rem; }
.success      { background:var(--teal-bg); border:1px solid var(--teal-bd); border-radius:14px; padding:2rem; text-align:center; margin-bottom:1.5rem; }
.success h3   { font-family:'Sora',sans-serif; color:var(--teal); margin:.5rem 0 .3rem; font-size:1.35rem; }
.success p    { color:var(--ink-soft); font-size:.9rem; margin:0; }

/* ── Progress bar (interview page) ── */
.prog-header  { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.35rem; }
.prog-title   { font-family:'Sora',sans-serif; font-size:1.3rem; font-weight:700; color:var(--ink); }
.prog-count   { font-size:.8rem; color:var(--ink-soft); font-weight:500; }
.prog-bar     { height:8px; background:var(--border); border-radius:99px; overflow:hidden; margin-bottom:1.5rem; }
.prog-fill    { height:100%; border-radius:99px; background:linear-gradient(90deg,var(--purple),#a78bfa); transition:width .6s cubic-bezier(.4,0,.2,1); }

/* ── Question card ── */
.q-pill       { display:inline-block; background:var(--purple-bg); color:var(--purple-txt); border-radius:20px; font-size:11px; font-weight:600; letter-spacing:.07em; text-transform:uppercase; padding:4px 13px; margin-bottom:1rem; }
.q-box        { background:var(--surface); border:1px solid var(--border); border-left:5px solid var(--purple); border-radius:0 14px 14px 0; padding:1.4rem 1.6rem; margin-bottom:1.6rem; box-shadow:var(--shadow); }
.q-box p      { font-size:clamp(1rem,3vw,1.15rem); color:var(--ink); line-height:1.75; margin:0; }

/* ── Previous answer display ── */
.ans-box      { background:var(--surface-2); border:1px solid var(--border); border-radius:11px; padding:1rem 1.1rem; margin-bottom:1.1rem; }
.ans-label    { font-size:.72rem; font-weight:600; text-transform:uppercase; letter-spacing:.06em; color:var(--ink-soft); margin-bottom:.5rem; display:flex; align-items:center; gap:.5rem; }
.ans-text     { font-size:.93rem; color:var(--ink); line-height:1.65; }

/* ── Score badges ── */
.badge        { display:inline-flex; align-items:center; padding:3px 11px; border-radius:20px; font-size:12px; font-weight:700; }
.hi  { background:var(--teal-bg);  color:var(--teal);  border:1px solid var(--teal-bd); }
.mid { background:var(--amber-bg); color:var(--amber); border:1px solid var(--amber-bd); }
.lo  { background:var(--red-bg);   color:var(--red);   border:1px solid var(--red-bd); }

/* ── Report stats grid ── */
.stats        { display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; margin-bottom:1.4rem; }
@media(max-width:420px){ .stats{ grid-template-columns:1fr 1fr; } }
.stat         { background:var(--surface); border:1px solid var(--border); border-radius:13px; padding:1.1rem .75rem; text-align:center; box-shadow:var(--shadow); }
.stat-lbl     { font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.06em; color:var(--ink-soft); margin-bottom:.35rem; }
.stat-num     { font-family:'Sora',sans-serif; font-size:2.1rem; font-weight:700; color:var(--ink); line-height:1; }
.stat-unit    { font-size:.82rem; color:var(--ink-soft); }

/* ── Section heading ── */
.sec-title    { font-family:'Sora',sans-serif; font-size:1.1rem; font-weight:600; color:var(--ink); margin:1.5rem 0 .85rem; }

/* ── Report feedback card ── */
.feedback     { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:1.4rem 1.5rem; line-height:1.9; color:var(--ink); white-space:pre-line; box-shadow:var(--shadow); font-size:.95rem; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--purple), var(--purple-dark)) !important;
    color: #fff !important; border: none !important; border-radius: 11px !important;
    font-family: 'Sora', sans-serif !important; font-weight: 600 !important;
    font-size: .95rem !important; padding: .65rem 1.5rem !important;
    width: 100%; transition: all .2s !important;
    box-shadow: 0 2px 8px rgba(99,102,241,.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,.35) !important;
}

.divider { border:none; border-top:1px solid var(--border); margin:1.4rem 0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 3. SESSION STATE  — four keys, set once
# ─────────────────────────────────────────────────────────────
for key, val in {"page": "upload", "state": None, "q_index": 0, "done": False}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ─────────────────────────────────────────────────────────────
# 4. HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────
def go(page):
    """Change page and immediately rerun."""
    st.session_state.page = page
    st.rerun()


def step_bar(current):
    """Show the Upload → Interview → Report progress bar."""
    pages  = ["upload", "interview", "report"]
    labels = ["Upload",  "Interview",  "Report"]
    idx    = pages.index(current)
    html   = '<div class="steps">'
    for i, label in enumerate(labels):
        dot = "done" if i < idx else ("active" if i == idx else "")
        lbl = "on"   if i == idx else ""
        num = "✓"    if i < idx else str(i + 1)
        html += f'<div class="step"><div class="dot {dot}">{num}</div><span class="step-lbl {lbl}">{label}</span></div>'
        if i < 2:
            html += f'<div class="line {"done" if idx > i else ""}"></div>'
    st.markdown(html + '</div>', unsafe_allow_html=True)


def badge(score):
    """Coloured score pill: green ≥7, amber ≥4, red <4."""
    if score is None:
        return ""
    cls = "hi" if score >= 7 else ("mid" if score >= 4 else "lo")
    return f'<span class="badge {cls}">{score}/10</span>'


# ─────────────────────────────────────────────────────────────
# 5. PAGE — UPLOAD
# ─────────────────────────────────────────────────────────────
def page_upload():
    step_bar("upload")

    # Hero section
    st.markdown("""
    <div class="hero">
        <span class="hero-icon">🤖</span>
        <h1>Your AI Interview Coach</h1>
        <p>Upload your résumé and get a personalised technical interview<br>
        based on <em>your</em> skills — plus a full feedback report at the end.</p>
    </div>
    """, unsafe_allow_html=True)

    # File uploader
    pdf = st.file_uploader("Upload your résumé (PDF)", type=["pdf"], label_visibility="collapsed")

    if pdf:
        # Show confirmation and start button
        st.markdown('<div class="info">✅ <strong>Resume uploaded!</strong> Click the button below to start your interview.</div>', unsafe_allow_html=True)

        if st.button("🚀  Start My Interview", use_container_width=True):
            with st.spinner("Reading your résumé and building your questions…"):
                result = graph.invoke({
                    "resume_file":      pdf,
                    "resume_text":      "",
                    "skills":           [],
                    "questions":        [],
                    "question":         "",
                    "current_question": 0,
                    "answers":          [],
                    "scores":           [],
                    "report":           "",
                })
                result["current_question"] = 0
                st.session_state.state   = result
                st.session_state.q_index = 0
                st.session_state.done    = False
            go("interview")

    else:
        # Empty state — drop zone hint + feature cards
        st.markdown("""
        <div class="drop-zone">
            <div style="font-size:2.5rem">📄</div>
            <strong style="color:var(--ink)">Drop your PDF résumé here</strong>
            <p>PDF only · max 10 MB · processed privately</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="features">
            <div class="feat">
                <div class="feat-icon">🔍</div>
                <div class="feat-title">Smart Detection</div>
                <div class="feat-desc">Reads your skills automatically from the résumé</div>
            </div>
            <div class="feat">
                <div class="feat-icon">🎤</div>
                <div class="feat-title">Live Interview</div>
                <div class="feat-desc">10 targeted questions, one at a time</div>
            </div>
            <div class="feat">
                <div class="feat-icon">📊</div>
                <div class="feat-title">Full Report</div>
                <div class="feat-desc">Strengths, weaknesses & how to improve</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 6. PAGE — INTERVIEW  (one question at a time)
# ─────────────────────────────────────────────────────────────
def page_interview():
    step_bar("interview")

    state    = st.session_state.state
    q_idx    = st.session_state.q_index
    total    = len(state["questions"])
    answered = len(state["answers"])

    # Progress bar
    pct = int(answered / total * 100)
    st.markdown(
        f'<div class="prog-header">'
        f'  <span class="prog-title">Interview</span>'
        f'  <span class="prog-count">{answered} of {total} answered</span>'
        f'</div>'
        f'<div class="prog-bar"><div class="prog-fill" style="width:{pct}%"></div></div>',
        unsafe_allow_html=True,
    )

    # ── If all questions are done, show completion banner ─────
    if st.session_state.done:
        st.markdown("""
        <div class="success">
            <div style="font-size:2.5rem">🎉</div>
            <h3>Interview Complete!</h3>
            <p>Great work! Your personalised report is ready.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📊  View My Report", use_container_width=True):
            go("report")
        return

    # ── Show the current question ─────────────────────────────
    question = state["questions"][q_idx]
    st.markdown(f'<span class="q-pill">Question {q_idx + 1} of {total}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="q-box"><p>{question}</p></div>', unsafe_allow_html=True)

    # ── Already answered this question — show review mode ─────
    if q_idx < len(state["answers"]):
        sc    = state["scores"][q_idx] if q_idx < len(state["scores"]) else None
        score = badge(sc)

        st.markdown(
            f'<div class="ans-box">'
            f'  <div class="ans-label">Your answer {score}</div>'
            f'  <div class="ans-text">{state["answers"][q_idx]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Navigation: Back / Next (or Finish on last question)
        col_back, col_next = st.columns(2)
        with col_back:
            if q_idx > 0:
                if st.button("← Back", use_container_width=True):
                    st.session_state.q_index -= 1
                    st.rerun()
        with col_next:
            if q_idx < total - 1:
                if st.button("Next Question →", use_container_width=True):
                    st.session_state.q_index += 1
                    st.rerun()
            else:
                # Last question answered — generate report
                if st.button("✅  Finish & Get My Report", use_container_width=True):
                    with st.spinner("Generating your personalised report…"):
                        state.update(generate_final_report(state))
                        st.session_state.state = state
                        st.session_state.done  = True
                    st.rerun()

    # ── Not yet answered — show the answer input ──────────────
    else:
        # Friendly hint for first question
        if q_idx == 0:
            st.markdown('<div class="info">💡 Type your answer below and press <strong>Enter</strong> to submit. Take your time!</div>', unsafe_allow_html=True)

        answer = st.chat_input("Type your answer here…")

        if answer:
            with st.spinner("Evaluating your answer…"):
                state["answers"].append(answer)
                state["current_question"] = len(state["answers"])
                state.update(evaluate_answer(state))
                st.session_state.state = state

            # Move to the next unanswered question automatically
            if q_idx + 1 < total:
                st.session_state.q_index = q_idx + 1
            st.rerun()

        # Back button (only shown if not on first question)
        if q_idx > 0:
            if st.button("← Back", use_container_width=False):
                st.session_state.q_index -= 1
                st.rerun()


# ─────────────────────────────────────────────────────────────
# 7. PAGE — REPORT
# ─────────────────────────────────────────────────────────────
def page_report():
    step_bar("report")

    state     = st.session_state.state
    questions = state.get("questions", [])
    answers   = state.get("answers",   [])
    scores    = state.get("scores",    [])
    avg       = round(sum(scores) / len(scores), 1) if scores else 0
    strong    = sum(1 for s in scores if s >= 7)

    # Page header
    st.markdown("""
    <div style="text-align:center;padding:1.25rem 0 1rem">
        <span style="font-size:2.5rem">📋</span>
        <h2 style="font-family:'Sora',sans-serif;font-size:clamp(1.7rem,5vw,2.3rem);
            font-weight:700;color:var(--ink);margin:.3rem 0 .2rem">Your Interview Report</h2>
        <p style="color:var(--ink-soft);font-size:.95rem;margin:0">
            Here's how you did — review each answer and read the AI feedback below.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 3 summary stat cards ──────────────────────────────────
    st.markdown(
        f'<div class="stats">'
        f'  <div class="stat"><div class="stat-lbl">Avg Score</div><div class="stat-num">{avg}<span class="stat-unit">/10</span></div></div>'
        f'  <div class="stat"><div class="stat-lbl">Questions</div><div class="stat-num">{len(questions)}</div></div>'
        f'  <div class="stat"><div class="stat-lbl">Strong (≥7)</div><div class="stat-num">{strong}<span class="stat-unit">/{len(questions)}</span></div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Per-question accordion ────────────────────────────────
    st.markdown('<div class="sec-title">📝 Question Breakdown</div>', unsafe_allow_html=True)

    for i, (q, a) in enumerate(zip(questions, answers)):
        sc = scores[i] if i < len(scores) else None
        label = f"Q{i + 1}  ·  {q[:60]}{'…' if len(q) > 60 else ''}"
        with st.expander(label):
            st.markdown(badge(sc), unsafe_allow_html=True)
            st.markdown(f"**Question:** {q}")
            st.markdown(f"**Your answer:** {a}")

    # ── AI written feedback ───────────────────────────────────
    st.markdown('<div class="sec-title">🤖 AI Feedback</div>', unsafe_allow_html=True)
    if state.get("report"):
        st.markdown(f'<div class="feedback">{state["report"]}</div>', unsafe_allow_html=True)

    # ── Start over button ─────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    if st.button("🔄  Start a New Interview", use_container_width=False):
        st.session_state.clear()
        st.rerun()


# ─────────────────────────────────────────────────────────────
# 8. ROUTER  — decides which page to show
# ─────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "upload":
    page_upload()

elif page == "interview":
    if st.session_state.state is None:   # safety: can't interview without state
        go("upload")
    page_interview()

elif page == "report":
    if st.session_state.state is None:   # safety: can't report without state
        go("upload")
    page_report()