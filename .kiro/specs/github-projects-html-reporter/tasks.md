# Implementation Plan

## TDD Workflow

This project follows Test-Driven Development (TDD):
1. **Write test first** - Define expected behavior
2. **Run test** - See it fail (red)
3. **Write code** - Minimal implementation
4. **Run test** - See it pass (green)
5. **Refactor** - Improve while keeping tests green

**Key Commands:**
- Run all tests: `pytest`
- Run specific test: `pytest tests/test_processor.py -v`
- Run with coverage: `pytest --cov=src tests/`

**Testing Focus:**
- ✅ Core logic and calculations
- ✅ Public interfaces
- ✅ Error handling
- ❌ Skip trivial getters/setters
- ❌ Don't over-test

---

## Tasks

- [x] 1. Set up project structure and core interfaces



  - Create directory structure for src/, tests/, templates/
  - Set up requirements.txt with dependencies
  - Create __init__.py files for packages





  - _Requirements: 1.1, 1.2_

- [x] 2. Implement data models and enums (TDD)
  - [x] 2.1 Create Priority and Status enums
    - Write tests for enum values and behavior


    - Define Priority enum with FIRE, P0, P1, P2
    - Define Status enum with all workflow states
    - Run tests to verify
    - _Requirements: 1.1, 5.1, 5.2_
  


  - [x] 2.2 Create ProjectItem data class
    - Write tests for ProjectItem creation and properties





    - Implement ProjectItem with all fields
    - Add is_planned and is_active properties
    - Run tests to verify
    - _Requirements: 2.5, 5.1, 5.2_
  
  - [x] 2.3 Create ProjectMetrics data class


    - Write tests for metrics structure
    - Define metrics structure for all statistics
    - Run tests to verify
    - _Requirements: 9.1, 9.2, 9.3, 5.3_



- [x] 3. Implement configuration management (TDD)
  - [x] 3.1 Create Config data class
    - Write tests for config loading and merging
    - Define configuration fields
    - Implement load() method for JSON config
    - Implement merge_with_args() for CLI override
    - Run tests to verify
    - _Requirements: 17.1, 17.2, 17.3, 17.4_
  
  - [x] 3.2 Add configuration validation
    - Write tests for validation logic
    - Validate owner and project_number
    - Validate format choices
    - Handle missing config file gracefully
    - Run tests to verify
    - _Requirements: 17.4, 17.5_

- [x] 4. Implement GitHub data fetcher


  - [x] 4.1 Create GitHubFetcher class

    - Implement __init__ with owner and project_number
    - Create _run_gh_command() helper method
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [x] 4.2 Implement data fetching methods


    - Implement fetch_project_details()
    - Implement fetch_project_items() with limit 100
    - Implement fetch_project_fields()
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [x] 4.3 Add error handling for GitHub CLI


    - Check if gh CLI is installed
    - Handle authentication errors
    - Validate JSON responses
    - _Requirements: 2.4, 19.1, 19.2, 19.3_

- [x] 5. Implement data processor (TDD)
  - [x] 5.1 Create data parsing functions
    - Write tests for JSON parsing with various inputs
    - Parse raw JSON to ProjectItem objects
    - Handle missing or null fields
    - Run tests to verify
    - _Requirements: 2.5, 19.3_
  
  - [x] 5.2 Implement metrics calculation
    - Write tests for each metric calculation
    - Calculate total items and estimates
    - Calculate completion percentage
    - Calculate planned vs unplanned percentages
    - Count high priority items not started
    - Run tests to verify
    - _Requirements: 9.1, 9.2, 9.3, 5.3, 5.4, 9.7_
  
  - [x] 5.3 Implement data grouping functions
    - Write tests for grouping logic
    - Group items by status
    - Group items by priority
    - Group items by assignee
    - Run tests to verify
    - _Requirements: 6.5, 7.2, 8.1_
  
  - [x] 5.4 Add color coding logic
    - Write tests for color coding with different values
    - Implement get_metric_color() function
    - Define thresholds for completion percentage
    - Define thresholds for unplanned percentage
    - Define thresholds for team workload
    - Run tests to verify
    - _Requirements: 9.4, 9.5, 9.6, 5.5, 5.6, 8.5_
  
  - [x] 5.5 Integrate grouping into metrics calculation



    - Update calculate_metrics() to populate items_by_status, items_by_priority, items_by_assignee
    - Use existing grouping functions
    - Update tests to verify grouped data in metrics


    - _Requirements: 6.5, 7.2, 8.1, 9.1_



- [x] 6. Implement snapshot management (TDD)
  - [x] 6.1 Create snapshot save functionality
    - Write tests for snapshot saving
    - Create snapshots/ directory if not exists
    - Save current data with timestamp


    - Use format: snapshot-YYYYMMDD-HHMMSS.json
    - Run tests to verify
    - _Requirements: 18.1, 18.2, 18.3_
  
  - [x] 6.2 Implement snapshot comparison

    - Write tests for comparison logic


    - Load previous snapshot if exists
    - Calculate items completed since last week
    - Calculate new items added

    - Track status changes
    - Run tests to verify
    - _Requirements: 18.4, 18.5_

