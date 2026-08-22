#!/usr/bin/env python
"""Django's command-line utility for TaskSwap."""
import os
import sys


def main():
    """Run administrative commands against the local TaskSwap project."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasksite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django is required. Install dependencies from requirements.txt.") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
