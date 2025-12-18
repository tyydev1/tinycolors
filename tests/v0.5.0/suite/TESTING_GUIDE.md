# TinyColors Testing Guide

## Quick Start

Run all tests:
```bash
python -m pytest tests/v0.5.0/test_tinycolors.py -v
```

Expected output:
```
============================= 282 passed in 0.40s ==============================
```

## Common Testing Commands

### Basic Test Run
```bash
# Run all tests with minimal output
python -m pytest tests/v0.5.0/test_tinycolors.py

# Run all tests with verbose output
python -m pytest tests/v0.5.0/test_tinycolors.py -v

# Run all tests with very verbose output
python -m pytest tests/v0.5.0/test_tinycolors.py -vv
```

### Coverage Analysis
```bash
# Show coverage report
python -m pytest tests/v0.5.0/test_tinycolors.py --cov=tinycolors --cov-report=term-missing

# Generate HTML coverage report
python -m pytest tests/v0.5.0/test_tinycolors.py --cov=tinycolors --cov-report=html
# View in browser: htmlcov/index.html
```

### Run Specific Tests
```bash
# Run specific test class
python -m pytest tests/v0.5.0/test_tinycolors.py::TestColorizeBasics -v

# Run specific test method
python -m pytest tests/v0.5.0/test_tinycolors.py::TestColorizeBasics::test_colorize_with_red_color -v

# Run tests matching a pattern
python -m pytest tests/v0.5.0/test_tinycolors.py -k "colorize" -v

# Run tests matching multiple patterns
python -m pytest tests/v0.5.0/test_tinycolors.py -k "colorize or colortext" -v
```

### Debugging Tests
```bash
# Show print statements during tests
python -m pytest tests/v0.5.0/test_tinycolors.py -v -s

# Stop on first failure
python -m pytest tests/v0.5.0/test_tinycolors.py -x

# Stop on first failure and drop to debugger
python -m pytest tests/v0.5.0/test_tinycolors.py -x --pdb

# Show local variables on failure
python -m pytest tests/v0.5.0/test_tinycolors.py -l
```

### Performance and Analysis
```bash
# Show slowest tests
python -m pytest tests/v0.5.0/test_tinycolors.py --durations=10

# Show test collection without running
python -m pytest tests/v0.5.0/test_tinycolors.py --collect-only

# Run with parallel processing (requires pytest-xdist)
python -m pytest tests/v0.5.0/test_tinycolors.py -n auto
```

## Test Organization

The test suite is organized into logical test classes:

```
TestColorizeBasics              - Basic colorize() function tests
TestColorizeStyles              - colorize() with style parameters
TestColorizeBackgrounds         - colorize() with background colors
TestColorizeCombo               - Combined parameter tests
TestColorizeDefaults            - Default/None value handling
TestColorizeErrors              - Error handling tests
TestColortextBasics             - New colortext() function tests
TestColortextBrightColors       - colortext() with bright colors
TestColortextBackground         - colortext() with backgrounds
TestColortextSpecialColors      - colortext() with gray/default
TestColortextErrors             - colortext() error handling
TestCprintLegacyAPI             - cprint() legacy API
TestCprintNewAPI                - cprint() new API
TestCprintAPIPreference         - cprint() API precedence
TestCprintKwargs                - cprint() kwargs passthrough
TestCinputLegacyAPI             - cinput() legacy API
TestCinputNewAPI                - cinput() new API
TestCinputAPIPreference         - cinput() API precedence
TestCinputReturnValue           - cinput() return value tests
TestClibColorClass              - clib color class tests
TestColorBrightClass            - color.bright class tests
TestColorBgClass                - color.bg class tests
TestColorBgBrightClass          - color.bg.bright class tests
TestColorStyleClasses           - color style classes (NodeProxy)
TestColorStyleClassValues       - Style class values
TestNodeProxyRepr               - NodeProxy methods
TestColorMap                    - COLOR_MAP tests
TestStyleMap                    - STYLE_MAP tests
TestBGColorMap                  - BG_COLOR_MAP tests
TestCombinedStylesMap           - COMBINED_STYLES tests
TestCombinedStylesWithBGMap     - COMBINED_STYLES_WITH_BG tests
TestEdgeCases                   - Edge case tests
TestIntegration                 - Integration/real-world tests
TestBackwardCompatibility       - Legacy API compatibility tests
```

