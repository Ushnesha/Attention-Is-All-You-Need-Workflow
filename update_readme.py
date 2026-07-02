#!/usr/bin/env python3
"""
update_readme.py
Auto-generates and updates README.md with codebase indices, dependencies, and recent commit history.
Can be installed as a git pre-commit hook to automate this process.
"""

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

# --- DEFAULT TEMPLATE ---
DEFAULT_README = """# Attention Is All You Need - Implementation Workflow

A step-by-step educational workflow implementing the core components of the "Attention Is All You Need" Transformer architecture in PyTorch.

---

## 📁 Code Components Index

<!-- START_COMPONENT_INDEX -->
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
<!-- END_DEPENDENCIES -->

---

## 📈 Recent Activity

<!-- START_GIT_HISTORY -->
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
"""


def get_first_line(docstring):
    """Extracts the first non-empty line of a docstring."""
    if not docstring:
        return "*No description provided.*"
    lines = [line.strip() for line in docstring.splitlines() if line.strip()]
    return lines[0] if lines else "*No description provided.*"


def parse_python_code(code_string):
    """Parses a string of Python code using ast and extracts functions/classes."""
    # Filter out notebook magic commands (e.g. %pip, !ls) which are syntax errors in ast.parse
    lines = []
    for line in code_string.splitlines():
        trimmed = line.strip()
        if trimmed.startswith('%') or trimmed.startswith('!'):
            continue
        lines.append(line)
    sanitized_code = "\n".join(lines)
    
    components = {"classes": [], "functions": []}
    try:
        tree = ast.parse(sanitized_code)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                doc = ast.get_docstring(node) or ""
                args = [arg.arg for arg in node.args.args]
                components["functions"].append({
                    "name": func_name,
                    "doc": doc.strip() if doc else "",
                    "args": args
                })
            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                doc = ast.get_docstring(node) or ""
                methods = []
                for subnode in node.body:
                    if isinstance(subnode, ast.FunctionDef):
                        m_name = subnode.name
                        # Skip private methods except __init__
                        if m_name.startswith('_') and m_name != '__init__':
                            continue
                        m_doc = ast.get_docstring(subnode) or ""
                        m_args = [arg.arg for arg in subnode.args.args if arg.arg != 'self']
                        methods.append({
                            "name": m_name,
                            "doc": m_doc.strip() if m_doc else "",
                            "args": m_args
                        })
                components["classes"].append({
                    "name": class_name,
                    "doc": doc.strip() if doc else "",
                    "methods": methods
                })
    except SyntaxError:
        # Ignore files/cells with syntax errors (like incomplete scratch files or complex magic)
        pass
    return components


def parse_notebook_file(file_path):
    """Loads a Jupyter notebook and extracts markdown sections and code structures."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = json.load(f)
    except Exception as e:
        print(f"Error reading notebook {file_path}: {e}")
        return None

    file_components = {"classes": [], "functions": [], "summary": ""}
    markdown_titles = []
    
    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type")
        source = cell.get("source", [])
        source_str = "".join(source) if isinstance(source, list) else str(source)
            
        if cell_type == "markdown":
            # Extract main markdown headers as summary context
            for line in source_str.splitlines():
                if line.strip().startswith("#"):
                    header = re.sub(r'^#+\s*', '', line).strip()
                    # Filter out simple/boring headers
                    if header and not any(w in header.lower() for w in ["test", "import"]):
                        markdown_titles.append(header)
        elif cell_type == "code":
            cell_comps = parse_python_code(source_str)
            file_components["classes"].extend(cell_comps["classes"])
            file_components["functions"].extend(cell_comps["functions"])
            
    if markdown_titles:
        file_components["summary"] = f"Interactive notebook covering: {', '.join(markdown_titles[:3])}"
    else:
        file_components["summary"] = "Jupyter Notebook implementation."
        
    return file_components


def parse_py_file(file_path):
    """Loads a python source file and parses its code structure."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading python file {file_path}: {e}")
        return None
        
    file_components = parse_python_code(code_content)
    
    # Try to extract the module-level docstring
    try:
        tree = ast.parse(code_content)
        module_doc = ast.get_docstring(tree)
        file_components["summary"] = module_doc.strip() if module_doc else "Python source module."
    except Exception:
        file_components["summary"] = "Python source module."
        
    return file_components


def scan_project_files(root_dir):
    """Scans the repository for Python files and Jupyter notebooks to document."""
    root = Path(root_dir)
    scanned_files = {}
    
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        
        # Determine path relative to workspace root
        try:
            rel_path = path.relative_to(root)
        except ValueError:
            continue
            
        parts = rel_path.parts
        # Exclude hidden files, directories, virtual envs, and metadata dirs
        if any(p.startswith('.') for p in parts):
            continue
        if any(p in {'venv', 'env', '.venv', '__pycache__', 'build', 'dist', 'artifacts'} for p in parts):
            continue
        if path.name == "update_readme.py":
            continue
            
        if path.suffix == ".py":
            comps = parse_py_file(path)
            if comps:
                scanned_files[str(rel_path)] = comps
        elif path.suffix == ".ipynb":
            comps = parse_notebook_file(path)
            if comps:
                scanned_files[str(rel_path)] = comps
                
    return scanned_files


