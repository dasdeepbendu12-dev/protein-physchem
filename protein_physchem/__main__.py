"""Entry point for `python -m protparam_offline`."""
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
