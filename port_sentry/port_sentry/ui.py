"""
Console user interface for PortSentry.

This module provides the ConsoleUI class which handles the real-time
display of port monitoring information using the rich library.
"""

import time
from typing import List

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text

from port_sentry.monitor import PortMonitor, ConnectionInfo
from port_sentry.utils import get_state_color, format_address


class ConsoleUI:
    """
    Console-based user interface for displaying port monitoring information.
    
    This class manages the real-time updating display using rich library
    components, including a live-updating table and keyboard controls.
    
    Attributes:
        monitor: The PortMonitor instance for data collection
        live: The rich Live display instance
        table: The rich Table instance for displaying connections
        paused: Whether the display update is paused
    """
    
    def __init__(self, monitor: PortMonitor) -> None:
        """
        Initialize the ConsoleUI.
        
        Args:
            monitor: PortMonitor instance for data collection
        """
        self.monitor = monitor
        self.live: Live = None
        self.table: Table = None
        self.paused: bool = False
        self.should_exit: bool = False
        self.console = Console()
        
        # Initialize table structure once
        self._init_table_structure()
    
    def _init_table_structure(self) -> None:
        """Initialize the table structure with columns."""
        self.table = Table(
            title="Port Sentry - Real-time Port Monitor",
            show_header=True,
            header_style="bold magenta"
        )
        
        # Define table columns
        self.table.add_column("Protocol", style="cyan", width=8)
        self.table.add_column("Local Address", style="green", width=25)
        self.table.add_column("Local Port", style="yellow", width=10)
        self.table.add_column("State", style="blue", width=12)
        self.table.add_column("PID", style="magenta", width=8)
        self.table.add_column("Process Name", style="white", width=25)
        self.table.add_column("Access", style="red", width=10)
    
    def make_table(self, connections: List[ConnectionInfo]) -> Table:
        """
        Create a rich Table from a list of ConnectionInfo objects.
        
        Args:
            connections: List of ConnectionInfo objects to display
            
        Returns:
            A rich Table object formatted for display
        """
        # Create a new table with the same structure as self.table
        table = Table(
            title="Port Sentry - Real-time Port Monitor",
            show_header=True,
            header_style="bold magenta"
        )
        
        # Define table columns (same as initialization)
        table.add_column("Protocol", style="cyan", width=8)
        table.add_column("Local Address", style="green", width=25)
        table.add_column("Local Port", style="yellow", width=10)
        table.add_column("State", style="blue", width=12)
        table.add_column("PID", style="magenta", width=8)
        table.add_column("Process Name", style="white", width=25)
        table.add_column("Access", style="red", width=10)
        
        # Sort connections by protocol and port for better readability
        connections.sort(key=lambda x: (x.proto, x.local_port))
        
        # Add rows to the table
        for conn in connections:
            # Get color for state
            state_color = get_state_color(conn.state)
            
            # Format process name with permission denied indicator
            if conn.permission_denied:
                process_display = Text("[Permission Denied]", style="red")
                access_display = Text("DENIED", style="bold red")
            else:
                process_display = Text(conn.process_name or "N/A", style="dim white")
                access_display = Text("OK", style="green")
            
            # Format PID
            pid_display = Text(str(conn.pid) if conn.pid is not None else "N/A", style="dim")
            
            # Format local address using utility function
            local_addr_display = format_address((conn.local_addr, conn.local_port))
            
            # Add row to table
            table.add_row(
                conn.proto.upper(),
                local_addr_display,
                str(conn.local_port),
                Text(conn.state, style=state_color),
                pid_display,
                process_display,
                access_display
            )
        
        return table
    
    def update_display(self) -> None:
        """
        Update the live display with current connection data.
        
        This method is called periodically to refresh the display.
        If paused, it shows a paused message instead of updating data.
        """
        if not self.live:
            return
            
        if self.paused:
            # Create a paused display without collecting data
            paused_table = Table(title="Port Sentry - PAUSED", show_header=False)
            paused_table.add_column("Status", justify="center")
            paused_table.add_row(Text("[PAUSED - Press 'p' to resume]", style="bold yellow"))
            self.live.update(paused_table)
        else:
            # Collect current connections and update display
            connections = self.monitor.collect_connections()
            table = self.make_table(connections)
            self.live.update(table)
    
    def handle_keypress(self, key: str) -> None:
        """
        Handle keyboard input from the user.
        
        Args:
            key: The key pressed by the user
        """
        if key == 'q':
            # Quit the application
            self.should_exit = True
            self.console.print("[yellow]Exiting Port Sentry...[/yellow]")
        elif key == 'p':
            # Toggle pause state
            self.paused = not self.paused
            if self.paused:
                self.console.print("[yellow]Display paused[/yellow]")
            else:
                self.console.print("[green]Display resumed[/green]")
    
    def run(self) -> None:
        """
        Run the main UI loop.
        
        This method initializes the live display and starts the refresh loop.
        It handles keyboard input and manages the display updates.
        """
        try:
            # Initialize table with empty data
            initial_table = self.make_table([])
            
            # Create and start the live display
            with Live(
                initial_table,
                console=self.console,
                refresh_per_second=1/self.monitor.refresh_interval,
                screen=False
            ) as live:
                self.live = live
                
                # Display startup message
                self.console.print("[dim]Port Sentry started. Press 'q' to quit, 'p' to pause.[/dim]")
                
                # Main loop
                while not self.should_exit:
                    # Update the display
                    self.update_display()
                    
                    # Check for keyboard events from Live context
                    # Note: This accesses a protected member of Live, but it's the
                    # recommended way to get keyboard events in this context
                    if hasattr(live, '_keyboard_events') and live._keyboard_events:
                        for key in live._keyboard_events:
                            self.handle_keypress(key)
                        live._keyboard_events.clear()
                    
                    # Sleep for the refresh interval
                    time.sleep(self.monitor.refresh_interval)
                    
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Interrupted by user. Exiting...[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
            self.console.print("[red]Port Sentry encountered an error and will exit.[/red]")
        finally:
            # Cleanup
            self.live = None
            self.table = None
