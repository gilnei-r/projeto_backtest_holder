# Research for "Save Plots and Add MT5 Provider"

## MetaTrader 5 Integration

**Decision**: Use the official `MetaTrader5` Python package for integration with the MetaTrader 5 terminal.

**Rationale**: The `MetaTrader5` package is the official and standard way to connect Python with the MT5 terminal. It is developed by MetaQuotes, the creators of MetaTrader, ensuring the best compatibility and performance. It provides all the necessary functionality for this feature, including connecting to the terminal, and downloading historical data.

**Alternatives considered**:
*   **PyTrader**: A third-party library that acts as a connector. While it might be easier to use, the official library is better supported and more reliable.
*   **Custom solution with ZeroMQ**: Building a custom solution using ZeroMQ would be too complex and time-consuming for this project.

## Saving Matplotlib Plots Without Displaying

**Decision**: Use `matplotlib.pyplot.savefig()` to save the plot to a file, followed by `matplotlib.pyplot.close()` to prevent the plot from being displayed.

**Rationale**: This is the standard and most efficient way to save plots to a file without rendering them on the screen. `savefig()` handles the file creation and format inference, while `close()` releases the memory used by the figure.

**Alternatives considered**:
*   **Using different backends**: It is possible to use a non-interactive backend for matplotlib, but this is a more complex solution and not necessary for this use case. The combination of `savefig()` and `close()` is sufficient and simpler.
