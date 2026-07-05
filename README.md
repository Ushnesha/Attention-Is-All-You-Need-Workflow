# Attention Is All You Need - Implementation Workflow

A step-by-step educational workflow implementing the core components of the "Attention Is All You Need" Transformer architecture in PyTorch.

---

## 📁 Code Components Index

<!-- START_COMPONENT_INDEX -->
### 📄 [multi_head_attention_implementation.ipynb](multi_head_attention_implementation.ipynb)
> Jupyter Notebook implementation.

**Classes:**
- `class MultiHeadAttention`: *No description provided.*
  - `def scaled_dot_product_attention(Q, K, V, mask)`: Args:
  - `def forward(query, key, value, mask)`: Args:

---

### 📄 [single_head_attention_implementation.ipynb](single_head_attention_implementation.ipynb)
> Interactive notebook covering: Implementing Scaled Dot-Product Attention: $softmax(\frac{QK^T}{\sqrt d_k})V$

**Functions:**
- `def scaled_dot_product_attention(query, key, value, mask)`: Computes Scaled Dot-Product Attention.

---

### 📄 [sinusoidal_positional_embedding_implementation.ipynb](sinusoidal_positional_embedding_implementation.ipynb)
> Interactive notebook covering: Implementing the Positional Encoding Function, Visualization

**Functions:**
- `def get_positional_encoding(max_seq_len, d_model)`: *No description provided.*
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

## 🔄 Automatic Documentation Sync

This repository uses an automatic documentation sync workflow. The `README.md` is updated dynamically whenever code changes are committed.

To manually refresh the documentation, run:
```bash
python3 update_readme.py
```

To install the git hook automatically:
```bash
python3 update_readme.py --install-hook
```
