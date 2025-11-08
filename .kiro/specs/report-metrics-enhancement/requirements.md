# Requirements Document

## Introduction

This specification defines enhancements to the GitHub Projects HTML Reporter to provide better metrics visibility, improved layout efficiency, and more actionable insights for project management. The goal is to create a comprehensive snapshot report that helps project managers understand current project status, team workload, planning accuracy, and identify bottlenecks at a glance.

## Glossary

- **System**: The GitHub Projects HTML Reporter application
- **Active Tasks**: Tasks with status Todo, In Progress, Pending, or Done (excluding Backlog)
- **Unplanned Work**: Tasks marked with P🔥 priority
- **Metric Card**: A visual card component displaying a single metric value
- **Chart Container**: A section containing a Plotly visualization
- **Responsive Grid**: A CSS grid layout that adapts to screen size

## Requirements

### Requirement 1: Enhanced Active Task Metrics

**User Story:** As a project manager, I want clearer breakdown of active task counts, so that I can understand work distribution better.

#### Acceptance Criteria

1. WHEN viewing the active tasks section, THE System SHALL display a "Done Count" metric showing the number of completed active tasks
2. WHEN viewing the active tasks section, THE System SHALL display a "To Do Count" metric showing the number of not-started active tasks
3. WHEN viewing the active tasks section, THE System SHALL rename "تسک‌های فعال" to show "All Active Tasks" calculated as (Total - Backlog - Done)
4. WHEN viewing the active tasks section, THE System SHALL display current "تسک‌های فعال" value as the total active items count

### Requirement 2: Unplanned Work Analysis

**User Story:** As a project manager, I want to see how much unplanned work was completed, so that I can assess planning accuracy and team responsiveness.

#### Acceptance Criteria

1. WHEN viewing metrics, THE System SHALL display overall unplanned percentage across all tasks
2. WHEN viewing metrics, THE System SHALL display percentage of done tasks that were unplanned (P🔥)
3. WHEN calculating unplanned done percentage, THE System SHALL divide P🔥 done tasks by total done tasks
4. WHEN displaying unplanned metrics, THE System SHALL use color coding (green < 20%, yellow 20-40%, red > 40%)

### Requirement 3: Clarified Hour Estimates

**User Story:** As a project manager, I want clear labeling of hour estimates, so that I understand what the numbers represent.

#### Acceptance Criteria

1. WHEN viewing total project metrics, THE System SHALL label hour estimates as "تخمین کل ساعت (برآورد اولیه)"
2. WHEN viewing the metric card, THE System SHALL include a subtitle explaining it shows total estimated hours for all tasks
3. WHEN calculating estimates, THE System SHALL sum all estimate_hours values from all tasks

### Requirement 4: Optimized Chart Layout

**User Story:** As a user, I want efficient use of screen space for charts, so that I can see more information without scrolling.

#### Acceptance Criteria

1. WHEN viewing on large screens (≥992px), THE System SHALL display "توزیع وضعیت" and "برنامه‌ریزی شده در مقابل برنامه‌ریزی نشده" charts side by side
2. WHEN viewing on large screens (≥992px), THE System SHALL display "توزیع اولویت" and "بار کاری تیم" charts side by side
3. WHEN viewing on medium screens (<992px), THE System SHALL display each chart in its own row
4. WHEN displaying charts, THE System SHALL maintain responsive behavior and proper spacing

### Requirement 5: Compact High Priority Items Display

**User Story:** As a project manager, I want high priority items displayed in a space-efficient grid, so that I can see more items at once.

#### Acceptance Criteria

1. WHEN viewing high priority items on large screens (≥992px), THE System SHALL display items in a 3-column grid
2. WHEN viewing high priority items on medium screens (768-991px), THE System SHALL display items in a 2-column grid
3. WHEN viewing high priority items on small screens (<768px), THE System SHALL display items in a single column
4. WHEN displaying high priority items, THE System SHALL use card components with consistent styling

### Requirement 6: Compact Status-Based Items Display

**User Story:** As a project manager, I want status-based task lists displayed in a space-efficient grid, so that I can scan tasks more quickly.

#### Acceptance Criteria

1. WHEN viewing tasks by status on large screens (≥992px), THE System SHALL display items in a 3-column grid within each tab
2. WHEN viewing tasks by status on medium screens (768-991px), THE System SHALL display items in a 2-column grid within each tab
3. WHEN viewing tasks by status on small screens (<768px), THE System SHALL display items in a single column within each tab
4. WHEN displaying status-based items, THE System SHALL maintain readability and proper spacing

### Requirement 7: Comprehensive Report Structure Review

**User Story:** As a project manager, I want a well-organized report with relevant metrics and sections, so that I can quickly find the information I need for decision-making.

#### Acceptance Criteria

1. WHEN generating a report, THE System SHALL include the following sections in order: Header, Active Work Metrics, Overall Project Metrics, Charts, High Priority Items, Items by Status, Detailed Table
2. WHEN displaying Active Work Metrics, THE System SHALL show: Done Count, To Do Count, In Progress Count, Pending Count, Active Completion %, Active Unplanned %, High Priority Not Started
3. WHEN displaying Overall Project Metrics, THE System SHALL show: Total Items, Total Estimate Hours, Overall Completion %, Overall Unplanned %, Unplanned Done %
4. WHEN displaying Charts section, THE System SHALL include: Status Distribution, Priority Distribution, Planned vs Unplanned, Team Workload
5. WHEN organizing report sections, THE System SHALL prioritize actionable metrics (active work) over historical data (overall totals)
6. WHEN displaying metrics, THE System SHALL use consistent color coding across all sections (green for good, yellow for warning, red for critical)
