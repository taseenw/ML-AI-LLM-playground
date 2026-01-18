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
