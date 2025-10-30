# Tasks: Update Benchmark Data

**Input**: Design documents from `/specs/004-update-benchmark-data/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- Paths shown below assume single project structure.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ensure the development environment is correctly configured.

- [x] T001 Verify all dependencies from `requirements.txt` are installed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

*No foundational tasks are required for this feature, as it modifies existing functionality.*

---

## Phase 3: User Story 1 - Use CDI as the primary benchmark (Priority: P1) 🎯 MVP

**Goal**: Replace the SELIC rate with the CDI rate as the primary benchmark for portfolio performance analysis.

**Independent Test**: Run `python main.py` and verify that the output charts and console summaries reference "CDI" instead of "SELIC" and that the benchmark data corresponds to the CDI rate.

### Implementation for User Story 1

- [x] T002 [US1] Modify `config.py` to define the CDI series code (12) and name ("CDI") as the new benchmark, replacing SELIC.
- [x] T003 [US1] Update the `get_benchmark_data` function in `data_loader.py` to use the new CDI configuration from `config.py` to download data for series 12 from the BCB.
- [x] T004 [US1] Update `scenarios.py` to ensure it correctly consumes the CDI benchmark data loaded in the previous step.
- [x] T005 [US1] Modify `plotting.py` to use "CDI" as the label in all charts and legends where the benchmark is displayed.
- [x] T006 [US1] Add a unit test to `tests/test_data_loader.py` to verify that the `get_benchmark_data` function correctly downloads and processes the CDI data (series 12).

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. The application should use CDI as its primary benchmark.

---

## Phase 4: User Story 2 - Adjust IPCA+ benchmark monthly (Priority: P2)

**Goal**: Modify the IPCA+ benchmark calculation so that the interest rate adjustment occurs only on the last day of each month.

**Independent Test**: Inspect the generated `ipca_benchmark` DataFrame in `scenarios.py` and confirm that the value only changes on the last calendar day of each month.

### Implementation for User Story 2

- [x] T007 [US2] Modify the `run_monthly_contributions_scenario` and `run_cdb_mixed_scenario` functions in `scenarios.py` to adjust the IPCA+ benchmark calculation logic. The value should be carried forward daily and only recalculated on the last day of the month.
- [x] T008 [US2] Add a unit test to `tests/test_scenarios.py` to verify that the IPCA+ benchmark value remains constant throughout each month, changing only on the last day.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently and correctly.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup, documentation, and validation.

- [x] T009 [P] Update `README.md` to reflect that the project now uses CDI as the default benchmark instead of SELIC.
- [x] T010 [P] Update `GEMINI.md` to reflect the changes in the benchmark.
- [ ] T011 Run all existing and new unit tests to ensure no regressions were introduced.
- [ ] T012 Perform a final validation by running the main script as described in `quickstart.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **User Stories (Phase 3 & 4)**: Depend on Setup completion.
- **Polish (Phase 5)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories.
- **User Story 2 (P2)**: No dependencies on other stories. Can be implemented before, after, or in parallel with US1.

### Within Each User Story

- Core implementation before testing (or vice-versa if following TDD).
- Story complete before moving to next priority.

### Parallel Opportunities

- User Story 1 and User Story 2 can be developed in parallel by different team members.
- Within US1, tasks T005 and T006 can be worked on in parallel after the initial changes in T002, T003, and T004.
- Polish tasks T009 and T010 can be done in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1
3. **STOP and VALIDATE**: Test User Story 1 independently.
4. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup.
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!).
3. Add User Story 2 → Test independently → Deploy/Demo.
4. Each story adds value without breaking previous stories.
