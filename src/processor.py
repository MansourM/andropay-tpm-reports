"""Data processor for GitHub Projects data."""

from typing import List, Dict
from src.models import ProjectItem, Priority, Status


def parse_item(raw_item: Dict) -> ProjectItem:
    """
    Parse raw JSON item to ProjectItem object.
    
    Args:
        raw_item: Raw item dictionary from GitHub API
        
    Returns:
        ProjectItem instance
    """
    # Extract content fields
    content = raw_item.get('content', {})
    
    # Parse status with fallback
    status_value = raw_item.get('status', 'Backlog')
    try:
        status = Status(status_value)
    except ValueError:
        status = Status.BACKLOG
    
    # Parse priority with fallback
    priority_value = raw_item.get('priority', 'P2')
    try:
        priority = Priority(priority_value)
    except ValueError:
        # Handle corrupted P🔥 emoji (encoding issues)
        if priority_value and priority_value.startswith('P') and len(priority_value) > 2:
            # Likely corrupted P🔥, treat as FIRE priority
            priority = Priority.FIRE
        else:
            # Default to P2 for other invalid priorities
            priority = Priority.P2
    
    return ProjectItem(
        id=raw_item.get('id', ''),
        title=raw_item.get('title', ''),
        status=status,
        priority=priority,
        assignees=raw_item.get('assignees', []),
        estimate_hours=raw_item.get('estimate (Hrs)'),
        labels=raw_item.get('labels', []),
        url=content.get('url', ''),
        repository=content.get('repository', ''),
        issue_number=content.get('number')
    )


def parse_items(raw_items: List[Dict]) -> List[ProjectItem]:
    """
    Parse list of raw items to ProjectItem objects.
    
    Args:
        raw_items: List of raw item dictionaries
        
    Returns:
        List of ProjectItem instances
    """
    return [parse_item(item) for item in raw_items]



from src.models import ProjectMetrics, Priority, Status


def calculate_metrics(items: List[ProjectItem]) -> ProjectMetrics:
    """
    Calculate all metrics for project items.
    
    Args:
        items: List of ProjectItem objects
        
    Returns:
        ProjectMetrics with calculated statistics
    """
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
            items_by_assignee={},
            active_items=0,
            active_completion_percentage=0.0,
            pending_items=0,
            in_progress_items=0,
            active_unplanned_percentage=0.0,
            active_unplanned_count=0,
            todo_items=0,
            done_active_items=0,
            unplanned_done_percentage=0.0,
            unplanned_done_count=0
        )
    
    total_items = len(items)
    
    # Calculate total estimate hours
    total_estimate_hours = sum(
        item.estimate_hours for item in items if item.estimate_hours is not None
    )
    
    # Calculate completion percentage
    done_items = sum(1 for item in items if item.status == Status.DONE)
    completion_percentage = round((done_items / total_items * 100), 1) if total_items > 0 else 0.0
    
    # Calculate planned vs unplanned
    unplanned_count = sum(1 for item in items if not item.is_planned)
    planned_count = total_items - unplanned_count
    unplanned_percentage = round((unplanned_count / total_items * 100), 1) if total_items > 0 else 0.0
    
    # Count high priority items not started
    high_priority_not_started = sum(
        1 for item in items
        if item.priority in [Priority.FIRE, Priority.P0]
        and item.status in [Status.BACKLOG, Status.TODO]
    )
    
    # Group items by status, priority, and assignee
    items_by_status = group_by_status(items)
    items_by_priority = group_by_priority(items)
    items_by_assignee = group_by_assignee(items)
    
    # Calculate active work metrics (excluding Backlog)
    active_items_list = [
        item for item in items 
        if item.status != Status.BACKLOG
    ]
    active_items = len(active_items_list)
    
    # Active completion: Done / (Total - Backlog)
    active_done = sum(1 for item in active_items_list if item.status == Status.DONE)
    active_completion_percentage = round((active_done / active_items * 100), 1) if active_items > 0 else 0.0
    
    # Count pending and in-progress
    pending_items = sum(1 for item in items if item.status == Status.PENDING)
    in_progress_items = sum(1 for item in items if item.status == Status.IN_PROGRESS)
    
    # Calculate unplanned work in active tasks
    active_unplanned_count = sum(1 for item in active_items_list if not item.is_planned)
    active_unplanned_percentage = round((active_unplanned_count / active_items * 100), 1) if active_items > 0 else 0.0
    
    # NEW: Calculate enhanced metrics
    todo_items = calculate_todo_count(items)
    done_active_items = calculate_done_active_count(items)
    unplanned_done_percentage, unplanned_done_count = calculate_unplanned_done_stats(items)
    
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



