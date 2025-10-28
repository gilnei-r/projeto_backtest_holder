# Tasks: IPCA Benchmark, Ticker Plot, and Data Verification

**Input**: Design documents from `/specs/002-ipca-benchmark-data-verification/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create `tests/` directory for test files.
- [X] T002 Create `tests/test_data_loader.py` for data loader tests.
- [X] T003 Create `tests/test_scenarios.py` for scenarios tests.
- [X] T004 Create `tests/test_plotting.py` for plotting tests.

---

## Phase 2: User Story 3 - Data Verification (Priority: P1)

**Goal**: As a user, I want the application to verify if the downloaded financial data is up-to-date, so that I don't have to re-download data unnecessarily and the backtest runs faster.

**Independent Test**: The data verification logic can be tested by checking mock data files with different timestamps.

### Implementation for User Story 3

- [X] T005 [US3] In `config.py`, add a setting `DATA_UPDATE_DAYS` to control how often to check for new data.
- [X] T006 [US3] In `data_loader.py`, modify `download_data` function to check the last modified time of the data file.
- [X] T007 [US3] In `data_loader.py`, if the file is recent enough (based on `DATA_UPDATE_DAYS`), skip the download.
- [X] T008 [US3] In `main.py`, ensure the data loading process is called before running the scenarios.

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently.

---

## Phase 3: User Story 1 - IPCA+x% Benchmark (Priority: P1)

**Goal**: As a user, I want to see my portfolio performance benchmarked against IPCA + x%, so that I can evaluate its real return above inflation. The value of 'x' should be configurable in `config.py`.

**Independent Test**: The benchmark calculation can be tested independently of the plotting by providing a set of portfolio values and IPCA data and verifying the calculated benchmark values.

### Implementation for User Story 1

- [X] T009 [US1] In `config.py`, add a new variable `IPCA_BENCHMARK_X` for the 'x' value.
- [X] T010 [US1] In `data_loader.py`, create a new function `get_ipca_data` to fetch IPCA data from the `python-bcb` library.
- [X] T011 [US1] In `scenarios.py`, create a function `calculate_ipca_benchmark` that takes the IPCA data and the `IPCA_BENCHMARK_X` value to calculate the benchmark.
- [X] T012 [US1] In `scenarios.py`, modify the backtesting scenarios to include the IPCA benchmark calculation.
- [X] T013 [US1] In `plotting.py`, update the performance plots to include the IPCA benchmark series.
- [X] T014 [US1] In `main.py`, ensure the IPCA benchmark is passed to the plotting function.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Ticker Value Plot (Priority: P2)

**Goal**: As a user, I want to see a bar plot showing the total current value of each ticker in my portfolio, so that I can easily visualize the distribution of my assets.

**Independent Test**: The plotting function can be tested independently by providing a list of tickers and their values and verifying the generated plot.

### Implementation for User Story 2

- [X] T015 [US2] In `plotting.py`, create a new function `plot_ticker_distribution` that takes a dictionary of tickers and their final values.
- [X] T016 [US2] The `plot_ticker_distribution` function should generate a bar plot.
- [X] T017 [US2] The bar plot should be sorted by descending total value as per FR-009.
- [X] T018 [US2] In `scenarios.py`, at the end of the simulation, gather the final value of each ticker.
- [X] T019 [US2] In `main.py`, call the new `plot_ticker_distribution` function to display the plot.

**Checkpoint**: At this point, User Stories 1, 2 and 3 should all work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T020 [P] Documentation updates in `README.md` and `GEMINI.md` to reflect the new features.
- [X] T021 Code cleanup and refactoring across modified files.
- [X] T022 Run `quickstart.md` validation to ensure all steps work as described.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **User Stories (Phase 2, 3, 4)**: All depend on Setup phase completion.
  - User stories can then proceed in parallel (if staffed) or sequentially in priority order (US3 -> US1 -> US2).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup (Phase 1).
- **User Story 2 (P2)**: Can start after Setup (Phase 1).
- **User Story 3 (P1)**: Can start after Setup (Phase 1).

### Within Each User Story

- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- Once Setup phase completes, all user stories can start in parallel.
- Different user stories can be worked on in parallel by different team members.

---

## Implementation Strategy

### MVP First (User Story 3 & 1)

1. Complete Phase 1: Setup
2. Complete Phase 2: User Story 3
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Stories 1 and 3 independently.
5. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup.
2. Add User Story 3 -> Test independently -> Deploy/Demo.
3. Add User Story 1 -> Test independently -> Deploy/Demo.
4. Add User Story 2 -> Test independently -> Deploy/Demo.
5. Each story adds value without breaking previous stories.
