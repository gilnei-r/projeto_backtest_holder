# Implementation Plan: Save Plots and Add MT5 Provider

**Branch**: `005-save-plots-and-add-mt5-provider` | **Date**: 2025-10-30 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-save-plots-and-add-mt5-provider/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature will add three main capabilities to the project:
1.  The ability to save all generated plots as `.png` files instead of displaying them.
2.  The integration of MetaTrader 5 as a new data provider for stocks, acting as a fallback for `yfinance`.
3.  The reporting of tickers that failed to download from any provider.

The technical approach will involve using the official `MetaTrader5` Python package for the integration and `matplotlib.pyplot.savefig()` for saving the plots.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: `yfinance`, `matplotlib`, `pandas`, `python-bcb`, `MetaTrader5`
**Storage**: CSV files in `data/` and `results/` directories.
**Testing**: `pytest`
**Target Platform**: Windows
**Project Type**: Single project (CLI)
**Performance Goals**: The script execution time does not increase by more than 10% on average when fallback to MetaTrader 5 is triggered for a small number of tickers.
**Constraints**: The MetaTrader 5 terminal must be running on the same machine.
**Scale/Scope**: ~50 tickers, configurable backtest period.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **Code Quality:** Yes, the new code will follow the existing coding standards and modular structure of the project.
*   **Testing Standards:** Yes, new unit tests will be added for the MetaTrader 5 integration and plot saving functionality to maintain the 80% test coverage.
*   **User Experience Consistency:** N/A (CLI application).
*   **Performance Requirements:** Yes, the performance goal of a maximum 10% increase in execution time will be tracked and optimized for.

**Post-Design Check**: The design choices made in Phase 1 are aligned with the constitution. No violations are reported.

## Project Structure

### Documentation (this feature)

```text
specs/005-save-plots-and-add-mt5-provider/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
src/
├── data_loader.py  # Modified to include MT5 provider
├── plotting.py     # Modified to save plots
├── main.py         # Modified to handle failed tickers
└── config.py       # Modified with new configuration options

tests/
├── test_data_loader.py  # Modified with tests for MT5
└── test_plotting.py     # Modified with tests for saving plots
```

**Structure Decision**: The existing single project structure will be maintained. The new functionality will be integrated into the existing modules (`data_loader.py`, `plotting.py`, `main.py`, `config.py`) to ensure consistency.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | N/A        | N/A                                 |
