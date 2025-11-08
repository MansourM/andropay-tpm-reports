# Requirements Document

## Introduction

This document specifies requirements for a Python-based GitHub Projects report generator that produces beautiful, self-contained HTML reports with Persian (RTL) language support, charts, and visualizations. The tool will help track weekly progress for the Andropay Task Management project.

## Glossary

- **GitHub Projects**: GitHub's project management tool (Projects v2)
- **GitHub CLI (gh)**: Command-line tool for interacting with GitHub
- **Self-contained HTML**: Single HTML file with all CSS, JavaScript, and assets embedded
- **RTL**: Right-to-left text direction for Persian language
- **Priority Levels**: P🔥 (urgent/unplanned), P0 (critical), P1 (high), P2 (medium)
- **Planned vs Unplanned**: Planned items (P0-P2) vs Unplanned items (P🔥)
- **Report Generator**: The Python application that creates reports
- **Project Item**: A task, issue, or card in the GitHub Project
- **Status**: Current state of an item (Backlog, Todo, Pending, In Progress, In Review, Done)

## Requirements

### Requirement 1: Cross-Platform Python Tool

**User Story:** As a developer, I want a Python-based tool that works on Windows, macOS, and Linux, so that all team members can generate reports regardless of their operating system.

#### Acceptance Criteria

1. THE Report Generator SHALL be implemented in Python 3.8 or higher
2. THE Report Generator SHALL use only cross-platform compatible libraries
3. THE Report Generator SHALL execute GitHub CLI commands using subprocess module
4. THE Report Generator SHALL parse JSON output from GitHub CLI commands
5. THE Report Generator SHALL handle file paths in a cross-platform manner using pathlib

### Requirement 2: Data Fetching from GitHub Projects

**User Story:** As a project manager, I want the tool to automatically fetch current project data from GitHub, so that reports always reflect the latest information.

#### Acceptance Criteria

1. THE Report Generator SHALL fetch project details using `gh project view` command
2. THE Report Generator SHALL fetch all project items using `gh project item-list` command with limit of 100
3. THE Report Generator SHALL fetch project field definitions using `gh project field-list` command
4. WHEN GitHub CLI command fails, THEN THE Report Generator SHALL display a clear error message
5. THE Report Generator SHALL validate that required project data fields exist before processing

### Requirement 3: Persian Language Support with RTL

**User Story:** As a Persian-speaking team member, I want reports in Persian with proper right-to-left layout, so that I can easily read and understand the content.

#### Acceptance Criteria

1. THE Report Generator SHALL generate HTML reports with RTL text direction
2. THE Report Generator SHALL use Persian language for all labels, headings, and descriptions
3. THE Report Generator SHALL properly render Persian numbers and dates
4. THE Report Generator SHALL ensure charts and visualizations work correctly with RTL layout
5. THE Report Generator SHALL use UTF-8 encoding for all text content

### Requirement 4: Self-Contained HTML Output

**User Story:** As a team lead, I want a single HTML file that I can share via chat or email, so that recipients can view the report without installing anything.

#### Acceptance Criteria

1. THE Report Generator SHALL produce a single HTML file as output
2. THE Report Generator SHALL embed all CSS styles inline within the HTML
3. THE Report Generator SHALL embed all JavaScript code inline within the HTML
4. THE Report Generator SHALL embed all chart libraries inline within the HTML
5. THE Report Generator SHALL ensure the HTML file opens correctly in modern web browsers without internet connection

### Requirement 5: Planned vs Unplanned Items Analysis

**User Story:** As a project manager, I want to see the ratio of planned vs unplanned work, so that I can identify process improvements and reduce mid-sprint interruptions.

#### Acceptance Criteria

1. THE Report Generator SHALL classify items with P🔥 priority as "Unplanned"
2. THE Report Generator SHALL classify items with P0, P1, or P2 priorities as "Planned"
3. THE Report Generator SHALL calculate percentage of unplanned items vs total items
4. THE Report Generator SHALL display planned vs unplanned ratio in a visual chart
5. WHEN unplanned percentage exceeds 20%, THEN THE Report Generator SHALL highlight this metric in red color
6. WHEN unplanned percentage is below 10%, THEN THE Report Generator SHALL highlight this metric in green color

### Requirement 6: Status Distribution Visualization

**User Story:** As a team member, I want to see how items are distributed across different statuses, so that I can understand the current workflow state.

#### Acceptance Criteria

1. THE Report Generator SHALL create a pie chart showing items by status
2. THE Report Generator SHALL create a bar chart showing items by status
3. THE Report Generator SHALL display count and percentage for each status
4. THE Report Generator SHALL use distinct colors for each status
5. THE Report Generator SHALL include all statuses: Backlog, Todo, Pending, In Progress, In Review, Done

