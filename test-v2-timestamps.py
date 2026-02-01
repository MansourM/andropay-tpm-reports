"""Test script for v2 implementation with timestamps."""

from src.fetcher_v2 import GitHubFetcherV2
from src.processor_v2 import parse_items_v2, filter_by_date_range, calculate_metrics_v2

# Test configuration
OWNER = "TechBurst-Pro"
PROJECT_NUMBER = 2

print("=" * 60)
print("Testing GitHub Projects Reporter V2 with Timestamps")
print("=" * 60)

# Fetch data with timestamps
print("\n1. Fetching project items with timestamps...")
fetcher = GitHubFetcherV2(OWNER, PROJECT_NUMBER)
raw_items = fetcher.fetch_project_items_with_timestamps(limit=10)
print(f"   ✓ Fetched {len(raw_items)} items")

# Parse items
print("\n2. Parsing items...")
items = parse_items_v2(raw_items)
print(f"   ✓ Parsed {len(items)} items")

# Display first item with timestamps
if items:
    item = items[0]
    print(f"\n3. Sample item with timestamps:")
    print(f"   Title: {item.title}")
    print(f"   Status: {item.status.value}")
    print(f"   Priority: {item.priority.value}")
    print(f"   Project Created: {item.project_created_at}")
    print(f"   Project Updated: {item.project_updated_at}")
    print(f"   Issue Created: {item.issue_created_at}")
    print(f"   Issue Updated: {item.issue_updated_at}")
    print(f"   Issue Closed: {item.issue_closed_at}")

# Test date filtering
print(f"\n4. Testing date filtering...")
print(f"   Total items: {len(items)}")

# Filter items created in November 2025
november_items = filter_by_date_range(
    items,
    start_date='2025-11-01',
    end_date='2025-11-30',
    date_field='issue_created_at'
)
print(f"   Items created in November 2025: {len(november_items)}")

# Filter items updated in December 2025
december_items = filter_by_date_range(
    items,
    start_date='2025-12-01',
    end_date='2025-12-31',
    date_field='issue_updated_at'
)
print(f"   Items updated in December 2025: {len(december_items)}")

# Calculate metrics
print(f"\n5. Calculating metrics...")
metrics = calculate_metrics_v2(items)
print(f"   Total items: {metrics.total_items}")
print(f"   Completion: {metrics.completion_percentage}%")
print(f"   Unplanned: {metrics.unplanned_percentage}%")

# Calculate metrics for filtered data
if november_items:
    print(f"\n6. Metrics for November 2025 items:")
    nov_metrics = calculate_metrics_v2(november_items)
    print(f"   Total: {nov_metrics.total_items}")
    print(f"   Completion: {nov_metrics.completion_percentage}%")
    print(f"   Unplanned: {nov_metrics.unplanned_percentage}%")

print("\n" + "=" * 60)
print("✓ V2 Implementation Test Complete!")
print("=" * 60)
