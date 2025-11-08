"""Markdown report renderer."""

from pathlib import Path
from typing import List
from datetime import datetime

from src.renderers.base import Renderer
from src.models import ProjectItem, ProjectMetrics, Priority
from src.processor import (
    get_completion_color,
    get_unplanned_color,
    get_high_priority_color
)


class MarkdownRenderer(Renderer):
    """Renderer for generating Markdown reports."""
    
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
        Render Markdown report and save to file.
        
        Args:
            items: List of all project items
            metrics: Calculated project metrics
            output_path: Path to save the Markdown file
            project_name: Name of the project
            owner: GitHub organization/user
            project_number: Project number
        """
        lines = []
        
        # Header
        lines.append(f"# گزارش پروژه: {project_name}\n")
        lines.append(f"**سازمان:** {owner} | **شماره پروژه:** {project_number}\n")
        lines.append(f"**تاریخ تولید:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append("\n---\n")
        
        # Summary Statistics
        lines.append("## خلاصه آمار\n")
        lines.append(f"- **تعداد کل آیتم‌ها:** {metrics.total_items}\n")
        lines.append(f"- **تخمین کل ساعت:** {metrics.total_estimate_hours}\n")
        
        completion_color = get_completion_color(metrics.completion_percentage)
        completion_emoji = self._get_emoji_for_color(completion_color)
        lines.append(f"- **درصد تکمیل:** {metrics.completion_percentage:.1f}% {completion_emoji}\n")
        
        unplanned_color = get_unplanned_color(metrics.unplanned_percentage)
        unplanned_emoji = self._get_emoji_for_color(unplanned_color)
        lines.append(f"- **برنامه‌ریزی نشده:** {metrics.unplanned_percentage:.1f}% {unplanned_emoji}\n")
        
        high_priority_color = get_high_priority_color(metrics.high_priority_not_started)
        high_priority_emoji = self._get_emoji_for_color(high_priority_color)
        lines.append(f"- **اولویت بالا شروع نشده:** {metrics.high_priority_not_started} {high_priority_emoji}\n")
        lines.append("\n")
        
        # Status Distribution
        lines.append("## توزیع وضعیت\n")
        lines.append("| وضعیت | تعداد | درصد |\n")
        lines.append("|-------|-------|------|\n")
        for status, status_items in metrics.items_by_status.items():
            count = len(status_items)
            percentage = (count / metrics.total_items * 100) if metrics.total_items > 0 else 0
            lines.append(f"| {status} | {count} | {percentage:.1f}% |\n")
        lines.append("\n")
        
        # Priority Distribution
        lines.append("## توزیع اولویت\n")
        lines.append("| اولویت | تعداد | درصد |\n")
        lines.append("|--------|-------|------|\n")
        for priority, priority_items in metrics.items_by_priority.items():
            count = len(priority_items)
            percentage = (count / metrics.total_items * 100) if metrics.total_items > 0 else 0
            lines.append(f"| {priority} | {count} | {percentage:.1f}% |\n")
        lines.append("\n")
        
        # High Priority Items
        high_priority_items = [
            item for item in items
            if item.priority in [Priority.FIRE, Priority.P0]
        ]
        
        if high_priority_items:
            lines.append("## آیتم‌های با اولویت بالا (P🔥 و P0)\n")
            for item in high_priority_items:
                assignees = ", ".join(item.assignees) if item.assignees else "بدون مسئول"
                estimate = f"{item.estimate_hours} ساعت" if item.estimate_hours else "-"
                lines.append(f"- **[{item.priority.value}]** [{item.title}]({item.url})\n")
                lines.append(f"  - وضعیت: {item.status.value}\n")
                lines.append(f"  - مسئولین: {assignees}\n")
                lines.append(f"  - تخمین: {estimate}\n")
            lines.append("\n")
        
        # Items by Status
        lines.append("## آیتم‌ها بر اساس وضعیت\n")
        for status, status_items in metrics.items_by_status.items():
            lines.append(f"### {status} ({len(status_items)})\n")
            for item in status_items:
                assignees = ", ".join(item.assignees) if item.assignees else "بدون مسئول"
                lines.append(f"- **[{item.priority.value}]** [{item.title}]({item.url}) - {assignees}\n")
            lines.append("\n")
        
        # Detailed Items Table
        lines.append("## جدول کامل آیتم‌ها\n")
        lines.append("| عنوان | وضعیت | اولویت | مسئولین | تخمین | برچسب‌ها |\n")
        lines.append("|-------|-------|--------|---------|-------|----------|\n")
        for item in items:
            title = f"[{item.title}]({item.url})"
            assignees = ", ".join(item.assignees) if item.assignees else "-"
            estimate = str(item.estimate_hours) if item.estimate_hours else "-"
            labels = ", ".join(item.labels) if item.labels else "-"
            lines.append(f"| {title} | {item.status.value} | {item.priority.value} | {assignees} | {estimate} | {labels} |\n")
        
        # Write to file
        content = "".join(lines)
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding='utf-8')
    
    def _get_emoji_for_color(self, color: str) -> str:
        """Get emoji representation for color."""
        if color == 'green':
            return '✅'
        elif color == 'yellow':
            return '⚠️'
        elif color == 'red':
            return '❌'
        return ''
