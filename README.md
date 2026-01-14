# 🏭 AI Content Factory: Multi-Agent Orchestration 🤖✨

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![LLM](https://img.shields.io/badge/LLM-Llama--3.3--Groq-green.svg)](https://groq.com/)
[![UI](https://img.shields.io/badge/UI-Streamlit--Dark-black.svg)](https://streamlit.io/)

The era of "one-size-fits-all" AI prompts is over. This project demonstrates a **Stateful Assembly Line** approach to content creation, transforming raw PDF data into a complete marketing storyboard and social campaign in seconds.



## 🚀 The Core Concept
Unlike standard chatbots, this system utilizes **LangGraph** to manage a multi-agent workflow. Each agent (node) is a specialist, collaborating in a resilient, state-aware environment.

### 🏗️ Agentic Workflow
1.  **PDF Processor:** Extracts and cleanses raw intelligence from uploaded documents.
2.  **Scriptwriter Node:** Analyzes data to craft a viral-ready 30s video script (Powered by **Llama 3.3 via Groq**).
3.  **Visual Designer Node:** Translates narrative beats into high-fidelity cinematic image prompts.
4.  **Social Strategist Node:** Synthesizes the core message into a high-engagement Twitter/X thread.
5.  **Memory Checkpointer:** A persistent layer ensuring zero data loss during refreshes via `thread_id` management.

## 🛠️ Technical Stack
- **Orchestration:** LangGraph (StateGraph logic)
- **Inference:** Groq Cloud (Llama-3.3-70b-versatile)
- **Image Generation:** Stability AI (Stable Diffusion XL via HF Router)
- **Persistence:** LangGraph Checkpointers & UUID-based session management
- **UI:** Streamlit (Custom Dark-Themed Glassmorphism Dashboard)

---

## 📸 Dashboard Preview
The UI features a professional dark-themed dashboard with persistent project history, allowing users to toggle between multiple active campaigns seamlessly.



---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/AhtishamIjaz/AI-Content-Factory.git](https://github.com/AhtishamIjaz/AI-Content-Factory.git)
cd AI-Content-Factory