### Requirement 7: Priority Distribution Visualization

**User Story:** As a project manager, I want to see priority distribution of active items, so that I can ensure we're focusing on the right work.

#### Acceptance Criteria

1. THE Report Generator SHALL create a chart showing items by priority level
2. THE Report Generator SHALL exclude "Done" items from priority distribution
3. THE Report Generator SHALL display count and percentage for each priority
4. THE Report Generator SHALL use color coding: P🔥 (red), P0 (orange), P1 (yellow), P2 (blue)
5. THE Report Generator SHALL show separate counts for planned vs unplanned priorities

### Requirement 8: Team Workload Visualization

**User Story:** As a team lead, I want to see workload distribution across team members, so that I can balance assignments and identify bottlenecks.

#### Acceptance Criteria

1. THE Report Generator SHALL create a bar chart showing items per team member
2. THE Report Generator SHALL display total estimated hours per team member
3. THE Report Generator SHALL show count of active items (not Done) per team member
4. THE Report Generator SHALL list unassigned items separately
5. WHEN a team member has more than 10 active items, THEN THE Report Generator SHALL highlight their workload in red

### Requirement 9: Summary Statistics with Color Coding

**User Story:** As a stakeholder, I want key metrics highlighted with colors, so that I can quickly identify good and bad trends.

#### Acceptance Criteria

1. THE Report Generator SHALL display total items count
2. THE Report Generator SHALL display total estimated hours
3. THE Report Generator SHALL calculate and display completion percentage (Done items / Total items)
4. WHEN completion percentage is above 70%, THEN THE Report Generator SHALL display it in green
5. WHEN completion percentage is below 30%, THEN THE Report Generator SHALL display it in red
6. WHEN completion percentage is between 30% and 70%, THEN THE Report Generator SHALL display it in yellow
7. THE Report Generator SHALL display count of high priority items (P🔥, P0) not yet started
8. WHEN high priority items not started exceeds 5, THEN THE Report Generator SHALL display count in red

### Requirement 10: High Priority Items Section

**User Story:** As a developer, I want to see all high priority items in one place, so that I know what needs immediate attention.

#### Acceptance Criteria

1. THE Report Generator SHALL create a dedicated section for P🔥 and P0 items
2. THE Report Generator SHALL display item title, status, assignees, and estimate for each high priority item
3. THE Report Generator SHALL sort high priority items by priority (P🔥 first, then P0)
4. THE Report Generator SHALL provide direct links to GitHub issues
5. THE Report Generator SHALL highlight unassigned high priority items

### Requirement 11: Items Grouped by Status

**User Story:** As a team member, I want to see all items organized by their current status, so that I can understand what's in each stage of the workflow.

#### Acceptance Criteria

1. THE Report Generator SHALL create sections for each status category
2. THE Report Generator SHALL list all items within each status section
3. THE Report Generator SHALL display item priority, title, assignees, and estimate
4. THE Report Generator SHALL sort items within each status by priority
5. THE Report Generator SHALL provide item count for each status section

### Requirement 12: Detailed Items Table

**User Story:** As a project manager, I want a comprehensive table of all items, so that I can review complete project details.

#### Acceptance Criteria

1. THE Report Generator SHALL create a table with columns: Title, Status, Priority, Assignees, Estimate, Labels
2. THE Report Generator SHALL make the table sortable by clicking column headers
3. THE Report Generator SHALL apply alternating row colors for readability
4. THE Report Generator SHALL use color coding for priority column
5. THE Report Generator SHALL make item titles clickable links to GitHub

### Requirement 13: Markdown Output Format

**User Story:** As a developer, I want to generate Markdown reports, so that I can include them in documentation or version control.

#### Acceptance Criteria

1. WHEN user specifies markdown format, THEN THE Report Generator SHALL produce a .md file
2. THE Report Generator SHALL include all summary statistics in markdown format
3. THE Report Generator SHALL create markdown tables for item listings
4. THE Report Generator SHALL use markdown headers for section organization
5. THE Report Generator SHALL include links to GitHub issues in markdown format

### Requirement 14: CSV Output Format

**User Story:** As a data analyst, I want to export project data to CSV, so that I can perform custom analysis in Excel or other tools.

#### Acceptance Criteria

1. WHEN user specifies CSV format, THEN THE Report Generator SHALL produce a .csv file
2. THE Report Generator SHALL include columns: Title, Status, Priority, Assignees, Estimate, Labels, URL
3. THE Report Generator SHALL use UTF-8 encoding with BOM for Excel compatibility
4. THE Report Generator SHALL handle commas and quotes in data fields correctly
5. THE Report Generator SHALL create separate rows for items with multiple assignees

