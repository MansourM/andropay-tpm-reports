# Implementation Plan

- [x] 1. Enhance data processing with new metrics



  - [x] 1.1 Add new fields to ProjectMetrics dataclass


    - Add `todo_items`, `done_active_items`, `unplanned_done_percentage`, `unplanned_done_count` fields
    - _Requirements: 1.1, 1.2, 2.2, 2.3_
  
  - [x] 1.2 Implement metric calculation functions


    - Create `calculate_todo_count()` function to count Todo status items
    - Create `calculate_done_active_count()` function to count Done items excluding Backlog
    - Create `calculate_unplanned_done_stats()` function to calculate unplanned done percentage and count
    - _Requirements: 1.1, 1.2, 2.2, 2.3_
  


  - [x] 1.3 Update calculate_metrics() function

    - Call new calculation functions
    - Populate new ProjectMetrics fields
    - Handle edge cases (division by zero, empty lists)


    - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3_
  

  - [x] 1.4 Write unit tests for new metrics



    - Test todo count calculation with various statuses
    - Test done active count excludes backlog
    - Test unplanned done percentage with different ratios

    - Test zero division handling
    - _Requirements: 1.1, 1.2, 2.2, 2.3_

- [x] 2. Update HTML renderer with new context


  - [x] 2.1 Add color coding for new metrics

    - Implement color logic for unplanned_done_percentage
    - Add color variables to template context
    - _Requirements: 2.4, 7.6_
  
  - [x] 2.2 Update template context dictionary

    - Include all new metrics in context
    - Ensure backward compatibility
    - _Requirements: 1.1, 1.2, 2.2, 7.2, 7.3_

- [x] 3. Restructure HTML template metrics section


  - [x] 3.1 Update Active Work Metrics section


    - Add "Done Count" metric card
    - Add "To Do Count" metric card
    - Rename and clarify "Active Tasks" label
    - Update metric card subtitles for clarity
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 7.2_
  
  - [x] 3.2 Update Overall Project Metrics section


    - Update "Total Estimate Hours" label to "تخمین کل ساعت (برآورد اولیه)"
    - Add subtitle explaining it's initial estimate
    - Add "Unplanned Done %" metric card
    - _Requirements: 2.2, 2.3, 3.1, 3.2, 3.3, 7.3_
  
  - [x] 3.3 Apply color coding to new metrics

    - Use metric-green, metric-yellow, metric-red classes
    - Apply to unplanned done percentage
    - Ensure consistency with existing metrics
    - _Requirements: 2.4, 7.6_

- [x] 4. Implement responsive chart grid layout


  - [x] 4.1 Create charts-grid CSS class


    - Define 2-column grid for large screens (≥992px)
    - Define 1-column grid for medium/small screens (<992px)
    - Set appropriate gap and spacing
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [x] 4.2 Restructure charts section HTML


    - Group Status Distribution and Planned vs Unplanned in first grid
    - Group Priority Distribution and Team Workload in second grid
    - Apply charts-grid wrapper class
    - _Requirements: 4.1, 4.2, 7.4_
  
  - [x] 4.3 Test responsive behavior

    - Verify side-by-side display on large screens
    - Verify stacked display on medium/small screens
    - Check spacing and alignment
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 5. Implement responsive items grid layout


  - [x] 5.1 Create items-grid CSS class


    - Define 3-column grid for large screens (≥992px)
    - Define 2-column grid for medium screens (768-991px)
    - Define 1-column grid for small screens (<768px)
    - Use auto-fit with minmax for flexibility
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [x] 5.2 Update high priority items section


    - Replace items-list with items-grid class
    - Adjust item-card styling for grid layout
    - Ensure cards have consistent height
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [x] 5.3 Update status-based items section


    - Apply items-grid to each tab content
    - Update item-row to item-card for consistency
    - Maintain priority badge and assignee display
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [x] 5.4 Test grid responsiveness

    - Verify 3-column layout on desktop
    - Verify 2-column layout on tablet
    - Verify 1-column layout on mobile
    - Check for horizontal overflow
    - _Requirements: 5.1, 5.2, 5.3, 6.1, 6.2, 6.3_

- [x] 6. Final integration and testing



  - [x] 6.1 Generate test report with real data


    - Run reporter against actual GitHub project
    - Verify all new metrics display correctly
    - Check calculations are accurate
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  
  - [x] 6.2 Cross-browser testing

    - Test in Chrome, Firefox, Edge
    - Verify responsive behavior in each browser
    - Check chart rendering
    - _Requirements: 4.4, 5.4, 6.4_
  
  - [x] 6.3 Accessibility review

    - Verify color contrast for new metrics
    - Check screen reader compatibility
    - Ensure keyboard navigation works
    - _Requirements: 7.6_
  
  - [x] 6.4 Update documentation

    - Document new metrics in README
    - Add examples of new report sections
    - Update screenshots if needed
    - _Requirements: 7.1, 7.2, 7.3_
