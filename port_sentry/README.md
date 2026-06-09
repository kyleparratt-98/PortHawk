# PortSentry

PortSentry is a real-time port monitoring command-line tool that provides a live-updating, color-coded display of network connections and their associated processes. It's designed for system administrators, developers, and security professionals who need to monitor port activity on their systems.

## Features

- **Real-time Monitoring**: Live updates of port connections with configurable refresh intervals
- **Cross-platform Support**: Works on Windows, macOS, and Linux using `psutil`
- **Color-coded Display**: Uses `rich` library for beautiful terminal output with color-coded connection states
- **Process Information**: Shows PID and process name for each connection
- **Permission Awareness**: Highlights connections where process information access is denied
- **Filtering Options**: Filter by protocol (TCP/UDP) and port number
- **Interactive Controls**: Pause/resume display with 'p', quit with 'q'
- **IPv4/IPv6 Support**: Displays both IPv4 and IPv6 connections
- **Keyboard Shortcuts**: Intuitive controls for pausing and quitting

## Installation

### From PyPI (Recommended)

