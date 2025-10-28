# Implementation Plan: IPCA Benchmark, Ticker Plot, and Data Verification

**Branch**: `002-ipca-benchmark-data-verification` | **Date**: 2025-10-28 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `C:\Git\Projeto_B&H\specs\002-ipca-benchmark-data-verification\spec.md`

## Summary

This feature will add three main capabilities to the backtesting script:
1.  A new benchmark based on IPCA + x%.
2.  A bar plot showing the total value of each ticker.
3.  A data verification mechanism to avoid unnecessary downloads.

## Technical Context

**Language/Version**: Python 3.11 [NEEDS CLARIFICATION: Please confirm the Python version]
**Primary Dependencies**: yfinance, pandas, matplotlib, python-bcb, numpy, openpyxl
**Storage**: File-based (Excel files for results)
**Testing**: [NEEDS CLARIFICATION: What testing framework should be used? e.g., pytest, unittest]
**Target Platform**: Windows/Linux/macOS (Python script)
**Project Type**: single project
**Performance Goals**: The data verification feature should significantly reduce the script's execution time when data is up-to-date.
**Constraints**: The solution should be implemented within the existing structure of the project.
**Scale/Scope**: The new features should work with the existing backtesting scenarios.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **Code Quality:** Does the proposed code adhere to our coding standards? Is it clean, readable, and maintainable?
*   **Testing Standards:** Are there comprehensive unit and integration tests for all new features and bug fixes? Is the 80% test coverage met?
*   **User Experience Consistency:** Does the UI and UX align with our design system and style guide?
*   **Performance Requirements:** Does the new code meet our performance benchmarks? Has it been profiled and optimized?

## Project Structure

### Documentation (this feature)

```text
specs/002-ipca-benchmark-data-verification/
├── plan.md              # This file
├── research.md          # To be generated
├── data-model.md        # To be generated
├── quickstart.md        # To be generated
└── tasks.md             # To be generated
```

### Source Code (repository root)

```text
# Single project (DEFAULT)
config.py
data_loader.py
main.py
plotting.py
scenarios.py
```

**Structure Decision**: The new features will be implemented by modifying the existing files (`config.py`, `data_loader.py`, `main.py`, `plotting.py`, `scenarios.py`).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |