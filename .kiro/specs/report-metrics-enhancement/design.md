# Design Document

## Overview

This design enhances the GitHub Projects HTML Reporter with improved metrics, better layout efficiency, and clearer insights. The solution involves updates to the data processing layer (processor.py), template rendering (html_renderer.py), and UI layout (report.html template).

## Architecture

### Component Updates

1. **Data Processing Layer** (`src/processor.py`)
   - Add new metric calculations for done count, todo count, and unplanned done percentage
   - Extend `ProjectMetrics` dataclass with new fields

2. **Rendering Layer** (`src/renderers/html_renderer.py`)
   - Pass new metrics to template context
   - Calculate color coding for new metrics

3. **Presentation Layer** (`src/templates/report.html`)
   - Restructure metrics sections with new cards
   - Implement responsive grid layouts for charts and item lists
   - Add CSS for side-by-side chart display

## Components and Interfaces

### 1. Enhanced ProjectMetrics Dataclass

```python
@dataclass
class ProjectMetrics:
    # Existing fields
    total_items: int
    active_items: int
    in_progress_items: int
    pending_items: int
    backlog_items: int
    done_items: int
    total_estimate_hours: int
    completion_percentage: float
    active_completion_percentage: float
    unplanned_percentage: float
    active_unplanned_percentage: float
    high_priority_not_started: int
    
    # NEW fields
    todo_items: int  # Active tasks with status "Todo"
    done_active_items: int  # Done tasks excluding backlog
    unplanned_done_percentage: float  # % of done tasks that were P🔥
    unplanned_done_count: int  # Count of P🔥 tasks that are done
```

### 2. Metric Calculation Functions

**Function: `calculate_todo_count(items: List[ProjectItem]) -> int`**
- Filter items where status is "Todo" and not in Backlog
- Return count

**Function: `calculate_done_active_count(items: List[ProjectItem]) -> int`**
- Filter items where status is "Done" and not in Backlog
- Return count

**Function: `calculate_unplanned_done_percentage(items: List[ProjectItem]) -> tuple[float, int]`**
- Filter done items (status == "Done")
- Count how many have priority == "P🔥"
- Calculate percentage: (unplanned_done / total_done) * 100
- Return (percentage, unplanned_done_count)

### 3. Template Context Enhancement

```python
def render(self, data: dict) -> str:
    # Existing context
    context = {
        'project_name': data['project_name'],
        'metrics': data['metrics'],
        # ... existing fields
        
        # NEW: Color coding for new metrics
        'unplanned_done_color': self._get_color_for_percentage(
            data['metrics'].unplanned_done_percentage,
            thresholds={'green': 20, 'yellow': 40}
        ),
    }
```

### 4. HTML Template Structure

#### Metrics Section Layout

```
┌─────────────────────────────────────────────┐
│ Active Work Metrics (بدون Backlog)          │
├─────────────┬─────────────┬─────────────────┤
│ Done Count  │ To Do Count │ In Progress     │
│ Pending     │ Active %    │ Active Unplan % │
│ High Pri NS │             │                 │
└─────────────┴─────────────┴─────────────────┘

┌─────────────────────────────────────────────┐
│ Overall Project Metrics                     │
├─────────────┬─────────────┬─────────────────┤
│ Total Items │ Est. Hours  │ Overall %       │
│ Unplan %    │ Unplan Done%│                 │
└─────────────┴─────────────┴─────────────────┘
```

#### Charts Section Layout (Large Screens)

```
┌──────────────────────┬──────────────────────┐
│ Status Distribution  │ Planned vs Unplanned │
└──────────────────────┴──────────────────────┘

┌──────────────────────┬──────────────────────┐
│ Priority Distribution│ Team Workload        │
└──────────────────────┴──────────────────────┘
```

#### High Priority Items Layout (Large Screens)

```
┌──────────────┬──────────────┬──────────────┐
│ Item Card 1  │ Item Card 2  │ Item Card 3  │
├──────────────┼──────────────┼──────────────┤
│ Item Card 4  │ Item Card 5  │ Item Card 6  │
└──────────────┴──────────────┴──────────────┘
```

## Data Models

### Metric Card Component

```html
<div class="metric-card">
    <h3>{{ title }}</h3>
    <p class="metric-value metric-{{ color }}">{{ value }}</p>
    <small>{{ subtitle }}</small>
</div>
```

### Chart Grid Container

```html
<div class="charts-grid">
    <div class="chart-container"><!-- Chart 1 --></div>
    <div class="chart-container"><!-- Chart 2 --></div>
</div>
```

### Item Grid Container

```html
<div class="items-grid">
    <div class="item-card"><!-- Item 1 --></div>
    <div class="item-card"><!-- Item 2 --></div>
    <div class="item-card"><!-- Item 3 --></div>
</div>
```

## CSS Grid Specifications

### Charts Grid

```css
.charts-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

@media (max-width: 991px) {
    .charts-grid {
        grid-template-columns: 1fr;
    }
}
```

### Items Grid (High Priority & Status Items)

```css
.items-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
    gap: 15px;
}

@media (max-width: 991px) {
    .items-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 767px) {
    .items-grid {
        grid-template-columns: 1fr;
    }
}
```

## Error Handling

1. **Missing Metrics**: If new metrics cannot be calculated, default to 0 and log warning
2. **Division by Zero**: When calculating percentages, check for zero denominators and return 0.0
3. **Invalid Data**: Validate that counts are non-negative integers

## Testing Strategy

### Unit Tests

1. **test_calculate_todo_count**: Verify correct filtering of Todo items
2. **test_calculate_done_active_count**: Verify Done items exclude Backlog
3. **test_calculate_unplanned_done_percentage**: Test with various ratios of P🔥 done items
4. **test_unplanned_done_percentage_zero_done**: Verify handling when no done items exist
5. **test_metrics_color_coding**: Verify correct color assignment for thresholds

### Integration Tests

1. **test_enhanced_metrics_in_context**: Verify all new metrics appear in template context
2. **test_html_rendering_with_new_metrics**: Verify HTML renders without errors
3. **test_responsive_grid_classes**: Verify correct CSS classes applied

### Visual Testing

1. Test responsive behavior at breakpoints: 1200px, 991px, 767px, 575px
2. Verify chart side-by-side layout on large screens
3. Verify item grids collapse correctly on smaller screens
4. Verify no horizontal scrollbars at any breakpoint

## Implementation Notes

1. **Backward Compatibility**: Existing metrics remain unchanged; only additions
2. **Performance**: New calculations are O(n) where n is number of items
3. **Localization**: All new labels use Persian text consistent with existing UI
4. **Color Coding**: Use existing color scheme (green/yellow/red) for consistency
