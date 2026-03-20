<div align="center">

# Agentic AI — Minimal ReAct Agent From First Principles

**A grounded Reason–Act–Observe agent built entirely from scratch in Python**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-Llama%203.3%2070B-6366f1?style=flat)
![Inference](https://img.shields.io/badge/Inference-Groq-f97316?style=flat)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat)
![Frameworks](https://img.shields.io/badge/Frameworks-Zero-ef4444?style=flat)

*No LangChain. No AutoGen. No CrewAI. No wrappers. Pure architecture.*

</div>

-----

## 📋 Table of Contents

- [What This Is](#-what-this-is)
- [The ReAct Loop](#-the-react-loop)
- [Repository Structure](#-repository-structure)
- [Core Components](#-core-components)
- [Example Agent Trace](#-example-agent-trace)
- [Getting Started](#-getting-started)
- [Design Philosophy](#-design-philosophy)
- [Roadmap](#-roadmap)
- [Research Context](#-research-context)

-----

## 🧠 What This Is

This repository implements the **ReAct (Reason + Act)** pattern — the foundational architecture behind modern AI agents — built from scratch at the primitive level.

Every component is written manually:

- Iterative reasoning loop
- Tool execution layer
- Structured output parsing
- Working memory (state accumulation)
- Tool grounding enforcement
- Policy constraint control
- Error handling and loop safeguards

**The goal:** move from *LLM user* to *intelligence systems engineer*.

-----

## 🔄 The ReAct Loop

```
┌─────────────────────────────────────────────────────────┐
│                      Question in                        │
└───────────────────────────┬─────────────────────────────┘
                            ▼
                    ┌───────────────┐
                    │  1. THOUGHT   │  LLM reasons about what to do
                    │  (Reasoning)  │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │   2. ACT      │  Parser extracts (tool, input)
                    │  (Action)     │  Grounding enforcer validates
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │  3. OBSERVE   │  Tool executes → returns result
                    │ (Observation) │  Appended to state memory
                    └───────┬───────┘
                            ▼
              ┌─────────────────────────────┐
              │  Goal reached?              │
              │  finish() after tool use?   │
              └──────┬──────────────────────┘
                     │ No                  │ Yes
                     ▼                     ▼
             Back to THOUGHT         Answer out
```

Each iteration: **Thought → Action → Observation → Memory update → repeat**

-----

## 📁 Repository Structure

```
Agentic-AI/
│
├── main.py               # Entry point — agent execution controller
├── requirements.txt      # Dependencies
├── pyproject.toml        # Project metadata
├── .python-version       # Python version pin
├── .gitignore
│
└── Agentic/              # Core agent architecture
    ├── llm.py            # LLM interface (Groq + Llama 3.3 70B)
    ├── tools.py          # Tool registry + Wikipedia implementation
    ├── parser.py         # Structured output parser
    ├── memory.py         # State memory and prompt builder
    ├── grounding.py      # Tool-before-finish enforcement
    └── controller.py     # Execution loop + iteration safeguards
```

-----

## ⚙️ Core Components

### 1. LLM Interface

Wraps the Groq API for inference with Llama 3.3 70B. Handles prompt construction, response parsing, and API error management.

### 2. Tool Registry

A dictionary of named callable functions. Adding a new tool is one line:

```python
registry.register("search_wikipedia", wikipedia_search)
registry.register("calculator", calc_fn)
# Any callable works — the parser routes to it dynamically
```

### 3. Parser Layer

Extracts structured `(action, tool_input)` pairs from raw LLM text. Handles malformed outputs gracefully.

### 4. State Memory

Accumulates `(thought, action, observation)` tuples across iterations. Rebuilds the full trace as a prompt for each LLM call — giving the model its full reasoning history.

```python
class StateMemory:
    def add(self, thought_action, observation):
        self.steps.append((thought_action, observation))

    def build_prompt(self):
        return format_trace(self.question, self.steps)
```

### 5. Execution Controller

Runs the loop with configurable iteration limits. Terminates cleanly when `finish()` is called or the limit is reached.

### 6. Grounding Enforcer

The agent **cannot call `finish()` without first using at least one tool**. This is enforced explicitly — the LLM cannot hallucinate a confident answer without evidence.

```python
if action == "finish" and not grounding.has_used_tool():
    memory.add_constraint_violation()
    continue   # force another tool call
```

-----

## 🔍 Example Agent Trace

```
Question: Who invented the telephone?

Thought:  I need to find accurate information about the telephone's invention.
          I should search Wikipedia.

Action:   search_wikipedia("invention of the telephone")

Observe:  Alexander Graham Bell was awarded the first patent for the telephone
          in 1876. He is widely credited as the inventor...

Thought:  I have a sourced, grounded answer. Bell received the patent in 1876.
          I can now call finish().

Action:   finish("Alexander Graham Bell invented the telephone,
                  receiving the first US patent in 1876.")

→ Agent terminated. Answer grounded in Wikipedia source.
```

-----

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com) (free tier available)

### Installation

```bash
git clone https://github.com/asfandyar-prog/Agentic-Ai.git
cd Agentic-Ai
pip install -r requirements.txt
```

### Configuration

```bash
# Create a .env file
echo "GROQ_API_KEY=your_key_here" > .env
```

### Run the agent

```bash
python main.py
```

-----

## 🏗 Design Philosophy

This project intentionally avoids high-level frameworks in order to:

|Goal                                    |Why it matters                                                        |
|----------------------------------------|----------------------------------------------------------------------|
|**Build first-principles understanding**|Frameworks abstract the loop — understanding requires seeing inside it|
|**Control reasoning explicitly**        |Every decision in the loop is visible and modifiable                  |
|**Debug cognition directly**            |Failure modes are observable without framework noise                  |
|**Study agent failure modes**           |Repetition, hallucination, grounding failures — all exposed           |
|**Engineer robust grounding**           |Grounding constraints are hard-coded, not suggested                   |


> *Architectural clarity before abstraction.*

-----

## 📌 Roadmap

- [x] Multi-step reasoning loop
- [x] Wikipedia API grounding (with 403 prevention headers)
- [x] Strict action validation
- [x] Tool-before-finish grounding enforcement
- [x] Iteration limit safeguards
- [x] Class-based modular design
- [ ] Repetition detection guard
- [ ] Improved structured memory abstraction
- [ ] Planning layer (Tree-of-Thought style)
- [ ] Multi-tool support (calculator, web search, code executor)
- [ ] Benchmark evaluation suite
- [ ] Autonomous experiment execution agent

-----

## 📚 Research Context

This implementation is inspired by:

- **ReAct: Synergizing Reasoning and Acting in Language Models** — Yao et al., ICLR 2023
- Tool-augmented LLM systems
- Grounded reasoning architectures
- Robustness under distribution shift

The long-term direction is integrating agentic control with **research automation** and **adaptive learning systems** — an agent that can design, run, and interpret experiments with verifiable, grounded reasoning.

-----

## 👤 Author

**Asfand Yar** · BSc Computer Science
Focus: agentic AI · self-supervised learning · vision transformers · robustness under distribution shift

-----

<div align="center">

MIT License · [asfandyar-prog](https://github.com/asfandyar-prog)

</div>
