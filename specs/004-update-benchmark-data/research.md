# Research: Update Benchmark Data

## BCB API Rate Limits and Usage Policies

- **Decision**: Assume no strict rate limits for the BCB SGS API.
- **Rationale**: Could not find official documentation for the `python-bcb` library or the BCB SGS API regarding rate limits. The existing implementation includes a retry mechanism, which should be sufficient for the project's needs.
- **Alternatives considered**: None.

## CDI Data Structure

- **Decision**: The data structure for the CDI series (code 12) is expected to be identical to the existing SELIC series data structure.
- **Rationale**: The `download_bcb_series` function in `data_loader.py` is generic and creates a pandas DataFrame with a single column named after the `series_name` parameter. The new code will call this function with `'cdi'` as the `series_name`, resulting in a DataFrame with a 'cdi' column, which is consistent with the existing implementation for SELIC.
- **Alternatives considered**: None.