# Attention Is All You Need - Implementation Workflow

A step-by-step educational workflow implementing the core components of the "Attention Is All You Need" Transformer architecture in PyTorch.

---

## 📁 Code Components Index

<!-- START_COMPONENT_INDEX -->
### 📄 [QKV_attention_implementation.ipynb](QKV_attention_implementation.ipynb)
> Interactive notebook covering: Implementing Scaled Dot-Product Attention: $softmax(\frac{QK^T}{\sqrt d_k})V$

**Functions:**
- `def scaled_dot_product_attention(query, key, value, mask)`: Computes Scaled Dot-Product Attention.
<!-- END_COMPONENT_INDEX -->

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ushnesha/Attention-Is-All-You-Need-Workflow.git
   cd Attention-Is-All-You-Need-Workflow
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📦 Dependencies

<!-- START_DEPENDENCIES -->
| Package | Version Specifier |
| --- | --- |
| `pandas` | `==2.3.3` |
| `torch` | `==2.3.0` |
| `torchdata` | `==0.8.0` |
| `torchtext` | `==0.18.0` |
| `spacy` | `==3.8.14` |
| `altair` | `==6.0.0` |
| `jupytext` | `==1.19.3` |
| `flake8` | `==7.3.0` |
| `black` | `==26.5.1` |
| `GPUtil` | `==1.4.0` |
| `wandb` | `==0.27.2` |
<!-- END_DEPENDENCIES -->

---

## 📈 Recent Activity

<!-- START_GIT_HISTORY -->
- [`b2315f2`](https://github.com/Ushnesha/Attention-Is-All-You-Need-Workflow/commit/b2315f2) - added simple qkv implementation
<!-- END_GIT_HISTORY -->

---

## 🔄 Automatic Documentation Sync

This repository uses an automatic documentation sync workflow. The `README.md` is updated dynamically whenever code changes are committed.

### How it works:
- A Git `pre-commit` hook triggers the `update_readme.py` script before every commit.
- The script scans the codebase, extracts class/function signatures & docstrings, reads `requirements.txt`, fetches recent Git history, and updates the marked blocks in this file.
- The updated `README.md` is automatically staged and included in the commit.

To manually refresh the documentation, run:
```bash
python3 update_readme.py
```

To install the git hook automatically:
```bash
python3 update_readme.py --install-hook
```