## Running Test Groups

```bash
# Run only colorize tests
python -m pytest tests/v0.5.0/test_tinycolors.py -k colorize -v

# Run only colortext tests
python -m pytest tests/v0.5.0/test_tinycolors.py -k colortext -v

# Run only cprint tests
python -m pytest tests/v0.5.0/test_tinycolors.py -k cprint -v

# Run only cinput tests
python -m pytest tests/v0.5.0/test_tinycolors.py -k cinput -v

# Run only color class tests
python -m pytest tests/v0.5.0/test_tinycolors.py -k "Color" -v

# Run only error handling tests
python -m pytest tests/v0.5.0/test_tinycolors.py -k error -v

# Run only edge case tests
python -m pytest tests/v0.5.0/test_tinycolors.py::TestEdgeCases -v

# Run only integration tests
python -m pytest tests/v0.5.0/test_tinycolors.py::TestIntegration -v
```

## Understanding Test Results

### Successful Run
```
============================= 282 passed in 0.40s ==============================
```
All tests passed successfully. The test suite confirms that all functions, methods, and classes work as expected.

### With Coverage
```
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
tinycolors/__init__.py     181      2    99%   13, 26
------------------------------------------------------
TOTAL                      181      2    99%
```
- Stmts: Total statements in the file
- Miss: Number of statements not covered by tests
- Cover: Coverage percentage
- Missing: Line numbers not covered (Windows-specific code in this case)

## Test Categories at a Glance

### Legacy API Tests
Tests the original colorize/cprint/cinput functions with individual color, style, and bg parameters.

**Count**: 40+ tests
**Functions**: colorize(), cprint(), cinput()
**Coverage**: All parameters, all values, all combinations

### New API Tests
Tests the new colortext/cprint/cinput functions with combined style notation (e.g., "bold red").

**Count**: 50+ tests
**Functions**: colortext(), cprint(as_=...), cinput(as_=...)
**Coverage**: All style combinations, backgrounds, special colors

### Color Class Tests
Tests the color class hierarchy, clib, color.bright, color.bg, and style classes.

**Count**: 70+ tests
**Classes**: clib, color, color.bright, color.bg, color.bold, color.dim, etc.
**Coverage**: All classes, all attributes, NodeProxy functionality

### Map Tests
Tests the color, style, and background maps for completeness and correctness.

**Count**: 30+ tests
**Maps**: COLOR_MAP, STYLE_MAP, BG_COLOR_MAP, COMBINED_STYLES, COMBINED_STYLES_WITH_BG
**Coverage**: All entries, correct ANSI codes, total counts

### Error Tests
Tests error handling and exception raising.

**Count**: 15+ tests
**Exceptions**: ColorNotFoundError, StyleNotFoundError
**Coverage**: Invalid colors, invalid styles, error messages

### Edge Cases
Tests unusual inputs and boundary conditions.

**Count**: 14 tests
**Scenarios**: Empty strings, unicode, special characters, very long text, newlines
**Coverage**: All edge cases mentioned

### Integration Tests
Tests real-world usage scenarios and component interactions.

**Count**: 7 tests
**Scenarios**: Multiple colored strings, platform initialization, API consistency
**Coverage**: Common use patterns

### Backward Compatibility
Tests that the legacy API continues to work correctly.

**Count**: 6 tests
**Focus**: Ensuring no regressions in existing functionality

## Interpreting Test Output

