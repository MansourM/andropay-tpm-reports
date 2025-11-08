# Design Document

## Overview

The GitHub Projects HTML Reporter is a Python-based command-line tool that generates beautiful, self-contained HTML reports with Persian (RTL) language support. The tool fetches data from GitHub Projects using the GitHub CLI, processes it, and generates interactive reports with charts and visualizations.

### Key Design Goals

1. **Simplicity**: Easy to use with sensible defaults
2. **Cross-platform**: Works on Windows, macOS, and Linux
3. **Self-contained**: Single HTML file with no external dependencies
4. **Persian-first**: RTL layout and Persian language throughout
5. **Visual**: Rich charts and color-coded metrics
6. **Extensible**: Clean architecture for future Laravel migration

---

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   CLI Entry     │
│   (main.py)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Fetcher   │ ──► GitHub CLI (subprocess)
│  (fetcher.py)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Processor  │
│ (processor.py)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Report Builder  │
│ (builder.py)    │
└────────┬────────┘
         │
         ├──► HTML Renderer (html_renderer.py)
         ├──► Markdown Renderer (md_renderer.py)
         ├──► CSV Renderer (csv_renderer.py)
         └──► JSON Renderer (json_renderer.py)
```

### Module Structure

```
github-reporter/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration management
│   ├── fetcher.py           # GitHub data fetching
│   ├── processor.py         # Data processing and analysis
│   ├── models.py            # Data models
│   ├── snapshot.py          # Weekly snapshot management
│   ├── renderers/
│   │   ├── __init__.py
│   │   ├── base.py          # Base renderer class
│   │   ├── html_renderer.py # HTML report generation
│   │   ├── md_renderer.py   # Markdown generation
│   │   ├── csv_renderer.py  # CSV export
│   │   └── json_renderer.py # JSON export
│   ├── charts/
│   │   ├── __init__.py
│   │   └── chart_builder.py # Chart generation
│   └── templates/
│       └── report.html      # Jinja2 HTML template
├── tests/
│   ├── test_fetcher.py
│   ├── test_processor.py
│   └── test_renderers.py
├── snapshots/               # Weekly snapshots (created at runtime)
├── reports/                 # Generated reports (created at runtime)
├── config.json              # User configuration (optional)
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Components and Interfaces

### 1. CLI Entry Point (main.py)

**Purpose**: Parse command-line arguments and orchestrate the report generation process.

**Key Functions**:
- Parse CLI arguments
- Load configuration
- Validate dependencies (GitHub CLI)
- Orchestrate data fetching, processing, and rendering
- Handle top-level errors

---

### 2. Configuration Management (config.py)

**Purpose**: Load and manage configuration from file and CLI arguments.

**Configuration Schema** (config.json):
```json
{
  "owner": "TechBurst-Pro",
  "project_number": 2,
  "default_format": "html",
  "output_directory": "reports"
}
```

---

### 3. Data Fetcher (fetcher.py)

**Purpose**: Fetch data from GitHub Projects using GitHub CLI.

**Key Methods**:
- `fetch_project_details()` - Get project metadata
- `fetch_project_items()` - Get all items (limit 100)
- `fetch_project_fields()` - Get field definitions
- `_run_gh_command()` - Execute gh CLI commands

**Error Handling**:
- Detect if gh CLI is not installed
- Handle authentication errors
- Validate JSON responses

---

### 4. Data Models (models.py)

**Purpose**: Define data structures for type safety.

**Key Models**:
- `Priority` - Enum for P🔥, P0, P1, P2
- `Status` - Enum for workflow states
- `ProjectItem` - Individual task/issue
- `ProjectData` - Complete project snapshot
- `ProcessedData` - Analyzed data with metrics



---

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class Priority(Enum):
    FIRE = "P🔥"  # Unplanned
    P0 = "P0"     # Critical
    P1 = "P1"     # High
    P2 = "P2"     # Medium

class Status(Enum):
    BACKLOG = "Backlog"
    TODO = "Todo"
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    IN_REVIEW = "In Review"
    DONE = "Done"

@dataclass
class ProjectItem:
    id: str
    title: str
    status: Status
    priority: Priority
    assignees: List[str]
    estimate_hours: Optional[float]
    labels: List[str]
    url: str
    
    @property
    def is_planned(self) -> bool:
        return self.priority != Priority.FIRE
    
    @property
    def is_active(self) -> bool:
        return self.status != Status.DONE

@dataclass
class ProjectMetrics:
    total_items: int
    total_estimate_hours: float
    completion_percentage: float
    planned_count: int
    unplanned_count: int
    unplanned_percentage: float
    high_priority_not_started: int
    items_by_status: dict
    items_by_priority: dict
    items_by_assignee: dict
```

---

## Data Processing (processor.py)

### Processing Pipeline

1. **Parse Raw Data**: Convert JSON to data models
2. **Calculate Metrics**: Compute all statistics
3. **Classify Items**: Planned vs Unplanned
4. **Group Data**: By status, priority, assignee
5. **Compare Snapshots**: Week-over-week changes (if available)

### Key Calculations

**Completion Percentage**:
```python
completion_percentage = (done_items / total_items) * 100
```

**Unplanned Percentage**:
```python
unplanned_percentage = (fire_priority_items / total_items) * 100
```

**Color Coding Logic**:
```python
def get_metric_color(value: float, thresholds: dict) -> str:
    if value >= thresholds['good']:
        return 'green'
    elif value <= thresholds['bad']:
        return 'red'
    else:
        return 'yellow'
```

---

## Chart Generation (charts/chart_builder.py)

### Chart Library Choice

**Plotly.js** - Selected for:
- Interactive charts
- RTL support
- Offline mode (can be embedded)
- Professional appearance
- Touch-friendly

### Chart Types

1. **Status Distribution**
   - Type: Pie chart + Bar chart
   - Data: Count per status
   - Colors: Distinct per status

2. **Priority Distribution**
   - Type: Horizontal bar chart
   - Data: Active items by priority
   - Colors: Red (P🔥), Orange (P0), Yellow (P1), Blue (P2)

3. **Planned vs Unplanned**
   - Type: Pie chart
   - Data: Planned vs Unplanned ratio
   - Colors: Green (Planned), Red (Unplanned)

4. **Team Workload**
   - Type: Horizontal bar chart
   - Data: Items per team member
   - Color coding: Red if > 10 items

### Chart Configuration

```python
def create_status_chart(data: dict) -> str:
    """Generate Plotly chart JSON for status distribution."""
    chart_config = {
        'data': [{
            'type': 'pie',
            'labels': list(data.keys()),
            'values': list(data.values()),
            'textinfo': 'label+percent',
            'direction': 'clockwise'
        }],
        'layout': {
            'title': {'text': 'توزیع وضعیت', 'font': {'family': 'Vazir'}},
            'direction': 'rtl'
        }
    }
    return json.dumps(chart_config)
```

---

## HTML Rendering (renderers/html_renderer.py)

### Template Engine

**Jinja2** - For HTML template rendering with:
- Variable substitution
- Control structures (loops, conditionals)
- Filters for formatting
- RTL-aware rendering

### HTML Structure

```html
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گزارش پروژه - {{ project_name }}</title>
    <style>
        /* Embedded CSS - Vazir font, RTL layout, responsive design */
    </style>
</head>
<body>
    <header>
        <!-- Project name, date, summary metrics -->
    </header>
    
    <section class="metrics">
        <!-- Color-coded key metrics -->
    </section>
    
    <section class="charts">
        <!-- Interactive charts -->
    </section>
    
    <section class="high-priority">
        <!-- P🔥 and P0 items -->
    </section>
    
    <section class="by-status">
        <!-- Items grouped by status -->
    </section>
    
    <section class="detailed-table">
        <!-- Sortable table of all items -->
    </section>
    
    <script>
        /* Embedded Plotly.js and custom JavaScript */
    </script>
