---
inclusion: always
---

### Test Driven Design (TDD)

**Workflow for each feature:**
1. **Write test first** - Define expected behavior with a failing test
2. **Write minimal code** - Make the test pass with simplest implementation
3. **Run test** - Verify it passes: `pytest tests/test_<module>.py -v`
4. **Refactor if needed** - Improve code while keeping tests green
5. **Mark task complete** - Update tasks.md when done

**Testing Guidelines:**
- Focus on **core logic** and **public interfaces**
- Test **happy path** and **key error cases**
- Keep tests **simple and readable**
- Use **descriptive test names**: `test_should_calculate_unplanned_percentage()`
- Mock external dependencies (GitHub CLI calls)
- Don't over-test: Skip trivial getters/setters

**Commands:**
- Run all tests: `pytest`
- Run specific test: `pytest tests/test_processor.py::test_should_calculate_metrics -v`
- Run with coverage: `pytest --cov=src tests/`