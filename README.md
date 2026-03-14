# 🤖 AI Resume Interviewer

An intelligent interview coach that reads your résumé, extracts your skills, and conducts a personalised technical interview — then gives you a full feedback report with scores and suggestions.

Built with **LangGraph**, **LangChain**, **Groq (LLaMA 3.3)**, and **Streamlit**.

---

## 📸 Demo

| Upload Page | Interview Page | Report Page |
|-------------|----------------|-------------|
| Upload your PDF résumé | Answer one question at a time | See scores + AI feedback |

---

## ✨ Features

- 📄 **PDF résumé parsing** — extracts raw text from any résumé
- 🔍 **Automatic skill extraction** — detects your tech stack using an LLM
- 🎤 **Personalised interview** — generates 10 technical questions based on *your* skills
- 🧠 **Live answer evaluation** — each answer is scored out of 10 by an AI evaluator
- 📊 **Full report** — strengths, weaknesses, and improvement suggestions
- 🌗 **Dark & light mode** — fully adaptive UI
- 📱 **Mobile friendly** — responsive layout for all screen sizes

---

## 🏗️ Project Structure

```
ai-resume-interviewer/
│
├── app.py                        # Streamlit UI — all 3 pages
│
├── graph/
│   ├── interview_graph.py        # LangGraph pipeline definition
│   ├── graph_state.py            # Shared state (TypedDict)
│   ├── current_question_node.py  # Node: serves current question
│   └── next_question_decide_node.py  # Conditional edge: next Q or report
│
├── modules/
│   ├── pdf_loader.py             # Extracts text from uploaded PDF
│   ├── skill_extractor.py        # LLM extracts skills from résumé text
│   ├── question_generator.py     # LLM generates 10 interview questions
│   ├── evaluate_answer.py        # LLM scores each answer out of 10
│   └── final_report.py           # LLM writes the final feedback report
│
├── .env                          # Your API keys (never commit this)
├── requirements.txt
└── README.md
```

---

## 🔄 How It Works (Pipeline)

```
Upload PDF
    ↓
[resume_parser]  →  extract raw text
    ↓
[skill]          →  detect tech skills from text
    ↓
[generate_question] →  create 10 tailored questions
    ↓
[interview]      →  show one question at a time
    ↓
[evaluate]       →  score the answer (0–10)
    ↓
    ├── more questions? → back to [interview]
    └── all done?       → [report] → END
```

This pipeline is built with **LangGraph** — a state machine framework where each box above is a *node* and the arrows are *edges*. The conditional branch after evaluate is a `conditional_edge` that checks if all questions have been answered.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Agentic pipeline / state machine |
| [LangChain](https://python.langchain.com/) | LLM chains and prompt templates |
| [Groq + LLaMA 3.3 70B](https://groq.com/) | Fast LLM inference |
| [Streamlit](https://streamlit.io/) | Web UI |
| [pypdf](https://pypdf.readthedocs.io/) | PDF text extraction |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/arnab06082004/AI_interviewer
cd AI_interviewer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com).

### 4. Run the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📦 Requirements

```txt
streamlit
langchain
langchain-groq
langgraph
pypdf
python-dotenv
```

---

## 📁 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key for LLaMA 3.3 inference |

---

## 🗺️ How the LangGraph State Works

All data flows through a single shared `state` dictionary defined in `graph_state.py`:

```python
class state(TypedDict):
    resume_file:      UploadedFile   # the uploaded PDF
    resume_text:      str            # extracted plain text
    skills:           List[str]      # detected skills
    questions:        List[str]      # generated interview questions
    question:         str            # current question being shown
    current_question: int            # index tracker
    answers:          List[str]      # candidate's answers
    scores:           List[int]      # per-answer scores (0–10)
    report:           str            # final AI feedback report
```

Every node receives this state, does its job, and returns only the keys it changed.

---

## 🔮 Future Improvements

- [ ] **Structured outputs** — use Pydantic models so scores are always valid integers
- [ ] **Critic agent** — add a second LLM to review and validate scores (true multi-agent)
- [ ] **Difficulty adjustment** — adapt question hardness based on live scores
- [ ] **Session persistence** — save interviews to a database so users can resume
- [ ] **Voice mode** — answer questions by speaking using Whisper
- [ ] **Export report** — download the final report as a PDF

---

## 🙋 FAQ

**Q: Which LLM is used?**  
LLaMA 3.3 70B running on Groq's ultra-fast inference API. You can swap it for any LangChain-compatible model by changing the `ChatGroq` initialisation in each module.

**Q: Is my résumé stored anywhere?**  
No. Everything runs in-memory during your Streamlit session. Nothing is saved to disk or sent anywhere except the Groq API for processing.

**Q: Can I use OpenAI instead of Groq?**  
Yes. Replace `ChatGroq` with `ChatOpenAI` from `langchain_openai` and set your `OPENAI_API_KEY`.

---

## 👨‍💻 Author

Built by **[Your Name]** — AI Engineer  
[GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile)

---

## 📄 License

MIT License — free to use, modify, and distribute.