<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python" alt="Python Version">
</p>

<h1 align="center">⚡ PortSentry ⚡</h1>
<p align="center"><i>Real-time port monitoring for your terminal — live, color-coded, and permission-aware.</i></p>

---

## ✨ Why This Exists

You're trying to debug why your microservice isn't listening on port 8080, so you run `netstat` and get a wall of text. Then `lsof` — more text. Then `ss` — slightly faster text. None of it updates live. None of it color-codes states. And when you hit a privileged port, you get a cryptic permission error and the whole command fails. PortSentry fixes all of that: one command gives you a live-updating, bordered table with green LISTEN, yellow ESTABLISHED, and red TIME_WAIT indicators — plus process names and graceful handling of permission-denied errors. It's the port monitoring tool you didn't know you needed.

## 🎯 Features

- **Live-updating table** — Real-time refresh of all TCP and UDP connections with a smooth, flicker-free display using the `rich` library.
- **Color-coded states** — Green for LISTEN, yellow for ESTABLISHED, red for TIME_WAIT — instantly identify connection status at a glance.
- **Process name resolution** — See exactly which process (by name and PID) owns each port, with `[Permission Denied]` fallback for privileged ports.
- **Protocol and port filtering** — Filter by TCP, UDP, or any specific port number via CLI flags.
- **Graceful error handling** — Permission errors on ports < 1024 are caught and displayed as `[root required]` instead of crashing the tool.
- **Keyboard controls** — Press `q` to quit, `p` to pause/resume the live display, `r` to force a refresh.
- **Zero-config startup** — Install with pip and run. No config files, no daemon setup.

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- On Linux: `psutil` may require `python3-dev` or `gcc` for compilation; on most systems it installs without issue.

### Quick Install

```bash
pip install port-sentry
```

### From Source

```bash
git clone https://github.com/yourusername/port-sentry.git
cd port-sentry
pip install -e .
```

## 🚀 Quick Start

```bash
# Show all TCP and UDP connections, updating every second
port-sentry
```

This will display a live-updating table with columns: Protocol, Local Address, Local Port, State, PID, Process Name, and Access. Press `q` to quit, `p` to pause.

## 📖 Usage

```bash
# Monitor only TCP connections, refresh every 2 seconds
port-sentry -i 2 -p tcp

# Filter by port 8080 (HTTP)
port-sentry -P 8080

# Show only UDP connections
port-sentry -p udp

# Display help and all available options
port-sentry --help
```

## 🏗️ Architecture

PortSentry is structured into four main modules:

- **`monitor.py`** — Contains `ConnectionInfo` (data class) and `PortMonitor` (collects connections via `psutil.net_connections()`, applies filters, and resolves process names). Handles permission errors gracefully.
- **`ui.py`** — Contains `ConsoleUI`, which uses the `rich` library's `Live` and `Table` components to render a live-updating, color-coded display. Handles keyboard input for pause/quit/refresh.
- **`cli.py`** — Contains `CLI`, which parses command-line arguments (`-i`, `-p`, `-P`, `--version`) using `argparse` and orchestrates the monitor and UI.
- **`utils.py`** — Contains helper functions: `get_state_color()` (maps state strings to rich color names), `format_address()` (formats socket address tuples), and `resolve_pid_info()` (resolves PID to process name, catching `psutil.AccessDenied`).

The data flow is straightforward: CLI → PortMonitor (collects data) → ConsoleUI (renders table via rich Live). The refresh loop runs in ConsoleUI, calling `collect_connections()` on each cycle.

## 📚 API Reference

### `ConnectionInfo` (dataclass)

| Attribute | Type | Description |
|-----------|------|-------------|
| `proto` | `str` | Protocol (`tcp`, `tcp6`, `udp`, `udp6`) |
| `local_addr` | `str` | Local IP address |
| `local_port` | `int` | Local port number |
| `state` | `str` | Connection state (`LISTEN`, `ESTABLISHED`, `TIME_WAIT`, `UDP`) |
| `pid` | `Optional[int]` | Process ID |
| `process_name` | `Optional[str]` | Process name |
| `permission_denied` | `bool` | Whether process info was inaccessible |

### `PortMonitor(refresh_interval=1.0, protocol_filter=None, port_filter=None)`

- `collect_connections()` → `List[ConnectionInfo]`: Collects and filters current network connections.
- `run()`: Continuous loop (for API compatibility; actual loop is in ConsoleUI).

### `ConsoleUI(monitor)`

- `make_table(connections)` → `rich.table.Table`: Creates a formatted table from connection data.
- `run()`: Starts the live display loop with keyboard handling.

### `CLI()`

- `parse_args()` → `argparse.Namespace`: Parses command-line arguments.
- `run()`: Initializes monitor and UI, starts monitoring.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit issues, feature requests, and pull requests. This project follows a standard fork-and-pull workflow.

## 📄 License

MIT © 2025

---

<p align="center">
  <sub>Built with ❤️ by an autonomous AI software factory</sub>
</p>