def parse_requirements(requirements_path):
    """Parses requirements.txt and extracts packages."""
    if not requirements_path.exists():
        return []
    dependencies = []
    try:
        with open(requirements_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                if "find-links" in line:
                    continue
                dependencies.append(line)
    except Exception as e:
        print(f"Error parsing requirements: {e}")
    return dependencies


def get_git_history():
    """Retrieves the last 5 commits using git log."""
    try:
        res = subprocess.run(
            ["git", "log", "-n", "5", "--oneline"],
            capture_output=True,
            text=True,
            check=True
        )
        commits = res.stdout.strip().splitlines()
        return commits if commits else ["No git commits found."]
    except Exception:
        return ["No git history found or Git is not initialized."]


def generate_component_index(scanned_files):
    """Formats scanned codebase component details into nice Markdown lists."""
    if not scanned_files:
        return "*No code components found yet.*"
        
    lines = []
    # Sort files alphabetically for output consistency
    for file_path, data in sorted(scanned_files.items()):
        lines.append(f"### 📄 [{file_path}]({file_path})")
        lines.append(f"> {data.get('summary', 'No description available.')}")
        lines.append("")
        
        classes = data.get("classes", [])
        functions = data.get("functions", [])
        
        if classes:
            lines.append("**Classes:**")
            for cls in classes:
                lines.append(f"- `class {cls['name']}`: {get_first_line(cls['doc'])}")
                for method in cls.get("methods", []):
                    args_str = ", ".join(method["args"])
                    lines.append(f"  - `def {method['name']}({args_str})`: {get_first_line(method['doc'])}")
            lines.append("")
            
        if functions:
            lines.append("**Functions:**")
            for func in functions:
                args_str = ", ".join(func["args"])
                lines.append(f"- `def {func['name']}({args_str})`: {get_first_line(func['doc'])}")
            lines.append("")
            
        lines.append("---")
        lines.append("")
        
    # Trim the trailing separator
    if lines and lines[-2] == "---":
        lines = lines[:-3]
        
    return "\n".join(lines)


def generate_dependencies_list(dependencies):
    """Formats the list of dependencies into a clean Markdown table."""
    if not dependencies:
        return "*No external dependencies listed.*"
        
    lines = ["| Package | Version Specifier |", "| --- | --- |"]
    for dep in dependencies:
        # Split on common comparison operators to format nicely
        parts = re.split(r'(==|>=|<=|>|<|~=)', dep)
        if len(parts) >= 2:
            pkg = parts[0].strip()
            ver = "".join(parts[1:]).strip()
            lines.append(f"| `{pkg}` | `{ver}` |")
        else:
            lines.append(f"| `{dep}` | `Latest/Any` |")
            
    return "\n".join(lines)


def generate_git_history_list(commits):
    """Formats the list of recent Git commits."""
    lines = []
    for commit in commits:
        # Match hash and message
        match = re.match(r"^([a-f0-9]+)\s+(.*)$", commit)
        if match:
            commit_hash, msg = match.groups()
            lines.append(f"- [`{commit_hash}`](https://github.com/Ushnesha/Attention-Is-All-You-Need-Workflow/commit/{commit_hash}) - {msg}")
        else:
            lines.append(f"- {commit}")
    return "\n".join(lines)


def update_section(content, section_name, new_block):
    """Updates content between specific START and END tags using safe string slicing."""
    start_tag = f"<!-- START_{section_name} -->"
    end_tag = f"<!-- END_{section_name} -->"
    
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        before = content[:start_idx + len(start_tag)]
        after = content[end_idx:]
        return f"{before}\n{new_block}\n{after}"
    else:
        # Tag not found, append at the end of the content safely
        return f"{content}\n\n{start_tag}\n{new_block}\n{end_tag}"


def install_git_hook():
    """Installs the git pre-commit hook."""
    git_dir = Path(".git")
    if not git_dir.exists() or not git_dir.is_dir():
        print("Error: .git directory not found. Run this from the root of a Git repository.")
        sys.exit(1)
        
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    pre_commit_path = hooks_dir / "pre-commit"
    
    hook_content = """#!/bin/sh
# Auto-generated by update_readme.py. Do not edit manually.
echo "Running update_readme.py pre-commit hook..."
python3 update_readme.py
git add README.md
"""
    try:
        with open(pre_commit_path, "w", encoding="utf-8") as f:
            f.write(hook_content)
        # chmod +x on POSIX systems
        pre_commit_path.chmod(pre_commit_path.stat().st_mode | 0o111)
        print(f"Git pre-commit hook successfully installed at {pre_commit_path}")
    except Exception as e:
        print(f"Error installing Git pre-commit hook: {e}")
        sys.exit(1)


def main():
    # Handle CLI args
    if len(sys.argv) > 1 and sys.argv[1] == "--install-hook":
        install_git_hook()
        return

    workspace_root = Path(__file__).resolve().parent
    readme_path = workspace_root / "README.md"
    
    # 1. Read or initialize README.md
    if not readme_path.exists():
        print("README.md not found. Initializing from default template...")
        readme_content = DEFAULT_README
    else:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()

    # 2. Gather data
    scanned_files = scan_project_files(workspace_root)
    dependencies = parse_requirements(workspace_root / "requirements.txt")
    git_commits = get_git_history()

    # 3. Format components
    comp_block = generate_component_index(scanned_files)
    dep_block = generate_dependencies_list(dependencies)
    git_block = generate_git_history_list(git_commits)

    # 4. Inject blocks into tags
    updated_content = update_section(readme_content, "COMPONENT_INDEX", comp_block)
    updated_content = update_section(updated_content, "DEPENDENCIES", dep_block)
    updated_content = update_section(updated_content, "GIT_HISTORY", git_block)

    # 5. Write back to file
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("README.md successfully updated!")


if __name__ == "__main__":
    main()
