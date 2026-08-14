#!/usr/bin/env python3
"""
Nord Terminal Installer for Linux Mint MATE
Script to install the Nord color palette in mate-terminal
"""

import argparse
import subprocess
import os
import sys
import shutil
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


def check_dependencies():
    """
    Check if required commands (dconf, gsettings) are available.
    Exit with an error message if any is missing.
    """
    required_commands = ["dconf", "gsettings"]
    missing = []

    for cmd in required_commands:
        if shutil.which(cmd) is None:
            missing.append(cmd)

    if missing:
        print(f"Error: Required command(s) not found: {', '.join(missing)}")
        print(
            f"    Please install the package that provides them (usually 'dconf' and 'gsettings' come pre-installed)."
        )
        sys.exit(1)
    else:
        print("Dependencies check passed.")


def backup_default_profile():
    """
    Create backup of the current default profile.
    Returns the path to the back file.
    """
    backup_dir = Path.home() / "nord-backup"
    backup_dir.mkdir(exist_ok=True)

    backup_file = backup_dir / "default_profile.conf"

    if backup_file.exists():
        print(f"    Backup already exists at {backup_file}. Skipping backup.")
        return backup_file

    print("Creating backup of current default profile...")
    try:
        subprocess.run(
            ["dconf", "dump", "/org/mate/terminal/profiles/default/"],
            stdout=open(backup_file, "w"),
            check=True,
            text=True,
        )
        print(f"Backup saved to {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"Failed to create backup: {e}")
        sys.exit(1)


def dry_run():
    """Simulate the installation without making any changes."""
    print("🔍 [DRY RUN] Simulation mode. No changes will be made.\n")

    # Check dependencies (just to verify)
    check_dependencies()

    print("\n Commands that would be executed:")
    print("  1. Backup current profile to ~/nord-backup/default_profile.conf")
    print("  2. Write Nord colors to /org/mate/terminal/profiles/nord/")
    print("     - background-color:  #2E2E34344040")
    print("     - foreground-color:  #D8D8DEDEE9E9")
    print("     - palette:           (16 Nord colors)")
    print("     - visible-name:      'Nord'")
    print("     - use-theme-colors:  false")
    print("  3. Add 'nord' to profile list")
    print("  4. Set 'nord' as default profile")
    print("  5. Restart terminal (pkill mate-terminal)")
    print("\n Dry run completed. No actual changes were made.")


def install():
    """Install the Nord color palette in mate-terminal."""
    print("Reading current settings from default profile...")

    # Read current font and other settings from default profile
    def read_default_setting(key):
        """Read a setting from the default profile using dconf."""
        cmd = ["dconf", "read", f"/org/mate/terminal/profiles/default/{key}"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    # Get current font (or fallback)
    font = read_default_setting("font")
    if font:
        print(f"    -> Using existing font: {font}")
    else:
        font = "'Monospace 12'"
        print(" -> Font not found, using fallback: Monospace 12")

    # Get current cursor shape
    cursor_shape = read_default_setting("cursor-shape") or "'ibeam'"
    cursor_blink = read_default_setting("cursor-blink-mode") or "'off'"
    scrollbar_pos = read_default_setting("scrollbar-position") or "'hidden'"
    silent_bell = read_default_setting("silent-bell") or "true"
    bold_same_fg = read_default_setting("bold-color-same-as-fg") or "true"

    print("Writing Nord colors to dconf...")

    # Write all keys under /org/mate/terminal/profiles/nord
    dconf_cmds = [
        ("visible-name", "'Nord'"),
        ("background-color", f"'{NORD_COLORS["nord0"]}'"),
        ("foreground-color", f"'{NORD_COLORS["nord4"]}'"),
        ("palette", f"'{NORD_PALETTE}'"),
        ("use-theme-colors", "false"),
        ("font", font),
        ("use-system-font", "false"),
        ("cursor-shape", cursor_shape),
        ("cursor-blink-mode", cursor_blink),
        ("scrollbar-position", scrollbar_pos),
        ("silent-bell", silent_bell),
        ("bold-color-same-as-fg", bold_same_fg),
    ]

    for key, value in dconf_cmds:
        cmd = ["dconf", "write", f"/org/mate/terminal/profiles/nord/{key}", value]
        print(f"   → Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to write {key}: {e.stderr}")
            sys.exit(1)

    print("Nord profile created successfully.")

    print("Activating Nord profile...")
    # Add 'nord' to the list of profiles if not already present
    list_cmd = ["gsettings", "get", "org.mate.terminal.global", "profile-list"]
    try:
        result = subprocess.run(list_cmd, capture_output=True, text=True, check=True)
        current_list = result.stdout.strip()
        if "'nord'" not in current_list:
            # Append 'nord' to the list
            if current_list == "[]":
                new_list = "['nord']"
            else:
                # Remove brackets and add 'nord'
                profiles = current_list.strip("[]").replace("'", "").split(",")
                profiles = [p.strip() for p in profiles if p.strip()]
                if "nord" not in profiles:
                    profiles.append("nord")
                new_list = "['" + "', '".join(profiles) + "']"
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.mate.terminal.global",
                    "profile-list",
                    new_list,
                ],
                check=True,
            )
            print(" -> 'nord' added to profile list.")
        else:
            print(" -> 'nord' already in profile list.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update profile list: {e}")
        sys.exit(1)

    # Set 'nord' as default profile
    try:
        subprocess.run(
            [
                "gsettings",
                "set",
                "org.mate.terminal.global",
                "default-profile",
                "'nord'",
            ],
            check=True,
        )
        print(" -> 'nord' set as default profile.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set default profile: {e}")
        sys.exit(1)

    print("Restarting terminal to apply changes...")
    try:
        subprocess.run(["pkill", "mate-terminal"], check=False)
        print(" Terminal restarted. Open a new terminal (Ctrl+Alt+T) to see Nord.")
    except Exception as e:
        print(f" Could not restart terminal automatically: {e}")
        print("  Please close all terminals and open a new one manually.")


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
        dry_run()
        # Future: call dry_run() function
    elif args.revert:
        print("Reverting to original configuration...")
        # Future: call revert() function
    else:
        print("Installing Nord...")
        check_dependencies()
        backup_default_profile()
        install()


if __name__ == "__main__":
    main()