</body>
</html>
```

### CSS Design

**Key Features**:
- Vazir font for Persian text
- RTL layout with flexbox
- Responsive breakpoints: 320px, 768px, 1024px
- Color scheme: Professional blues with accent colors
- Print-friendly styles

**Color Coding**:
```css
.metric-good { color: #22c55e; }    /* Green */
.metric-warning { color: #eab308; } /* Yellow */
.metric-bad { color: #ef4444; }     /* Red */

.priority-fire { background: #fee2e2; color: #991b1b; }
.priority-p0 { background: #fed7aa; color: #9a3412; }
.priority-p1 { background: #fef3c7; color: #92400e; }
.priority-p2 { background: #dbeafe; color: #1e40af; }
```

---

## Snapshot Management (snapshot.py)

### Snapshot Format

```json
{
  "timestamp": "2025-11-08T17:42:00Z",
  "project_id": "PVT_kwDOCBxBz84BGVfV",
  "metrics": {
    "total_items": 76,
    "completion_percentage": 26.3,
    "unplanned_percentage": 18.4
  },
  "items": [...]
}
```

### Comparison Logic

```python
def compare_snapshots(current: ProjectData, previous: ProjectData) -> dict:
    """Calculate changes between snapshots."""
    return {
        'items_completed': count_newly_done(current, previous),
        'items_added': count_new_items(current, previous),
        'status_changes': track_status_changes(current, previous)
    }
```

---

## Alternative Renderers

### Markdown Renderer (md_renderer.py)

**Output Format**:
```markdown
# گزارش پروژه

## خلاصه آمار
- تعداد کل: 76
- درصد تکمیل: 26.3%
- برنامه‌ریزی نشده: 18.4%

## توزیع وضعیت
| وضعیت | تعداد | درصد |
|-------|-------|------|
| Backlog | 34 | 44.7% |
...
```

### CSV Renderer (csv_renderer.py)

**Columns**:
```
Title,Status,Priority,Assignees,Estimate,Labels,URL
```

**Encoding**: UTF-8 with BOM for Excel compatibility

### JSON Renderer (json_renderer.py)

**Structure**:
```json
{
  "metadata": {...},
  "metrics": {...},
  "items": [...]
}
```

---

## Error Handling

### Error Types and Responses

1. **GitHub CLI Not Found**
   ```
   خطا: GitHub CLI یافت نشد
   لطفاً از https://cli.github.com نصب کنید
   ```

2. **Authentication Failed**
   ```
   خطا: احراز هویت ناموفق
   دستور: gh auth login
   ```

3. **Project Not Found**
   ```
   خطا: پروژه یافت نشد
   بررسی کنید: owner و project_number
   ```

4. **Invalid Data**
   ```
   خطا: داده‌های ناقص
   فیلدهای گمشده: [list]
   ```

---

## Testing Strategy

### Test-Driven Development (TDD) Approach

**Philosophy**: Write tests first, then implement to make them pass. Keep tests focused and practical.

### Unit Tests

**Test Framework**: pytest

**What to Test** (focus on core logic):
- ✅ Data parsing and model creation
- ✅ Metrics calculations (percentages, counts, grouping)
- ✅ Color coding logic
- ✅ Snapshot comparison
- ✅ Configuration loading and validation

**What NOT to Test** (avoid over-engineering):
- ❌ Simple getters/setters
- ❌ Trivial property methods
- ❌ Third-party library internals (Jinja2, Plotly)

**Example Test Structure**:
```python
# tests/test_processor.py
import pytest
from src.models import ProjectItem, Priority, Status
from src.processor import calculate_metrics

def test_should_calculate_unplanned_percentage():
    # Arrange
    items = [
        ProjectItem(priority=Priority.FIRE, status=Status.TODO, ...),
        ProjectItem(priority=Priority.P1, status=Status.TODO, ...),
        ProjectItem(priority=Priority.P1, status=Status.DONE, ...)
    ]
    
    # Act
    result = calculate_metrics(items)
    
    # Assert
    assert result.unplanned_percentage == pytest.approx(33.3, rel=0.1)
    assert result.unplanned_count == 1
    assert result.planned_count == 2

def test_should_return_red_for_high_unplanned_percentage():
    # Arrange
    percentage = 25.0
    
    # Act
    color = get_unplanned_color(percentage)
    
    # Assert
    assert color == 'red'
```

**Mocking External Dependencies**:
```python
# tests/test_fetcher.py
from unittest.mock import patch, MagicMock
import json

@patch('subprocess.run')
def test_should_fetch_project_items(mock_run):
    # Arrange
    mock_run.return_value = MagicMock(
        stdout=json.dumps({"items": [{"id": "1", "title": "Test"}]}),
        returncode=0
    )
    fetcher = GitHubFetcher("owner", 2)
    
    # Act
    items = fetcher.fetch_project_items()
    
    # Assert
    assert len(items) == 1
    assert items[0]["title"] == "Test"
    mock_run.assert_called_once()
```

### Integration Tests

**Scope**: Test complete workflows with sample data

**Key Integration Tests**:
- End-to-end HTML report generation
- Multiple output formats (HTML, MD, CSV, JSON)
- Configuration loading from file
- Snapshot creation and comparison

**Example**:
```python
# tests/test_integration.py
def test_should_generate_html_report_end_to_end(tmp_path, sample_data):
    # Arrange
    config = Config(owner="test", project_number=1, output_directory=str(tmp_path))
    
    # Act
    generate_report(config, sample_data, format='html')
    
    # Assert
    output_file = tmp_path / "report.html"
    assert output_file.exists()
    content = output_file.read_text(encoding='utf-8')
    assert 'dir="rtl"' in content
    assert 'گزارش پروژه' in content
```

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_models.py           # Data model tests
├── test_config.py           # Configuration tests
├── test_fetcher.py          # GitHub fetching tests (mocked)
├── test_processor.py        # Data processing tests
├── test_snapshot.py         # Snapshot management tests
├── test_chart_builder.py    # Chart generation tests
├── test_renderers.py        # Renderer tests
└── test_integration.py      # End-to-end tests
```

### Shared Test Fixtures

```python
# tests/conftest.py
import pytest
from src.models import ProjectItem, Priority, Status

@pytest.fixture
def sample_items():
    """Provide sample project items for testing."""
    return [
        ProjectItem(
            id="1",
            title="Test Item 1",
            status=Status.TODO,
            priority=Priority.P1,
            assignees=["user1"],
            estimate_hours=5.0,
            labels=["bug"],
            url="https://github.com/..."
        ),
        # More sample items...
    ]

@pytest.fixture
def sample_project_data():
    """Provide complete project data structure."""
    return {
        "project": {...},
        "items": [...],
        "fields": [...]
    }
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_processor.py -v

# Run specific test
pytest tests/test_processor.py::test_should_calculate_unplanned_percentage -v

# Run with coverage
pytest --cov=src --cov-report=html tests/

# Run only fast tests (skip integration)
pytest -m "not integration"
```

### TDD Workflow Example

**Feature**: Calculate unplanned percentage

1. **Write test first** (it will fail):
```python
def test_should_calculate_unplanned_percentage():
    items = [create_item(Priority.FIRE), create_item(Priority.P1)]
    result = calculate_metrics(items)
    assert result.unplanned_percentage == 50.0
```

2. **Run test** - See it fail: `pytest tests/test_processor.py::test_should_calculate_unplanned_percentage -v`

3. **Write minimal code**:
```python
def calculate_metrics(items):
    unplanned = sum(1 for i in items if i.priority == Priority.FIRE)
    total = len(items)
    return ProjectMetrics(
        unplanned_percentage=(unplanned / total * 100) if total > 0 else 0
    )
```

4. **Run test** - See it pass

5. **Refactor if needed** - Improve code while keeping test green

### Coverage Goals

- **Core logic**: 80%+ coverage
- **Integration**: Key workflows covered
- **Don't chase 100%**: Focus on valuable tests, not coverage numbers

---

## Dependencies

### Required Libraries

```
# requirements.txt
plotly>=5.18.0          # Interactive charts
jinja2>=3.1.2           # Template engine
python-dateutil>=2.8.2  # Date handling
pytest>=7.4.0           # Testing
```

### Optional Dependencies

```
# requirements-dev.txt
black>=23.0.0           # Code formatting
mypy>=1.7.0             # Type checking
pylint>=3.0.0           # Linting
```

---

## Performance Considerations

### Optimization Strategies

1. **Data Fetching**: Single batch fetch, no pagination needed (limit 100)
2. **Chart Generation**: Pre-compute all data, generate JSON once
3. **HTML Size**: Minify embedded JavaScript and CSS
4. **Caching**: Cache Plotly.js library locally for offline use

### Expected Performance

- Data fetch: < 5 seconds
- Processing: < 1 second
- HTML generation: < 2 seconds
- **Total**: < 10 seconds for complete report

---

## Future Extensibility

### Laravel Migration Path

**Current Design Supports**:
1. **Clean separation**: Data fetching, processing, rendering are independent
2. **JSON API**: Easy to convert fetcher to API client
3. **Database ready**: Models can map to Eloquent models
4. **Template reuse**: Jinja2 templates similar to Blade

**Migration Steps**:
1. Replace fetcher with Laravel API client
2. Store snapshots in database
3. Convert Jinja2 templates to Blade
4. Add authentication and multi-user support

### Extensibility Points

- **New chart types**: Add to chart_builder.py
- **New output formats**: Implement base renderer interface
- **Custom metrics**: Extend processor.py
- **Themes**: Template variables for colors/fonts

---

## Security Considerations

1. **Input Validation**: Validate all user inputs (owner, project_number)
2. **Command Injection**: Use subprocess with list arguments, not shell=True
3. **File Permissions**: Create output files with appropriate permissions
4. **Sensitive Data**: Don't log authentication tokens

---

## Deployment

### Installation

```bash
# Clone repository
git clone <repo-url>
cd github-reporter

# Install dependencies
pip install -r requirements.txt

# Run
python src/main.py --help
```

### Distribution

**Option 1**: Python package
```bash
pip install github-projects-reporter
```

**Option 2**: Standalone executable (PyInstaller)
```bash
pyinstaller --onefile src/main.py
```

---

## Summary

This design provides:
- ✅ Clean, modular architecture
- ✅ Type-safe data models
- ✅ Comprehensive error handling
- ✅ Persian RTL support throughout
- ✅ Interactive, self-contained HTML
- ✅ Multiple output formats
- ✅ Weekly tracking with snapshots
- ✅ Color-coded metrics
- ✅ Extensible for Laravel migration

The implementation will follow Python best practices with clear separation of concerns, making it easy to test, maintain, and extend.
