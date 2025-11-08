"""Snapshot management for weekly tracking."""

import json
from pathlib import Path
from datetime import datetime
from typing import List

from src.models import ProjectItem


def save_snapshot(items: List[ProjectItem], snapshot_dir: str = "snapshots") -> str:
    """
    Save current project items as a snapshot with timestamp.
    
    Args:
        items: List of ProjectItem objects to save
        snapshot_dir: Directory to save snapshots (default: "snapshots")
        
    Returns:
        Path to the saved snapshot file
    """
    # Create snapshots directory if it doesn't exist
    snapshot_path = Path(snapshot_dir)
    snapshot_path.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp filename
    timestamp = datetime.now()
    filename = timestamp.strftime("snapshot-%Y%m%d-%H%M%S.json")
    filepath = snapshot_path / filename
    
    # Prepare snapshot data
    snapshot_data = {
        "timestamp": timestamp.isoformat() + "Z",
        "items": [_serialize_item(item) for item in items]
    }
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(snapshot_data, f, ensure_ascii=False, indent=2)
    
    return str(filepath)


def _serialize_item(item: ProjectItem) -> dict:
    """
    Serialize a ProjectItem to a dictionary.
    
    Args:
        item: ProjectItem to serialize
        
    Returns:
        Dictionary representation of the item
    """
    return {
        "id": item.id,
        "title": item.title,
        "status": item.status.value,
        "priority": item.priority.value,
        "assignees": item.assignees,
        "estimate_hours": item.estimate_hours,
        "labels": item.labels,
        "url": item.url,
        "repository": item.repository,
        "issue_number": item.issue_number
    }



def load_latest_snapshot(snapshot_dir: str = "snapshots") -> List[ProjectItem] | None:
    """
    Load the most recent snapshot from the snapshots directory.
    
    Args:
        snapshot_dir: Directory containing snapshots (default: "snapshots")
        
    Returns:
        List of ProjectItem objects from the latest snapshot, or None if no snapshots exist
    """
    snapshot_path = Path(snapshot_dir)
    
    # Check if directory exists
    if not snapshot_path.exists():
        return None
    
    # Find all snapshot files
    snapshot_files = list(snapshot_path.glob("snapshot-*.json"))
    
    if not snapshot_files:
        return None
    
    # Get the most recent snapshot (sort by filename which includes timestamp)
    latest_snapshot = max(snapshot_files, key=lambda p: p.name)
    
    # Load and deserialize
    with open(latest_snapshot, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return [_deserialize_item(item_data) for item_data in data["items"]]


def _deserialize_item(data: dict) -> ProjectItem:
    """
    Deserialize a dictionary to a ProjectItem.
    
    Args:
        data: Dictionary representation of an item
        
    Returns:
        ProjectItem instance
    """
    from src.models import Priority, Status
    
    return ProjectItem(
        id=data["id"],
        title=data["title"],
        status=Status(data["status"]),
        priority=Priority(data["priority"]),
        assignees=data["assignees"],
        estimate_hours=data["estimate_hours"],
        labels=data["labels"],
        url=data["url"],
        repository=data["repository"],
        issue_number=data["issue_number"]
    )


def compare_snapshots(current: List[ProjectItem], previous: List[ProjectItem] | None) -> dict:
    """
    Compare current items with previous snapshot to calculate changes.
    
    Args:
        current: Current list of ProjectItem objects
        previous: Previous list of ProjectItem objects (or None if no previous snapshot)
        
    Returns:
        Dictionary with comparison metrics:
        - items_completed: Count of items that moved to Done
        - items_added: Count of new items
        - status_changes: List of items that changed status
    """
    if previous is None:
        return {
            "items_completed": 0,
            "items_added": 0,
            "status_changes": []
        }
    
    # Create lookup dictionaries
    previous_by_id = {item.id: item for item in previous}
    current_by_id = {item.id: item for item in current}
    
    # Calculate items completed (moved to Done)
    items_completed = 0
    for item in current:
        if item.id in previous_by_id:
            prev_item = previous_by_id[item.id]
            from src.models import Status
            if prev_item.status != Status.DONE and item.status == Status.DONE:
                items_completed += 1
    
    # Calculate new items added
    items_added = sum(1 for item_id in current_by_id if item_id not in previous_by_id)
    
    # Track status changes
    status_changes = []
    for item in current:
        if item.id in previous_by_id:
            prev_item = previous_by_id[item.id]
            if prev_item.status != item.status:
                status_changes.append({
                    "id": item.id,
                    "title": item.title,
                    "from_status": prev_item.status.value,
                    "to_status": item.status.value
                })
    
    return {
        "items_completed": items_completed,
        "items_added": items_added,
        "status_changes": status_changes
    }
