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

# Nord color palette in dconf format (each hex component is doubled)
# Based on the official Nord documentation
NORD_COLORS = {
    "nord0": "#2E2E34344040",  # Polar Night - Darkest
    "nord1": "#3B3B42425252",
    "nord2": "#43434C4C5E5E",
    "nord3": "#4C4C56566A6A",
    "nord4": "#D8D8DEDEE9E9",  # Snow Storm - Lightest (text)
    "nord5": "#E5E5E9E9F0F0",
    "nord6": "#ECECEFEFF4F4",  # Almost white (background for light themes)
    "nord7": "#8F8FBCBCBBBB",  # Frost - Aqua (classes, types)
    "nord8": "#8888C0C0D0D0",  # Frost - Ice (functions, calls)
    "nord9": "#8181A1A1C1C1",  # Frost - Arctic (keywords)
    "nord10": "#5E5E8181ACAC",  # Frost - Deep ocean (pragmas)
    "nord11": "#BFBF61616A6A",  # Aurora - Red (errors)
    "nord12": "#D0D087877070",  # Aurora - Orange (dangerous)
    "nord13": "#EBEBCBCB8B8B",  # Aurora - Yellow (warnings)
    "nord14": "#A3A3BEBE8C8C",  # Aurora - Green (success)
    "nord15": "#B4B48E8EADAD",  # Aurora - Purple (numbers)
}

# ANSI palette order (16 colors) in dconf format
# Index: 0=black, 1=red, 2=green, 3=yellow, 4=blue, 5=magenta, 6=cyan, 7=white
# Then bright versions: 8-15
NORD_PALETTE = (
    f"{NORD_COLORS['nord0']}:{NORD_COLORS['nord11']}:{NORD_COLORS['nord14']}:{NORD_COLORS['nord13']}:"
    f"{NORD_COLORS['nord9']}:{NORD_COLORS['nord15']}:{NORD_COLORS['nord8']}:{NORD_COLORS['nord4']}:"
    f"{NORD_COLORS['nord3']}:{NORD_COLORS['nord11']}:{NORD_COLORS['nord14']}:{NORD_COLORS['nord13']}:"
    f"{NORD_COLORS['nord9']}:{NORD_COLORS['nord15']}:{NORD_COLORS['nord8']}:{NORD_COLORS['nord6']}"
)


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
