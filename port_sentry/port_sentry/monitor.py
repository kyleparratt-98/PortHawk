"""
Port monitoring core functionality.

This module contains the ConnectionInfo data class and PortMonitor class
which are responsible for collecting and processing network connection data.
"""

from dataclasses import dataclass
from typing import List, Optional
import socket
import time

import psutil

from port_sentry.utils import resolve_pid_info


@dataclass
class ConnectionInfo:
    """
    Data class representing a network connection.
    
    Attributes:
        proto: Protocol type ('tcp', 'tcp6', 'udp', 'udp6')
        local_addr: Local IP address as string
        local_port: Local port number
        state: Connection state string
        pid: Process ID owning the connection, or None
        process_name: Name of the owning process, or None
        permission_denied: Whether access to process info was denied
    """
    proto: str
    local_addr: str
    local_port: int
    state: str
    pid: Optional[int] = None
    process_name: Optional[str] = None
    permission_denied: bool = False


class PortMonitor:
    """
    Monitor for collecting network connection information.
    
    This class handles the collection of network connections from the system,
    filtering by protocol and port if specified, and converting raw connection
    data into ConnectionInfo objects.
    
    Attributes:
        refresh_interval: Time in seconds between data collection cycles
        protocol_filter: Optional protocol filter ('tcp', 'udp', etc.)
        port_filter: Optional port number filter
    """
    
    def __init__(
        self, 
        refresh_interval: float = 1.0, 
        protocol_filter: Optional[str] = None,
        port_filter: Optional[int] = None
    ) -> None:
        """
        Initialize the PortMonitor.
        
        Args:
            refresh_interval: Time in seconds between data collection cycles
            protocol_filter: Optional protocol filter ('tcp', 'udp', etc.)
            port_filter: Optional port number filter
        """
        self.refresh_interval = refresh_interval
        self.protocol_filter = protocol_filter.lower() if protocol_filter else None
        self.port_filter = port_filter
    
    def collect_connections(self) -> List[ConnectionInfo]:
        """
        Collect all current network connections.
        
        Returns:
            A list of ConnectionInfo objects representing current connections
        """
        connections: List[ConnectionInfo] = []
        
        try:
            # Get all network connections
            net_connections = psutil.net_connections(kind='all')
        except (psutil.AccessDenied, psutil.Error):
            # If we can't get connections, return empty list
            # In a production app, we might want to log this
            return connections
        
        for conn in net_connections:
            # Skip connections without local address
            if conn.laddr is None:
                continue
            
            # Extract protocol
            proto = self._get_protocol_name(conn.family, conn.type)
            
            # Apply protocol filter if specified
            if self.protocol_filter and proto != self.protocol_filter:
                continue
            
            # Extract local address and port
            local_addr, local_port = conn.laddr
            
            # Apply port filter if specified
            if self.port_filter and local_port != self.port_filter:
                continue
            
            # Determine connection state
            state = self._get_connection_state(conn.status, proto)
            
            # Resolve process information
            process_name = None
            permission_denied = False
            
            if conn.pid is not None:
                process_name, permission_denied = resolve_pid_info(conn.pid)
            
            # Create ConnectionInfo object
            connection_info = ConnectionInfo(
                proto=proto,
                local_addr=local_addr,
                local_port=local_port,
                state=state,
                pid=conn.pid,
                process_name=process_name,
                permission_denied=permission_denied
            )
            
            connections.append(connection_info)
        
        return connections
    
    def _get_protocol_name(self, family: int, socket_type: int) -> str:
        """
        Convert address family and socket type to protocol name string.
        
        Args:
            family: Address family (e.g., socket.AF_INET, socket.AF_INET6)
            socket_type: Socket type (e.g., socket.SOCK_STREAM, socket.SOCK_DGRAM)
        
        Returns:
            Protocol name string ('tcp', 'tcp6', 'udp', 'udp6', or 'unknown')
        """
        # Determine base protocol
        if socket_type == socket.SOCK_STREAM:
            base_proto = 'tcp'
        elif socket_type == socket.SOCK_DGRAM:
            base_proto = 'udp'
        else:
            return 'unknown'
        
        # Append '6' for IPv6
        if family == socket.AF_INET6:
            return f'{base_proto}6'
        elif family == socket.AF_INET:
            return base_proto
        else:
            return base_proto  # fallback for other address families
    
    def _get_connection_state(self, status: str, proto: str) -> str:
        """
        Determine the display state for a connection.
        
        For UDP connections, always return 'UDP' as per requirements.
        TCP connections use the actual status from psutil.
        
        Args:
            status: Connection status from psutil (may be None or empty)
            proto: Protocol name
            
        Returns:
            State string for display
        """
        if proto.startswith('udp'):
            # Always return 'UDP' for UDP connections as per requirements
            return 'UDP'
        elif status:
            # For TCP, use the actual status
            return status.upper()
        else:
            # Fallback for unknown status
            return 'NONE'
    
    def run(self) -> None:
        """
        Run the monitor in a continuous loop.
        
        This method is kept for API compatibility but the actual
        refresh loop is handled by the ConsoleUI class.
        """
        while True:
            connections = self.collect_connections()
            # In this implementation, the display is handled by ConsoleUI
            # This method could be extended to support other output formats
            time.sleep(self.refresh_interval)
