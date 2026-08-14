#!/usr/bin/env python3
"""
Nord Terminal Installer for Linux Mint MATE
Script to install the Nord color palette in mate-terminal
"""

import argparse
import subprocess
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Install Nord color palette in mate-terminal"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--revert", action="store_true", help="Restore original terminal configuration"
    )

    args = parser.parse_args()

    if args.dry_run:
        print("[DRY RUN] Simulation mode. No changes will be made.")
        # Future: call dry_run() function
    elif args.revert:
        print("Reverting to original configuration...")
        # Future: call revert() function
    else:
        print("Installing Nord...")
        # Future: call install() function


if __name__ == "__main__":
    main()
