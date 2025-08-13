# Math Tutor with Step-by-Step Reasoning

**Proof-of-concept AI math tutor** that solves problems in algebra, calculus, and discrete mathematics with **verified, step-by-step solutions** using a local large language model and a computer algebra system.

---

## Problem Statement

Build a math tutoring agent that:

* Solves problems in algebra, calculus, and discrete math.
* Provides a **full, verified chain of reasoning**.
* Uses **SymPy** to validate each step.
* Outputs **professional LaTeX-formatted solutions**.
* Suggests **related practice problems**.

---

## Key Features

* **Multi-topic support**: Algebra, Calculus, Discrete Math.
* **Step-by-step reasoning**: From problem to final answer.
* **Symbolic verification**: Every step checked with SymPy.
* **Dual output**: Raw internal reasoning + user-friendly explanation.
* **LaTeX formatting**: Clear, professional presentation (PDF/HTML).
* **Practice generator**: Creates similar problems for practice.
* **Local inference**: All processing runs on your machine.

---

## Workflow

1. **Input** (CLI or Web): User submits a problem.
2. **Step Generation** (LLM): Local GPT-OSS-20B breaks it into steps (JSON format).
3. **Verification** (SymPy): Each step validated for correctness.
4. **Explanation**: Verified steps converted into polished explanation.
5. **Rendering**: Final solution formatted in LaTeX.
6. **Practice Problems**: Similar questions suggested.
7. **Output**: PDF/HTML solution + practice list.

---

## Technology Stack

* **Language Model**: GPT-OSS-20B (local)
* **Math Engine**: SymPy
* **Backend**: Python 3.9+
* **Web Framework**: Flask / FastAPI
* **LaTeX Renderer**: PyLaTeX / pdflatex
* **Dependencies**: `transformers`, `torch`, `sympy`, `flask`

---

## Setup

**Prerequisites**

* Python 3.9+
* Local LaTeX distribution (MiKTeX / TeX Live)
* GPU for LLM inference

**Installation**

```bash
git clone https://github.com/amar-at-iitm/math_tutor
cd math_tutor
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Model Setup**

* Download GPT-OSS-20B weights into `models/`
* Update `config.py` with the model path

---

## Usage

**CLI**

```bash
python tutor.py --problem "Solve x**2 + 5*x + 6 = 0"
```

**Web**

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

---

## Structure

```
math_tutor/
├── agent/                  # Core modules (step gen, verify, render, practice)
├── data/                   # Demo problems
├── models/                 # Local LLM weights
├── templates/              # Web HTML
├── app.py                  # Web entry point
├── tutor.py                # CLI entry point
└── requirements.txt        # Dependencies
```

---

## Milestones

* [x] Load GPT-OSS-20B + SymPy integration
* [x] JSON schema for reasoning steps
* [ ] Verification module for incorrect steps
* [ ] LaTeX export + practice generator
* [ ] Evaluate on 50 problems
