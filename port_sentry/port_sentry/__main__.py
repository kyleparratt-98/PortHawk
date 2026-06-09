"""
Main entry point for PortSentry.

This module serves as the entry point when the package is run as a module.
It imports and executes the CLI interface.
"""

import sys
from port_sentry.cli import CLI


def main() -> None:
    """
    Main function to run PortSentry.
    
    This function creates a CLI instance and runs it, handling any
    uncaught exceptions at the top level.
    """
    try:
        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nPortSentry terminated by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Handle any other exceptions
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
