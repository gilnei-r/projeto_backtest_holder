# Research & Decisions

**Feature**: CDB Scenario and Data Persistence

This document records the technical decisions made to resolve ambiguities before implementation.

## 1. Daily Data Caching Mechanism

- **Requirement**: Data (tickers, SELIC, IPCA) should only be downloaded once per day.
- **Unknown**: What is the best method to check if the cached data is up-to-date?

- **Decision**: Check the file's last modification timestamp.
- **Rationale**: We will use Python's standard `os.path.getmtime()` to get the last modification time of a data file. This timestamp will be compared with the current time. If the difference is less than 24 hours (86,400 seconds), we use the cached file. This approach is simple, efficient, and relies only on built-in Python libraries, avoiding external dependencies. It directly addresses `FR-003` and `FR-004`.
- **Alternatives Considered**:
  - **Metadata File**: Storing the last download date in a separate JSON or text file. This was rejected as it adds unnecessary complexity and another file to manage.
  - **Date in Filename**: Appending the date to the CSV filename (e.g., `TICKER_2025-10-28.csv`). This would clutter the data directory and make finding the latest file more complex.

## 2. Data Storage Location

- **Requirement**: Save downloaded data to CSV files.
- **Unknown**: Where should these CSV files be stored?

- **Decision**: A `data/` directory will be created in the project root.
- **Rationale**: The feature specification (`FR-001`, `FR-008`) explicitly requires a `data/` directory. This is a standard convention that separates volatile data from the core source code, keeping the project structure clean. The application will create this directory if it doesn't exist.
- **Alternatives Considered**:
  - **Root Directory**: Storing files in the project root would clutter the main directory and mix data with configuration and source code.
  - `results/` **Directory**: The `results/` directory is intended for final outputs of the backtests (Excel files, plots), not for cached input data.
