# V2 Implementation: Time-Based Filtering

## Problem & Solution

**Problem:** Cannot filter GitHub Projects reports by date/time range → impossible to calculate KPIs for specific periods.

**Root Cause:** Original tool uses `gh project item-list` which doesn't expose timestamp fields.

**Solution:** ✅ GitHub GraphQL API provides timestamps via `gh api graphql`

## What Was Built

### New V2 Modules (3 files)
- `src/fetcher_v2.py` - GraphQL fetcher with timestamp support
- `src/models_v2.py` - Models with 5 timestamp fields
- `src/processor_v2.py` - Date filtering + metrics calculation

### Timestamp Fields Available
```python
project_created_at   # When added to project
project_updated_at   # Last updated in project
issue_created_at     # When issue created
issue_updated_at     # When issue updated
issue_closed_at      # When issue closed (null if open)
```

## Usage

```python
from src.fetcher_v2 import GitHubFetcherV2
from src.processor_v2 import parse_items_v2, filter_by_date_range, calculate_metrics_v2

# Fetch with timestamps
fetcher = GitHubFetcherV2("TechBurst-Pro", 2)
items = parse_items_v2(fetcher.fetch_project_items_with_timestamps())

# Filter by date range (e.g., November 2025)
november = filter_by_date_range(
    items,
    start_date='2025-11-01',
    end_date='2025-11-30',
    date_field='issue_created_at'  # or issue_updated_at, issue_closed_at, etc.
)

# Calculate KPIs for specific period
metrics = calculate_metrics_v2(november)
print(f"Completion: {metrics.completion_percentage}%")
print(f"Unplanned: {metrics.unplanned_percentage}%")
```

## Testing

```powershell
python test-v2-timestamps.py
```

**Test Results:**
- ✓ Fetched 10 items with timestamps
- ✓ Date filtering works correctly
- ✓ All 5 timestamp fields populated

## Next Steps - Choose Integration Approach

### Option 1: Add to Existing CLI ⭐ Recommended
Modify `src/main.py` to add flags:
```
--use-v2              # Use GraphQL fetcher
--start-date DATE     # e.g., 2025-11-01
--end-date DATE       # e.g., 2025-11-30
--date-field FIELD    # issue_created_at, issue_updated_at, etc.
```

### Option 2: Separate V2 Tool
Create `src/main_v2.py` as standalone CLI with date filtering built-in.

### Option 3: Full Migration
Replace original fetcher with V2, deprecate old code.

## Benefits Unlocked

✅ Sprint reports (2-week periods)  
✅ Monthly/quarterly KPIs  
✅ Trend analysis over time  
✅ Filter by completion date  
✅ Time-based metrics

## Original Implementation Preserved

All original files unchanged - V2 is additive:
- `src/fetcher.py`, `src/models.py`, `src/processor.py`, `src/main.py`