- [x] 7. Implement chart generation


  - [x] 7.1 Set up Plotly chart builder
    - Create ChartBuilder class
    - Add helper for RTL configuration
    - _Requirements: 21.1, 3.4_
  

  - [x] 7.2 Create status distribution charts
    - Implement pie chart for status
    - Implement bar chart for status
    - Add Persian labels and RTL support

    - _Requirements: 6.1, 6.2, 6.3, 6.4, 3.2_
  
  - [x] 7.3 Create priority distribution chart
    - Implement horizontal bar chart
    - Exclude Done items

    - Apply priority color coding
    - _Requirements: 7.1, 7.2, 7.4_
  
  - [x] 7.4 Create planned vs unplanned chart
    - Implement pie chart
    - Use green for planned, red for unplanned
    - _Requirements: 5.4, 5.5, 5.6_
  
  - [x] 7.5 Create team workload chart
    - Implement horizontal bar chart
    - Show items per team member
    - Apply color coding for overload
    - _Requirements: 8.1, 8.3, 8.5_
  
  - [x] 7.6 Add chart interactivity
    - Configure hover tooltips
    - Enable legend click to show/hide
    - Ensure touch device support
    - _Requirements: 21.2, 21.3, 21.4, 21.5_

- [x] 8. Create HTML template


  - [x] 8.1 Design base HTML structure


    - Create report.html template with RTL
    - Add meta tags for UTF-8 and viewport
    - Structure sections: header, metrics, charts, items
    - _Requirements: 4.1, 4.2, 3.1, 3.2_
  
  - [x] 8.2 Embed CSS styles


    - Add Vazir font (embedded or CDN fallback)
    - Implement RTL layout with flexbox
    - Add responsive breakpoints
    - Apply color scheme and typography
    - _Requirements: 3.3, 20.1, 20.2, 20.3, 22.1, 22.2, 22.3_
  

  - [x] 8.3 Create metrics section
    - Display total items and estimates
    - Show completion percentage with color
    - Show planned vs unplanned with color
    - Show high priority not started with color
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8_

  
  - [x] 8.4 Create charts section
    - Add placeholders for all charts
    - Ensure proper spacing and layout

    - _Requirements: 6.1, 7.1, 5.4, 8.1_
  
  - [x] 8.5 Create high priority section
    - List P🔥 and P0 items
    - Show title, status, assignees, estimate
    - Add links to GitHub

    - Highlight unassigned items
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [x] 8.6 Create status-grouped sections
    - Create section for each status
    - List items with priority, title, assignees

    - Sort by priority within status
    - Show item counts
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_
  
  - [x] 8.7 Create detailed items table
    - Add table with all columns
    - Make sortable with JavaScript


    - Apply alternating row colors
    - Color-code priority column
    - Make titles clickable links
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

  
  - [x] 8.8 Embed JavaScript
    - Embed Plotly.js library
    - Add chart rendering code
    - Add table sorting functionality
    - Ensure offline functionality
    - _Requirements: 4.3, 4.4, 4.5, 21.5_

- [x] 9. Implement HTML renderer


  - [x] 9.1 Create HTMLRenderer class

    - Set up Jinja2 environment
    - Load report.html template
    - _Requirements: 4.1_
  
  - [x] 9.2 Implement render method

    - Pass all data to template
    - Generate charts JSON
    - Render final HTML
    - _Requirements: 4.2, 4.3, 4.4_
  
  - [x] 9.3 Add Persian text handling

    - Ensure UTF-8 encoding
    - Format Persian numbers
    - Format Persian dates
    - _Requirements: 3.2, 3.3, 3.5_

- [x] 10. Implement alternative renderers


  - [x] 10.1 Create base renderer interface


    - Define abstract Renderer class
    - Define render() method signature
    - _Requirements: 13.1, 14.1, 15.1_
  
  - [x] 10.2 Implement Markdown renderer


    - Create MarkdownRenderer class
    - Generate markdown with tables
    - Include all statistics
    - Add GitHub links
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
  
  - [x] 10.3 Implement CSV renderer


    - Create CSVRenderer class
    - Define columns structure
    - Use UTF-8 with BOM
    - Handle special characters
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_
  
  - [x] 10.4 Implement JSON renderer


    - Create JSONRenderer class
    - Include complete data structure
    - Add metadata
    - Format with indentation
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_



- [x] 12. Create CLI interface


  - [x] 12.1 Create main.py entry point


    - Implement argument parser with --format, --output, --owner, --project flags
    - Add --help documentation
    - Set default values from config
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_
  
  - [x] 12.2 Implement main orchestration function

    - Load configuration from file and merge with CLI args
    - Validate GitHub CLI is installed
    - Fetch data using GitHubFetcher
    - Process data using processor functions
    - Generate report using appropriate renderer
    - Save snapshot for weekly tracking
    - _Requirements: 16.6, 19.1, 19.5, 17.1, 17.2, 17.3_
  
  - [x] 12.3 Add comprehensive error handling

    - Catch GitHubCLIError and display clear messages
    - Catch ConfigValidationError and show validation issues
    - Handle file write errors
    - Exit with appropriate error codes
    - _Requirements: 19.1, 19.2, 19.3, 19.4_


- [x] 13. Create documentation
  - [x] 13.1 Write README.md


    - Add installation instructions
    - Add usage examples
    - Document configuration
    - Add troubleshooting section

  

  - [x] 13.2 Add code documentation
    - Write docstrings for remaining functions
    - Add type hints where missing
    - Include usage examples in docstrings

  
  - [x] 13.3 Create example config file

    - Provide config.json template
    - Document all options

- [x] 14. Integration testing and validation

  - [x] 14.1 Write integration tests


    - Test end-to-end with sample data
    - Test all output formats
    - Test configuration loading
    - Test snapshot comparison
  

  - [x] 14.2 Manual testing
    - Generate HTML report with real data
    - Test on different browsers
    - Test on mobile devices
    - Verify Persian text rendering
    - Verify RTL layout
    - Verify chart interactivity



- [x] 15. Final polish


  - [x] 15.1 Code cleanup

    - Run code formatter (black)
    - Fix linting issues
    - Remove debug code
  
  - [x] 15.2 Create example reports

    - Generate sample HTML report
    - Generate sample Markdown report
    - Include in repository
