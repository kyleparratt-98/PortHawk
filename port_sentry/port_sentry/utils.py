"""
Utility functions for the PortSentry port monitoring tool.

This module provides helper functions for formatting, color coding,
and process information resolution used throughout the application.
"""

import socket
from typing import Optional, Tuple
import psutil


def get_state_color(state: str) -> str:
    """
    Return a color name for a given connection state.
    
    Args:
        state: The connection state string (e.g., 'LISTEN', 'ESTABLISHED', 'UDP')
    
    Returns:
        A color name string compatible with the rich library.
    """
    state = state.upper()
    
    # Define color mappings for different connection states
    if state in ['LISTEN', 'UDP']:
        return 'green'
    elif state in ['ESTABLISHED', 'SYN_SENT', 'SYN_RECV']:
        return 'blue'
    elif state in ['FIN_WAIT1', 'FIN_WAIT2', 'TIME_WAIT', 'CLOSE_WAIT', 
                   'CLOSING', 'LAST_ACK']:
        return 'yellow'
    elif state in ['CLOSED', 'NONE']:
        return 'dim white'
    else:
        return 'red'  # Unknown or error states


def format_address(addr: Optional[Tuple[str, int]]) -> str:
    """
    Format an IP address and port tuple into a human-readable string.
    
    Args:
        addr: A tuple of (ip_address, port), or None
    
    Returns:
        Formatted string in the format 'ip_address:port', or empty string if addr is None
    """
    if addr is None:
        return ''
    
    ip, port = addr
    
    # Handle IPv6 addresses
    if ':' in ip and ip != '::':
        # IPv6 address, wrap in brackets
        return f'[{ip}]:{port}'
    else:
        return f'{ip}:{port}'


def resolve_pid_info(pid: int) -> Tuple[Optional[str], bool]:
    """
    Resolve process information for a given PID.
    
    Args:
        pid: Process ID to look up
    
    Returns:
        A tuple of (process_name, permission_denied)
        - process_name: The name of the process, or None if not found
        - permission_denied: True if access to process info was denied
    """
    try:
        process = psutil.Process(pid)
        process_name = process.name()
        return (process_name, False)
    except psutil.NoSuchProcess:
        # Process no longer exists
        return (None, False)
    except psutil.AccessDenied:
        # Permission denied to access process info
        return (None, True)
    except Exception:
        # Any other exception
        return (None, False)
