"""Data models for GitHub Projects Reporter."""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class Priority(Enum):
    """Priority levels for project items."""
    
    FIRE = "P🔥"  # Unplanned urgent work
    P0 = "P0"     # Critical priority
    P1 = "P1"     # High priority
    P2 = "P2"     # Medium priority


class Status(Enum):
    """Status values for project items."""
    
    BACKLOG = "Backlog"
    TODO = "Todo"
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    IN_REVIEW = "In Review"
    DONE = "Done"



@dataclass
class ProjectItem:
    """Represents a single item in the GitHub project."""
    
    id: str
    title: str
    status: Status
    priority: Priority
    assignees: List[str]
    estimate_hours: Optional[float]
    labels: List[str]
    url: str
    repository: str
    issue_number: Optional[int]
    
    @property
    def is_planned(self) -> bool:
        """Check if item is planned (not P🔥)."""
        return self.priority != Priority.FIRE
    
    @property
    def is_active(self) -> bool:
        """Check if item is active (not Done)."""
        return self.status != Status.DONE



@dataclass
class ProjectMetrics:
    """Calculated metrics for the project."""
    
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
    
    # Active work metrics (excluding Backlog)
    active_items: int = 0
    active_completion_percentage: float = 0.0
    pending_items: int = 0
    in_progress_items: int = 0
    active_unplanned_percentage: float = 0.0
    
    # NEW: Enhanced metrics
    todo_items: int = 0  # Active tasks with status "Todo"
    done_active_items: int = 0  # Done tasks excluding backlog
    unplanned_done_percentage: float = 0.0  # % of done tasks that were P🔥
    unplanned_done_count: int = 0  # Count of P🔥 tasks that are done
    active_unplanned_count: int = 0  # Count of P🔥 tasks in active work
