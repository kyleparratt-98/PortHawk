<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/stars-potential-gold?style=for-the-badge" alt="Stars">
</p>

<h1 align="center">⚡ PortSentry ⚡</h1>
<p align="center"><i>Live color-coded port monitoring with process names, right in your terminal</i></p>

---

## ✨ Why This Exists

Every developer and sysadmin has been there: debugging a port conflict, hunting for a rogue process, or trying to understand why your application won't bind to port 8080. `netstat` gives you raw data. `lsof` gives you a firehose. `ss` gives you a snapshot. None of them give you a **live, color-coded, real-time dashboard** of every port on your machine with process names — and none of them handle permission errors gracefully without crashing. PortSentry fills that gap: one command, zero configuration, instant insight.

## 🎯 Features

- **Real-time live display** — Watch ports open, close, and change state as they happen, updated every second
- **Color-coded status indicators** — Green for LISTEN, yellow for ESTABLISHED, red for TIME_WAIT — at a glance
- **Process name resolution** — See exactly which process owns each port, including PID
- **Graceful permission handling** — No crashes on privileged ports; shows `[Permission Denied]` in dim red instead
- **Protocol and port filtering** — Focus on TCP, UDP, or a specific port with `-p tcp` and `-P 8080`
- **Live keyboard controls** — Press `q` to quit, `p` to pause/resume the display
- **Lightweight and cross-platform** — Uses `psutil` and `rich`, works on Linux, macOS, and Windows

## 📦 Installation

### Prerequisites
- Python 3.8 or later
- pip (Python package manager)

### Quick Install
```bash
pip install port-sentry
```

### From Source
```bash
git clone https://github.com/your-username/port-sentry.git
cd port-sentry
pip install -e .
```

## 🚀 Quick Start

Just run it. That's it. No flags, no config files, no setup.

```bash
port-sentry
```

You'll see a live, bordered table of all TCP and UDP connections, with color-coded states, process names, and PIDs. Press `q` to quit, `p` to pause.

## 📖 Usage

```bash
# Monitor with a custom refresh interval (every 2 seconds)
port-sentry -i 2

# Show only TCP connections
port-sentry -p tcp

# Show only UDP connections
port-sentry -p udp

# Filter to a specific port (e.g., 8080)
port-sentry -P 8080

# Combine filters: TCP only, port 80, 3-second refresh
port-sentry -p tcp -P 80 -i 3
```

## 🏗️ Architecture

The codebase is organized into four cleanly separated modules:

- **`monitor.py`** — Core data collection layer. Uses `psutil.net_connections()` to fetch all network connections, resolves process names via PID, and wraps everything in `ConnectionInfo` dataclass objects. Handles `psutil.AccessDenied` gracefully.
- **`ui.py`** — Presentation layer. Uses the `rich` library's `Live` and `Table` components to render a real-time, color-coded, bordered table with keyboard controls (q/p).
- **`cli.py`** — Entry point and argument parsing. Uses `argparse` to handle `-i`, `-p`, `-P`, and `--version` flags. Instantiates `PortMonitor` and `ConsoleUI`.
- **`utils.py`** — Shared utilities: `get_state_color()` maps states to rich styles, `format_address()` formats address tuples, `resolve_pid_info()` safely resolves process names.

Data flow: `CLI` → `PortMonitor.collect_connections()` → `ConnectionInfo` list → `ConsoleUI.make_table()` → `rich.live.Live` display.

## 📚 API Reference

### `PortMonitor(refresh_interval=1.0, protocol_filter=None, port_filter=None)`

The core data collector.

- `collect_connections()` → `List[ConnectionInfo]` — Fetches all current network connections, applies filters, returns a list of `ConnectionInfo` dataclass instances.
- `run()` — Continuous loop (used internally by `ConsoleUI`).

### `ConnectionInfo`

Dataclass with fields: `proto`, `local_addr`, `local_port`, `state`, `pid`, `process_name`, `permission_denied`.

### `ConsoleUI(monitor)`

Handles the live display.

- `make_table(connections)` → `Table` — Builds a `rich.Table` from connection data.
- `run()` — Starts the live display loop with keyboard event handling.

### `CLI()`

Command-line wrapper.

- `parse_args()` → `argparse.Namespace` — Parses command-line arguments.
- `run()` — Parses args, instantiates `PortMonitor` and `ConsoleUI`, starts monitoring.

## 🤝 Contributing

Contributions are welcome! Whether it's bug fixes, feature requests, or documentation improvements, please check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. The project is structured for easy extension — adding JSON/CSV export, sorting, or new filters is straightforward.

## 📄 License

MIT © 2025

---

<p align="center">
  <sub>Built with ❤️ by an autonomous AI software factory</sub>
</p>
