---
inclusion: manual
---

# Python Development Guidelines

## Code Style

- Follow PEP 8 conventions
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable names in English (comments can be in Persian)

## Project Structure

```
project/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
└── requirements.txt
```

## Dependencies

- Use `requirements.txt` for dependencies
- Pin major versions: `requests>=2.31.0,<3.0.0`
- Separate dev dependencies if needed

## Testing

- Use `pytest` for testing
- Test file naming: `test_*.py`
- One test file per module
- Use descriptive test names: `test_should_parse_json_correctly()`

## Error Handling

- Use specific exceptions, not bare `except:`
- Provide meaningful error messages
- Log errors appropriately

## Code Organization

- One class per file (unless tightly coupled)
- Group related functions in modules
- Use `__init__.py` to expose public API

## Documentation

- Use docstrings for all public functions/classes
- Format: Google style or NumPy style
- Include examples for complex functions

## Example

```python
from typing import List, Dict, Optional

def fetch_project_items(project_id: str, limit: int = 100) -> List[Dict]:
    """
    Fetch items from GitHub project.
    
    Args:
        project_id: GitHub project ID
        limit: Maximum number of items to fetch
        
    Returns:
        List of project items as dictionaries
        
    Raises:
        ValueError: If project_id is empty
        RuntimeError: If GitHub CLI fails
    """
    if not project_id:
        raise ValueError("project_id cannot be empty")
    
    # Implementation here
    pass
```

## Common Patterns

### CLI Arguments
```python
import argparse

parser = argparse.ArgumentParser(description='Generate project report')
parser.add_argument('--format', choices=['html', 'md', 'csv'], default='html')
args = parser.parse_args()
```

### JSON Handling
```python
import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### Subprocess for GitHub CLI
```python
import subprocess
import json

result = subprocess.run(
    ['gh', 'project', 'view', '2', '--owner', 'TechBurst-Pro', '--format', 'json'],
    capture_output=True,
    text=True,
    check=True
)
data = json.loads(result.stdout)
```

## Keep It Simple

- Prefer standard library over external dependencies when possible
- Write clear, readable code over clever code
- Don't over-engineer for future requirements
