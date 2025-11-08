"""Base renderer interface."""

from abc import ABC, abstractmethod
from typing import List

from src.models import ProjectItem, ProjectMetrics


class Renderer(ABC):
    """Abstract base class for report renderers."""
    
    @abstractmethod
    def render(
        self,
        items: List[ProjectItem],
        metrics: ProjectMetrics,
        output_path: str,
        project_name: str = "GitHub Project",
        owner: str = "",
        project_number: int = 0
    ) -> None:
        """
        Render report and save to file.
        
        Args:
            items: List of all project items
            metrics: Calculated project metrics
            output_path: Path to save the report file
            project_name: Name of the project
            owner: GitHub organization/user
            project_number: Project number
        """
        pass
