<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/stars-potential-gold?style=for-the-badge" alt="Stars">
</p>

<h1 align="center">⚡ PortHawk ⚡</h1>
<p align="center"><i>Real-time port monitoring at the speed of thought — watch every connection flow in your terminal</i></p>

---

## ✨ Why This Exists
You're debugging a rogue process, investigating a security incident, or just trying to understand what's happening on your network stack. You run `netstat` or `lsof` — and get a static wall of text that's outdated the instant it prints. PortHawk gives you a live-updating, color-coded dashboard of every TCP and UDP connection on your machine, with process names, PIDs, and real-time filtering. No polling scripts. No ancient tools. Just instant visibility.

## 🎯 Features
- **Live Streaming**: Connections update in real-time with zero lag — watch ports open and close as they happen
- **Color-Coded UI**: Protocol, state, and access status are colorized for instant scanning
- **Protocol Filtering**: Focus on TCP, TCP6, UDP, UDP6, or watch everything at once
- **Port Filtering**: Zero in on a specific port to track a single service
- **Process Resolution**: See which PID and process name owns each connection (when permissions allow)
- **Keyboard Controls**: Press `p` to pause/resume, `q` to quit cleanly
- **Custom Refresh Rate**: Set the polling interval from milliseconds to seconds
- **Rich Terminal Output**: Beautiful tables powered by the `rich` library

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- `pip` package manager
- Linux, macOS, or Windows (with admin/root for full process info)

### Quick Install
```bash
pip install port-sentry
```

### From Source
```bash
git clone https://github.com/your-username/porthawk.git
cd porthawk
pip install -e .
```

## 🚀 Quick Start
```bash
# Watch all network connections update live
port-sentry
```

## 📖 Usage
```bash
# Monitor only TCP connections
port-sentry --protocol tcp

# Watch a specific port (e.g., 8080) with 0.5s refresh
port-sentry --port 8080 --interval 0.5

# Filter to UDP6 connections
port-sentry --protocol udp6
```

## 🏗️ Architecture
PortHawk is built on three core modules:

- **`monitor.py`**: Contains `PortMonitor` and `ConnectionInfo` — collects raw network connections via `psutil`, applies filters, and wraps each connection in a clean dataclass with resolved process info.
- **`ui.py`**: `ConsoleUI` manages the live terminal display using `rich.Live` and `rich.Table`, handling keyboard input for pause/resume and exit.
- **`cli.py`**: `CLI` parses command-line arguments (`--interval`, `--protocol`, `--port`, `--version`) and wires the monitor to the UI.
- **`utils.py`**: Helper functions for PID-to-process-name resolution, state coloring, and address formatting.

## 📚 API Reference

### `PortMonitor(refresh_interval, protocol_filter, port_filter)`
- **`collect_connections()`** → `List[ConnectionInfo]`: Returns all current filtered connections
- **`run()`**: Continuous monitoring loop (used internally by ConsoleUI)

### `ConnectionInfo`
| Field | Type | Description |
|-------|------|-------------|
| `proto` | `str` | `tcp`, `tcp6`, `udp`, `udp6` |
| `local_addr` | `str` | Local IP address |
| `local_port` | `int` | Local port number |
| `state` | `str` | Connection state (e.g., `LISTEN`, `ESTABLISHED`, `UDP`) |
| `pid` | `Optional[int]` | Process ID |
| `process_name` | `Optional[str]` | Process name (e.g., `nginx`, `python3`) |
| `permission_denied` | `bool` | Whether process info was inaccessible |

### `ConsoleUI(monitor)`
- **`run()`**: Starts the live display loop with keyboard controls

## 🤝 Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs and requesting features
- Setting up a development environment
- Running tests and linting
- Submitting pull requests

## 📄 License
MIT © 2025

---

<p align="center">
  <sub>Built with ❤️ by an autonomous AI software factory</sub>
</p>
