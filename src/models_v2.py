"""Data models v2 with timestamp support."""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class Priority(Enum):
    """Priority levels for project items."""
    
    FIRE = "P🔥"
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


class Status(Enum):
    """Status values for project items."""
    
    BACKLOG = "Backlog"
    TODO = "Todo"
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    IN_REVIEW = "In Review"
    DONE = "Done"


@dataclass
class ProjectItemV2:
    """Project item with timestamp fields."""
    
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
    
    # Timestamp fields
    project_created_at: Optional[str] = None
    project_updated_at: Optional[str] = None
    issue_created_at: Optional[str] = None
    issue_updated_at: Optional[str] = None
    issue_closed_at: Optional[str] = None
    
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
    active_items: int = 0
    active_completion_percentage: float = 0.0
    pending_items: int = 0
    in_progress_items: int = 0
    active_unplanned_percentage: float = 0.0
    todo_items: int = 0
    done_active_items: int = 0
    unplanned_done_percentage: float = 0.0
    unplanned_done_count: int = 0
    active_unplanned_count: int = 0
