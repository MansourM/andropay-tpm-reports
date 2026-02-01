"""Data processor v2 with date filtering support."""

from typing import List, Dict, Optional
from datetime import datetime
from src.models_v2 import ProjectItemV2, Priority, Status, ProjectMetrics


def parse_item_v2(raw_item: Dict) -> ProjectItemV2:
    """
    Parse raw JSON item to ProjectItemV2 object.
    
    Args:
        raw_item: Raw item dictionary from GraphQL API
        
    Returns:
        ProjectItemV2 instance
    """
    content = raw_item.get('content', {})
    
    status_value = raw_item.get('status', 'Backlog')
    try:
        status = Status(status_value)
    except ValueError:
        status = Status.BACKLOG
    
    priority_value = raw_item.get('priority', 'P2')
    try:
        priority = Priority(priority_value)
    except ValueError:
        if priority_value and priority_value.startswith('P') and len(priority_value) > 2:
            priority = Priority.FIRE
        else:
            priority = Priority.P2
    
    return ProjectItemV2(
        id=raw_item.get('id', ''),
        title=raw_item.get('title', ''),
        status=status,
        priority=priority,
        assignees=raw_item.get('assignees', []),
        estimate_hours=raw_item.get('estimate (Hrs)'),
        labels=raw_item.get('labels', []),
        url=content.get('url', ''),
        repository=content.get('repository', ''),
        issue_number=content.get('number'),
        project_created_at=raw_item.get('project_created_at'),
        project_updated_at=raw_item.get('project_updated_at'),
        issue_created_at=raw_item.get('issue_created_at'),
        issue_updated_at=raw_item.get('issue_updated_at'),
        issue_closed_at=raw_item.get('issue_closed_at')
    )


def parse_items_v2(raw_items: List[Dict]) -> List[ProjectItemV2]:
    """Parse list of raw items to ProjectItemV2 objects."""
    return [parse_item_v2(item) for item in raw_items]


def filter_by_date_range(
    items: List[ProjectItemV2],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date_field: str = 'issue_created_at'
) -> List[ProjectItemV2]:
    """
    Filter items by date range.
    
    Args:
        items: List of ProjectItemV2 objects
        start_date: Start date in ISO format (e.g., '2025-01-01')
        end_date: End date in ISO format (e.g., '2025-01-31')
        date_field: Which timestamp field to filter on
                   ('issue_created_at', 'issue_updated_at', 'issue_closed_at',
                    'project_created_at', 'project_updated_at')
    
    Returns:
        Filtered list of items
    """
    if not start_date and not end_date:
        return items
    
    from datetime import timezone
    
    filtered = []
    for item in items:
        date_value = getattr(item, date_field, None)
        if not date_value:
            continue
        
        item_date = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
        
        if start_date:
            start = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
            if item_date < start:
                continue
        
        if end_date:
            end = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)
            if item_date > end:
                continue
        
        filtered.append(item)
    
    return filtered


def calculate_metrics_v2(items: List[ProjectItemV2]) -> ProjectMetrics:
    """Calculate metrics for ProjectItemV2 objects."""
    if not items:
        return ProjectMetrics(
            total_items=0,
            total_estimate_hours=0.0,
            completion_percentage=0.0,
            planned_count=0,
            unplanned_count=0,
            unplanned_percentage=0.0,
            high_priority_not_started=0,
            items_by_status={},
            items_by_priority={},
            items_by_assignee={}
        )
    
    total_items = len(items)
    total_estimate_hours = sum(
        item.estimate_hours for item in items if item.estimate_hours is not None
    )
    
    done_items = sum(1 for item in items if item.status == Status.DONE)
    completion_percentage = round((done_items / total_items * 100), 1) if total_items > 0 else 0.0
    
    unplanned_count = sum(1 for item in items if not item.is_planned)
    planned_count = total_items - unplanned_count
    unplanned_percentage = round((unplanned_count / total_items * 100), 1) if total_items > 0 else 0.0
    
    high_priority_not_started = sum(
        1 for item in items
        if item.priority in [Priority.FIRE, Priority.P0]
        and item.status in [Status.BACKLOG, Status.TODO]
    )
    
    items_by_status = {}
    items_by_priority = {}
    items_by_assignee = {}
    
    for item in items:
        status_name = item.status.value
        if status_name not in items_by_status:
            items_by_status[status_name] = []
        items_by_status[status_name].append(item)
        
        priority_name = item.priority.value
        if priority_name not in items_by_priority:
            items_by_priority[priority_name] = []
        items_by_priority[priority_name].append(item)
        
        if not item.assignees:
            if "Unassigned" not in items_by_assignee:
                items_by_assignee["Unassigned"] = []
            items_by_assignee["Unassigned"].append(item)
        else:
            for assignee in item.assignees:
                if assignee not in items_by_assignee:
                    items_by_assignee[assignee] = []
                items_by_assignee[assignee].append(item)
    
    active_items_list = [item for item in items if item.status != Status.BACKLOG]
    active_items = len(active_items_list)
    active_done = sum(1 for item in active_items_list if item.status == Status.DONE)
    active_completion_percentage = round((active_done / active_items * 100), 1) if active_items > 0 else 0.0
    
    pending_items = sum(1 for item in items if item.status == Status.PENDING)
    in_progress_items = sum(1 for item in items if item.status == Status.IN_PROGRESS)
    
    active_unplanned_count = sum(1 for item in active_items_list if not item.is_planned)
    active_unplanned_percentage = round((active_unplanned_count / active_items * 100), 1) if active_items > 0 else 0.0
    
    todo_items = sum(1 for item in items if item.status == Status.TODO)
    done_active_items = sum(1 for item in items if item.status == Status.DONE)
    
    done_items_list = [item for item in items if item.status == Status.DONE]
    total_done = len(done_items_list)
    unplanned_done_count = sum(1 for item in done_items_list if item.priority == Priority.FIRE)
    unplanned_done_percentage = round((unplanned_done_count / total_done * 100), 1) if total_done > 0 else 0.0
    
    return ProjectMetrics(
        total_items=total_items,
        total_estimate_hours=total_estimate_hours,
        completion_percentage=completion_percentage,
        planned_count=planned_count,
        unplanned_count=unplanned_count,
        unplanned_percentage=unplanned_percentage,
        high_priority_not_started=high_priority_not_started,
        items_by_status=items_by_status,
        items_by_priority=items_by_priority,
        items_by_assignee=items_by_assignee,
        active_items=active_items,
        active_completion_percentage=active_completion_percentage,
        pending_items=pending_items,
        in_progress_items=in_progress_items,
        active_unplanned_percentage=active_unplanned_percentage,
        active_unplanned_count=active_unplanned_count,
        todo_items=todo_items,
        done_active_items=done_active_items,
        unplanned_done_percentage=unplanned_done_percentage,
        unplanned_done_count=unplanned_done_count
    )
