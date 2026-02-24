# Agentic-AI

## Minimal ReAct Agent From First Principles

This repository implements a grounded **Reason–Act–Observe (ReAct)** agent architecture built entirely from scratch in Python.

The purpose of this project is to understand and engineer agentic AI systems at the architectural level — without relying on high-level orchestration frameworks such as LangChain, LangGraph, CrewAI, or AutoGen.

This is not a demo wrapper.  
This is a first-principles intelligence system.

---

## 🚀 Motivation

Modern agent frameworks abstract away the core intelligence loop.

This project focuses on implementing the primitive components manually:

- Iterative reasoning loop
- Tool execution layer
- Structured output parsing
- Working memory (state accumulation)
- Tool grounding enforcement
- Policy constraint control
- Error handling and loop safeguards

The goal is to move from “LLM user” to **intelligence systems engineer**.

---

### Core Components

- **LLM Interface** (Groq + Llama 3.3 70B)
- **Tool Registry**
- **Parser Layer**
- **State Memory**
- **Execution Controller**
- **Grounding Enforcement Logic**

---

## ⚙️ Current Capabilities

- Multi-step reasoning
- Wikipedia API grounding
- Strict action validation
- Tool-before-finish enforcement
- Iteration limit safeguards
- HTTP error handling (403 prevention with headers)
- Class-based modular design
- Scalable tool registry architecture

---


## 🔧 Technologies Used

- Python
- Groq API (Llama 3.3 70B)
- Wikipedia API
- Requests
- python-dotenv

---

## 🛠 Example Agent Flow

1. Agent receives a question.
2. Generates a reasoning step (`Thought`).
3. Chooses an action (`search_wikipedia` or `finish`).
4. Executes the tool.
5. Receives observation.
6. Updates internal memory.
7. Repeats until termination conditions are satisfied.

---

## 🔍 Design Philosophy

This project intentionally avoids high-level frameworks to:

- Build first-principles understanding
- Control reasoning explicitly
- Debug cognition behavior directly
- Study failure modes of agent systems
- Engineer robust grounding mechanisms

The objective is architectural clarity before abstraction.

---

## 📌 Roadmap

- [ ] Repetition detection guard
- [ ] Improved structured memory abstraction
- [ ] Planning layer (Tree-of-Thought style)
- [ ] Multi-tool support
- [ ] Benchmark evaluation suite
- [ ] Autonomous experiment execution agent

---

## 📚 Research Context

This implementation is inspired by:

- **ReAct: Synergizing Reasoning and Acting in Language Models (ICLR 2023)**
- Tool-augmented LLM systems
- Grounded reasoning architectures
- Robustness under distribution shift

The long-term direction is integrating agentic control with research automation and adaptive learning systems.

---

## 👤 Author

**Asfand Yar**  
BSc Computer Science
Focused on agentic AI, self-supervised learning, vision transformers, and robustness under distribution shift.

---

## 📜 License

MIT License