### Requirement 15: JSON Output Format

**User Story:** As a developer, I want to export raw data to JSON, so that I can integrate with other tools or scripts.

#### Acceptance Criteria

1. WHEN user specifies JSON format, THEN THE Report Generator SHALL produce a .json file
2. THE Report Generator SHALL include complete project data structure
3. THE Report Generator SHALL include metadata: generation timestamp, project info
4. THE Report Generator SHALL format JSON with proper indentation for readability
5. THE Report Generator SHALL use UTF-8 encoding

### Requirement 16: Command Line Interface

**User Story:** As a user, I want a simple command-line interface, so that I can easily generate reports with different options.

#### Acceptance Criteria

1. THE Report Generator SHALL accept `--format` argument with choices: html, md, csv, json
2. THE Report Generator SHALL accept `--output` argument to specify output file path
3. THE Report Generator SHALL accept `--owner` argument to specify GitHub organization
4. THE Report Generator SHALL accept `--project` argument to specify project number
5. THE Report Generator SHALL display help message when run with `--help` flag
6. WHEN no arguments provided, THEN THE Report Generator SHALL use default values: html format, TechBurst-Pro owner, project 2

### Requirement 17: Configuration File Support

**User Story:** As a user, I want to save my project settings in a config file, so that I don't have to type them every time.

#### Acceptance Criteria

1. THE Report Generator SHALL read configuration from `config.json` file if present
2. THE Report Generator SHALL support configuration for: owner, project_number, default_format, output_directory
3. THE Report Generator SHALL allow command-line arguments to override config file settings
4. WHEN config file is missing, THEN THE Report Generator SHALL use built-in defaults
5. THE Report Generator SHALL validate configuration values before use

### Requirement 18: Weekly Report Tracking

**User Story:** As a project manager, I want to track changes week over week, so that I can see progress trends.

#### Acceptance Criteria

1. THE Report Generator SHALL save a snapshot of current data with timestamp
2. THE Report Generator SHALL store snapshots in a `snapshots/` directory
3. THE Report Generator SHALL name snapshot files with format: `snapshot-YYYYMMDD-HHMMSS.json`
4. WHEN previous snapshot exists, THEN THE Report Generator SHALL calculate changes since last snapshot
5. THE Report Generator SHALL display metrics: items completed since last week, new items added, items moved to different statuses

### Requirement 19: Error Handling and Validation

**User Story:** As a user, I want clear error messages when something goes wrong, so that I can fix issues quickly.

#### Acceptance Criteria

1. WHEN GitHub CLI is not installed, THEN THE Report Generator SHALL display installation instructions
2. WHEN GitHub authentication fails, THEN THE Report Generator SHALL display authentication instructions
3. WHEN project data is incomplete, THEN THE Report Generator SHALL display which fields are missing
4. WHEN output file cannot be written, THEN THE Report Generator SHALL display file permission error
5. THE Report Generator SHALL validate all required dependencies on startup

### Requirement 20: Responsive HTML Design

**User Story:** As a mobile user, I want reports to display correctly on my phone, so that I can review them anywhere.

#### Acceptance Criteria

1. THE Report Generator SHALL use responsive CSS that adapts to screen size
2. THE Report Generator SHALL ensure charts resize appropriately on mobile devices
3. THE Report Generator SHALL use readable font sizes on small screens
4. THE Report Generator SHALL ensure tables scroll horizontally on narrow screens
5. THE Report Generator SHALL test HTML output on viewport widths from 320px to 1920px

### Requirement 21: Chart Interactivity

**User Story:** As a report viewer, I want interactive charts that show details on hover, so that I can explore data without cluttering the view.

#### Acceptance Criteria

1. THE Report Generator SHALL use interactive chart library (Plotly or Chart.js)
2. WHEN user hovers over chart element, THEN THE Report Generator SHALL display detailed tooltip
3. THE Report Generator SHALL allow clicking chart legend to show/hide data series
4. THE Report Generator SHALL ensure chart interactions work on touch devices
5. THE Report Generator SHALL maintain chart interactivity in offline mode

### Requirement 22: Professional Visual Design

**User Story:** As a stakeholder, I want reports to look professional and polished, so that I can share them with confidence.

#### Acceptance Criteria

1. THE Report Generator SHALL use a modern, clean design aesthetic
2. THE Report Generator SHALL use consistent color scheme throughout the report
3. THE Report Generator SHALL use proper spacing and typography
4. THE Report Generator SHALL include a header with project name and generation date
5. THE Report Generator SHALL use icons or visual indicators for status and priority