def group_by_status(items: List[ProjectItem]) -> Dict[str, List[ProjectItem]]:
    """
    Group items by their status.
    
    Args:
        items: List of ProjectItem objects
        
    Returns:
        Dictionary mapping status to list of items
    """
    grouped = {}
    for item in items:
        status_name = item.status.value
        if status_name not in grouped:
            grouped[status_name] = []
        grouped[status_name].append(item)
    return grouped


def group_by_priority(items: List[ProjectItem]) -> Dict[str, List[ProjectItem]]:
    """
    Group items by their priority.
    
    Args:
        items: List of ProjectItem objects
        
    Returns:
        Dictionary mapping priority to list of items
    """
    grouped = {}
    for item in items:
        priority_name = item.priority.value
        if priority_name not in grouped:
            grouped[priority_name] = []
        grouped[priority_name].append(item)
    return grouped


def group_by_assignee(items: List[ProjectItem]) -> Dict[str, List[ProjectItem]]:
    """
    Group items by assignees.
    
    Items with multiple assignees will appear in multiple groups.
    Items with no assignees will be in "Unassigned" group.
    
    Args:
        items: List of ProjectItem objects
        
    Returns:
        Dictionary mapping assignee name to list of items
    """
    grouped = {}
    for item in items:
        if not item.assignees:
            # Unassigned items
            if "Unassigned" not in grouped:
                grouped["Unassigned"] = []
            grouped["Unassigned"].append(item)
        else:
            # Add item to each assignee's group
            for assignee in item.assignees:
                if assignee not in grouped:
                    grouped[assignee] = []
                grouped[assignee].append(item)
    return grouped



def get_completion_color(percentage: float) -> str:
    """
    Get color for completion percentage.
    
    Args:
        percentage: Completion percentage (0-100)
        
    Returns:
        Color name: 'green', 'yellow', or 'red'
    """
    if percentage > 70:
        return "green"
    elif percentage < 30:
        return "red"
    else:
        return "yellow"


def get_unplanned_color(percentage: float) -> str:
    """
    Get color for unplanned percentage.
    
    Lower is better for unplanned work.
    
    Args:
        percentage: Unplanned percentage (0-100)
        
    Returns:
        Color name: 'green', 'yellow', or 'red'
    """
    if percentage < 10:
        return "green"
    elif percentage > 20:
        return "red"
    else:
        return "yellow"


def get_workload_color(item_count: int) -> str:
    """
    Get color for team member workload.
    
    Args:
        item_count: Number of active items assigned
        
    Returns:
        Color name: 'green', 'yellow', or 'red'
    """
    if item_count > 10:
        return "red"
    elif item_count >= 6:
        return "yellow"
    else:
        return "green"


def get_high_priority_color(count: int) -> str:
    """
    Get color for high priority items not started.
    
    Args:
        count: Number of high priority items not started
        
    Returns:
        Color name: 'green', 'yellow', or 'red'
    """
    if count > 5:
        return "red"
    elif count > 0:
        return "yellow"
    else:
        return "green"


def calculate_todo_count(items: List[ProjectItem]) -> int:
    """
    Calculate count of active tasks with Todo status.
    
    Args:
        items: List of ProjectItem objects
        
    Returns:
        Count of Todo items (excluding Backlog)
    """
    return sum(
        1 for item in items
        if item.status == Status.TODO
    )


def calculate_done_active_count(items: List[ProjectItem]) -> int:
    """
    Calculate count of Done tasks excluding Backlog.
    
    Args:
        items: List of ProjectItem objects
        
    Returns:
        Count of Done items that are not in Backlog
    """
    return sum(
        1 for item in items
        if item.status == Status.DONE
    )


def calculate_unplanned_done_stats(items: List[ProjectItem]) -> tuple[float, int]:
    """
    Calculate percentage and count of done tasks that were unplanned (P🔥).
    
    Args:
        items: List of ProjectItem objects
        
    Returns:
        Tuple of (percentage, count) where:
        - percentage: % of done tasks that were P🔥
        - count: number of P🔥 tasks that are done
    """
    done_items = [item for item in items if item.status == Status.DONE]
    total_done = len(done_items)
    
    if total_done == 0:
        return (0.0, 0)
    
    unplanned_done = sum(1 for item in done_items if item.priority == Priority.FIRE)
    percentage = round((unplanned_done / total_done * 100), 1)
    
    return (percentage, unplanned_done)
