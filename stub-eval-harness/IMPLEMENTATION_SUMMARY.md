# Eval Runner Implementation Summary

## Project Overview

A Python CLI tool for running LLM evaluations. This is a stub/baseline project with a dummy model for learning purposes. Uses Typer for CLI and follows Python packaging best practices.

## Repository Structure

```
stub-eval-harness/
├── pyproject.toml          # Package configuration and dependencies
├── eval-run                 # Executable wrapper script (no .py extension)
├── .gitignore              # Git ignore rules
├── configs/
│   └── config.yaml         # Configuration file (TODO: implement loading)
├── data/
│   └── prompts.jsonl       # Input dataset (JSONL format)
├── outputs/
│   └── results.jsonl       # Generated results (JSONL format)
├── src/
│   └── eval_runner/        # Main package
│       ├── __init__.py     # Package initialization
│       └── cli.py          # CLI implementation
└── tests/
    ├── __init__.py
    └── test_cli.py         # Simple pytest tests
```

## Implementation Details

### 1. Package Configuration (`pyproject.toml`)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "eval-runner"
version = "0.1.0"
dependencies = [
    "typer>=0.9.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
]

# No entry point - using wrapper script instead (eval-run in repo root)

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

### 2. CLI Wrapper Script (`eval-run`)

```python
#!/usr/bin/env python3
"""Simple wrapper to run eval-run command"""
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the app
from eval_runner.cli import app

if __name__ == "__main__":
    app()
```

**Usage:** `./eval-run --config configs/config.yaml`

### 3. Main CLI Implementation (`src/eval_runner/cli.py`)

```python
import json
import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def eval_run(
    config: str = typer.Option(..., "--config", help="Path to config file"),
):
    """Run evaluation with the given config file."""
    print(f"Running eval with config: {config}")
    # read in file from data/prompts.jsonl its a id, prompt pair
    with open("data/prompts.jsonl", "r") as f:
        prompts = [json.loads(line) for line in f]
    
    output_dict = {}
    for prompt in prompts:
        response = dummyAIPass(prompt)
        output_dict[prompt["id"]] = response

    # write to file in outputs/results.jsonl
    with open("outputs/results.jsonl", "w") as f:
        for id, response in output_dict.items():
            f.write(json.dumps({"id": id, "response": response}) + "\n")

# Just sends req and return
def dummyAIPass(prompt_object: dict):
    # dummy response for id #
    response = "dummy response for prompt with id: " + prompt_object["id"]

    return response
```

### 4. Tests (`tests/test_cli.py`)

```python
"""Simple tests for the eval_runner CLI functionality."""
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from eval_runner.cli import dummyAIPass


def test_dummy_ai_pass_returns_response_with_id():
    """Test that dummyAIPass returns a response containing the prompt ID."""
    prompt = {"id": "42", "prompt": "Test prompt"}
    response = dummyAIPass(prompt)
    
    assert "42" in response
    assert response == "dummy response for prompt with id: 42"


def test_output_format():
    """Test that output has correct JSON structure."""
    prompt = {"id": "1", "prompt": "Test"}
    response = dummyAIPass(prompt)
    
    output = {"id": prompt["id"], "response": response}
    
    # Verify structure
    assert "id" in output
    assert "response" in output
    assert isinstance(output["id"], str)
    assert isinstance(output["response"], str)
```

### 5. Configuration File (`configs/config.yaml`)

```yaml
dataset_path: data/prompts.jsonl
output_path: outputs/results.jsonl
```

### 6. Sample Dataset (`data/prompts.jsonl`)

```json
{"id":"1","prompt":"Return JSON with keys name and age for Alice age 20."}
{"id":"2","prompt":"Summarize in 1 sentence: The sky is blue because of Rayleigh scattering."}
{"id":"3","prompt":"Extract tags as a JSON list: 'I love basketball and lifting'."}
```

### 7. Sample Output (`outputs/results.jsonl`)

```json
{"id": "1", "response": "dummy response for prompt with id: 1"}
{"id": "2", "response": "dummy response for prompt with id: 2"}
{"id": "3", "response": "dummy response for prompt with id: 3"}
```

## How to Run

### Run the CLI

```bash
cd stub-eval-harness
./eval-run --config configs/config.yaml
```

### Run Tests

```bash
cd stub-eval-harness
python3 -m pytest tests/ -v
```

## Current Status

| Feature | Status |
|---------|--------|
| CLI with `--config` option | ✅ Working |
| JSONL dataset reading | ✅ Working |
| JSONL output writing | ✅ Working |
| Stub model function | ✅ Working |
| Tests | ✅ 2 tests passing |
| Config file loading | ⚠️ TODO (config accepted but not used yet) |

## Next Steps

1. **Implement config loading** — Use pyyaml to load `config.yaml` and use `dataset_path` and `output_path` instead of hardcoded paths
2. **Add logging** — Add progress logging during evaluation
3. **Add timing** — Track latency per prompt

## Dependencies

- `typer>=0.9.0` — CLI framework
- `pyyaml>=6.0` — YAML config parsing (declared, ready to use)
- `pytest>=7.0.0` — Testing (dev dependency)

## Design Decisions

1. **Wrapper script instead of entry point** — Avoids `.egg-info` clutter, simpler for development
2. **`src/` layout** — Industry standard for Python packages
3. **Simple tests** — Minimal tests that cover core functionality without over-engineering
4. **JSONL format** — Standard for ML datasets, one JSON object per line