### Test Name Format
```
tests/v0.5.0/test_tinycolors.py::TestClassName::test_method_name PASSED [XX%]
```

Example:
```
tests/v0.5.0/test_tinycolors.py::TestColorizeBasics::test_colorize_with_red_color PASSED [0%]
```

### Success Indicator
```
PASSED  - Test passed successfully
FAILED  - Test failed (would show assertion error)
SKIPPED - Test was skipped (marked with @pytest.mark.skip)
XFAIL   - Expected failure (marked with @pytest.mark.xfail)
```

### Progress Indicator
The `[XX%]` at the end shows what percentage of tests have completed so far.

## Continuous Integration

To use these tests in CI/CD pipelines:

```bash
# Non-zero exit code on failure
python -m pytest tests/v0.5.0/test_tinycolors.py --tb=short

# Exit immediately on first failure
python -m pytest tests/v0.5.0/test_tinycolors.py -x

# Generate JUnit XML for CI systems
python -m pytest tests/v0.5.0/test_tinycolors.py --junit-xml=results.xml

# Generate coverage badge/metrics
python -m pytest tests/v0.5.0/test_tinycolors.py --cov=tinycolors --cov-report=xml
```

## Pytest Configuration

Tests use pytest from `pyproject.toml`. Key settings:
- Test discovery in `tests/` directory
- Tests must have `test_` prefix or be in `Test` classes
- Markers available for organizing tests

## Tips and Tricks

### Run tests automatically on file changes
```bash
# Requires pytest-watch
pip install pytest-watch
ptw tests/v0.5.0/test_tinycolors.py
```

### Generate test report
```bash
# Requires pytest-html
pip install pytest-html
python -m pytest tests/v0.5.0/test_tinycolors.py --html=report.html --self-contained-html
```

### Show which tests would run without executing
```bash
python -m pytest tests/v0.5.0/test_tinycolors.py --collect-only -q
```

### Count test methods
```bash
python -m pytest tests/v0.5.0/test_tinycolors.py --collect-only -q | wc -l
```

## Troubleshooting

### Issue: "No module named pytest"
**Solution**: Install pytest
```bash
pip install pytest pytest-cov
```

### Issue: "Tests not found"
**Solution**: Run from project root directory
```bash
cd /home/razkar/PycharmProjects/tinycolors
python -m pytest tests/v0.5.0/test_tinycolors.py
```

### Issue: "ModuleNotFoundError: No module named 'tinycolors'"
**Solution**: Add project to Python path or install in development mode
```bash
cd /home/razkar/PycharmProjects/tinycolors
pip install -e .
```

### Issue: Tests timeout
**Solution**: These tests run very fast (~0.4s) so timeout shouldn't occur. If it does, there may be a system issue.

## Additional Resources

- Pytest Documentation: https://docs.pytest.org/
- Test File: `/home/razkar/PycharmProjects/tinycolors/tests/v0.5.0/test_tinycolors.py`
- Test Summary: `/home/razkar/PycharmProjects/tinycolors/tests/v0.5.0/TEST_SUITE_SUMMARY.md`

## Quick Reference

```bash
# Most common commands

# Run all tests
pytest tests/v0.5.0/test_tinycolors.py -v

# Run with coverage
pytest tests/v0.5.0/test_tinycolors.py --cov=tinycolors --cov-report=term-missing

# Run specific test class
pytest tests/v0.5.0/test_tinycolors.py::TestColorizeBasics -v

# Run specific test
pytest tests/v0.5.0/test_tinycolors.py::TestColorizeBasics::test_colorize_with_red_color -v

# Run tests matching pattern
pytest tests/v0.5.0/test_tinycolors.py -k "bold" -v

# Show slowest tests
pytest tests/v0.5.0/test_tinycolors.py --durations=10

# Stop on first failure
pytest tests/v0.5.0/test_tinycolors.py -x -v
```
