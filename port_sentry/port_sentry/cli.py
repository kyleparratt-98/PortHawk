"""
Command-line interface for PortSentry.

This module provides the CLI class which handles command-line argument parsing
and orchestrates the port monitoring application.
"""

import argparse
import sys
from typing import Optional

from port_sentry.monitor import PortMonitor
from port_sentry.ui import ConsoleUI


class CLI:
    """
    Command-line interface for PortSentry.
    
    This class handles argument parsing and application initialization.
    """
    
    def __init__(self) -> None:
        """Initialize the CLI with argument parser."""
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the argument parser.
        
        Returns:
            Configured argparse.ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            prog="port-sentry",
            description="Real-time port monitoring tool",
            epilog="Press 'q' to quit, 'p' to pause/resume during monitoring"
        )
        
        parser.add_argument(
            "-i", "--interval",
            type=float,
            default=1.0,
            help="Refresh interval in seconds (default: 1.0)"
        )
        
        parser.add_argument(
            "-p", "--protocol",
            type=str,
            choices=["tcp", "tcp6", "udp", "udp6", "all"],
            default="all",
            help="Filter by protocol (default: all)"
        )
        
        parser.add_argument(
            "-P", "--port",
            type=int,
            default=None,
            help="Filter by port number"
        )
        
        parser.add_argument(
            "--version",
            action="version",
            version="PortSentry 1.0.0"
        )
        
        return parser
    
    def parse_args(self) -> argparse.Namespace:
        """
        Parse command-line arguments.
        
        Returns:
            Parsed arguments namespace
        """
        return self.parser.parse_args()
    
    def run(self) -> None:
        """
        Run the PortSentry application.
        
        This method parses command-line arguments, initializes the monitor
        and UI, and starts the monitoring loop.
        """
        try:
            # Parse command-line arguments
            args = self.parse_args()
            
            # Validate interval
            if args.interval <= 0:
                print("Error: Refresh interval must be greater than 0", file=sys.stderr)
                sys.exit(1)
            
            # Convert protocol filter (handle 'all' as None)
            protocol_filter = None
            if args.protocol != "all":
                protocol_filter = args.protocol
            
            # Validate port filter if provided
            if args.port is not None:
                if args.port < 1 or args.port > 65535:
                    print("Error: Port number must be between 1 and 65535", file=sys.stderr)
                    sys.exit(1)
            
            # Initialize monitor with user-specified parameters
            monitor = PortMonitor(
                refresh_interval=args.interval,
                protocol_filter=protocol_filter,
                port_filter=args.port
            )
            
            # Initialize and run the console UI
            ui = ConsoleUI(monitor)
            ui.run()
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nPortSentry terminated by user.", file=sys.stderr)
            sys.exit(0)
        except ValueError as e:
            # Handle value errors (e.g., invalid port number)
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
