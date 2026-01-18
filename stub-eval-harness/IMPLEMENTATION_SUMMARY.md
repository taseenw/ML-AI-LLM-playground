# Eval Runner Implementation Summary

## Project Overview
A Python CLI tool for running LLM evaluations with a clean, industry-standard structure. The project uses Typer for CLI, follows proper package structure, and implements a baseline evaluation runner with stub model responses.

## Repository Structure

```
stub-eval-harness/
├── pyproject.toml          # Package configuration and dependencies
├── eval-run                # Executable wrapper script
├── .gitignore              # Git ignore rules
├── configs/
│   └── config.yaml         # Configuration file
├── data/
│   └── prompts.jsonl       # Input dataset (JSONL format)
├── outputs/
│   └── results.jsonl       # Generated results (JSONL format)
├── src/
│   └── eval_runner/         # Main package
│       ├── __init__.py     # Package initialization
│       └── cli.py          # CLI implementation
└── tests/                  # Test directory (to be implemented)
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

# No entry point - using wrapper script instead (eval-run in repo root)

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

**Key Points:**
- Uses modern `pyproject.toml` for package configuration
- Defines dependencies (typer for CLI, pyyaml for config loading)
- Configured for `src/` layout (industry standard)
- Uses wrapper script approach instead of entry points to avoid `.egg-info` clutter

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

**Key Points:**
- Executable script (no `.py` extension for cleaner command interface)
- Uses shebang (`#!/usr/bin/env python3`) to run with Python
- Dynamically adds `src/` to Python path for imports
- Imports and executes the Typer app

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

**Key Points:**
- Uses Typer for CLI framework
- `eval_run()` function accepts `--config` option (required)
- Reads JSONL dataset from `data/prompts.jsonl`
- Processes each prompt through `dummyAIPass()` stub function
- Writes results to `outputs/results.jsonl` in JSONL format
- Output format: `{"id": "...", "response": "..."}`

**Current Status:**
- ✅ CLI command working
- ✅ JSONL reading implemented
- ✅ JSONL writing implemented
- ✅ Stub model function implemented
- ⚠️ Config file loading not yet implemented (hardcoded paths)
- ⚠️ Config validation not yet implemented
- ⚠️ Tests not yet implemented

### 4. Package Initialization (`src/eval_runner/__init__.py`)

```python
# This file makes eval_runner a Python package
```

**Key Points:**
- Empty `__init__.py` makes the directory a Python package
- Allows imports like `from eval_runner.cli import app`

### 5. Configuration File (`configs/config.yaml`)

```yaml
dataset_path: data/prompts.jsonl
output_path: outputs/results.jsonl
```

**Key Points:**
- YAML format for human-readable config
- Defines input dataset path
- Defines output results path
- Currently not being used (paths are hardcoded in CLI)

### 6. Sample Dataset (`data/prompts.jsonl`)

```json
{"id":"1","prompt":"Return JSON with keys name and age for Alice age 20."}
{"id":"2","prompt":"Summarize in 1 sentence: The sky is blue because of Rayleigh scattering."}
{"id":"3","prompt":"Extract tags as a JSON list: 'I love basketball and lifting'."}
```

**Key Points:**
- JSONL format (one JSON object per line)
- Each line has `id` and `prompt` fields
- 3 sample prompts included

### 7. Sample Output (`outputs/results.jsonl`)

```json
{"id": "1", "response": "dummy response for prompt with id: 1"}
{"id": "2", "response": "dummy response for prompt with id: 2"}
{"id": "3", "response": "dummy response for prompt with id: 3"}
```

**Key Points:**
- JSONL format matching input structure
- Each line has `id` and `response` fields
- Generated by stub model function

## How It Works

### Execution Flow

1. **User runs command:**
   ```bash
   ./eval-run --config configs/config.yaml
   ```

2. **Wrapper script (`eval-run`):**
   - Adds `src/` to Python path
   - Imports `eval_runner.cli.app`
   - Calls `app()` which starts Typer

3. **Typer CLI (`cli.py`):**
   - Parses `--config` argument
   - Calls `eval_run(config="configs/config.yaml")`
   - Currently ignores config file (hardcoded paths)

4. **Evaluation loop:**
   - Reads `data/prompts.jsonl`
   - For each prompt, calls `dummyAIPass()`
   - Collects responses in dictionary

5. **Output writing:**
   - Writes results to `outputs/results.jsonl`
   - One JSON line per prompt with `id` and `response`

## Design Decisions

### Why wrapper script instead of entry points?
- Avoids `.egg-info` directory clutter
- No need for `pip install -e .`
- Simpler for development
- Still provides clean command interface

### Why `src/` layout?
- Industry standard for Python packages
- Separates source code from other files
- Makes package structure clear
- Easier to test and maintain

### Why Typer?
- Modern CLI framework (built on Click)
- Type hints support
- Automatic help generation
- Clean, Pythonic API

## Next Steps (To Complete Requirements)

1. **Config Loading:**
   - Load YAML config file using `pyyaml`
   - Extract `dataset_path` and `output_path`
   - Use config values instead of hardcoded paths
   - Add validation for required fields

2. **Config Dataclass:**
   - Create `RunConfig` dataclass
   - Validate required fields
   - Add model settings (provider, temperature, max_tokens)

3. **Dataset Loader:**
   - Create `load_dataset()` function
   - Create `Example` dataclass
   - Add error handling for invalid JSON/missing fields

4. **Runner Improvements:**
   - Add timing/latency tracking
   - Add progress logging
   - Implement proper model interface

5. **Logging:**
   - Add logging for run start
   - Log dataset item count
   - Log progress updates
   - Log output location

6. **Tests:**
   - Config loader tests
   - Dataset loader tests
   - Runner tests
   - Use pytest framework

## Usage Examples

```bash
# Run evaluation
./eval-run --config configs/config.yaml

# Show help
./eval-run --help
```

## Dependencies

- `typer>=0.9.0` - CLI framework
- `pyyaml>=6.0` - YAML config parsing (declared but not yet used)

## File Sizes & Line Counts

- `cli.py`: 32 lines
- `eval-run`: 14 lines
- `pyproject.toml`: 20 lines
- `config.yaml`: 2 lines
- `prompts.jsonl`: 3 lines
- `results.jsonl`: 4 lines (generated)

## Notes

- All code follows Python best practices
- Uses type hints where appropriate
- Clean separation of concerns
- Ready for extension with real model integration
- Structure supports testing and maintainability
