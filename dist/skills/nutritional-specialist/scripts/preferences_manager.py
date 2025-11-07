#!/usr/bin/env python3
"""
User Preferences Manager for Nutritional Specialist Skill

This script manages user food preferences, allergies, goals, and dietary restrictions
in a JSON database file.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

PREFERENCES_FILE = Path.home() / ".claude" / "nutritional_preferences.json"


def ensure_preferences_file() -> None:
    """Ensure the preferences file exists and create it if it doesn't."""
    PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not PREFERENCES_FILE.exists():
        PREFERENCES_FILE.write_text("{}")


def load_preferences() -> Dict[str, Any]:
    """Load user preferences from the JSON file."""
    ensure_preferences_file()
    try:
        with open(PREFERENCES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_preferences(preferences: Dict[str, Any]) -> None:
    """Save user preferences to the JSON file."""
    ensure_preferences_file()
    with open(PREFERENCES_FILE, 'w') as f:
        json.dump(preferences, f, indent=2)


def get_preferences() -> Dict[str, Any]:
    """Get all user preferences."""
    prefs = load_preferences()
    if not prefs:
        return {
            "initialized": False,
            "message": "No preferences found. User needs to complete initial setup."
        }
    return prefs


def set_preferences(preferences: Dict[str, Any]) -> None:
    """Set user preferences with the provided data."""
    prefs = load_preferences()
    prefs.update(preferences)
    prefs["initialized"] = True
    save_preferences(prefs)


def update_preference(key: str, value: Any) -> None:
    """Update a specific preference."""
    prefs = load_preferences()
    prefs[key] = value
    save_preferences(prefs)


def has_preferences() -> bool:
    """Check if user preferences have been initialized."""
    prefs = load_preferences()
    return prefs.get("initialized", False)


def reset_preferences() -> None:
    """Reset all preferences (clear the file)."""
    if PREFERENCES_FILE.exists():
        PREFERENCES_FILE.unlink()


def display_preferences() -> str:
    """Return a formatted string of all preferences."""
    prefs = load_preferences()
    if not prefs or not prefs.get("initialized", False):
        return "No preferences have been set yet."

    output = ["=== User Nutritional Preferences ===\n"]

    sections = [
        ("Goals", "goals"),
        ("Food Preferences", "food_preferences"),
        ("Allergies", "allergies"),
        ("Dislikes", "dislikes"),
        ("Dietary Restrictions", "dietary_restrictions"),
        ("Health Conditions", "health_conditions"),
        ("Cuisine Preferences", "cuisine_preferences"),
        ("Meal Timing Preferences", "meal_timing"),
        ("Additional Notes", "notes")
    ]

    for title, key in sections:
        if key in prefs and prefs[key]:
            output.append(f"\n{title}:")
            value = prefs[key]
            if isinstance(value, list):
                for item in value:
                    output.append(f"  - {item}")
            elif isinstance(value, dict):
                for k, v in value.items():
                    output.append(f"  {k}: {v}")
            else:
                output.append(f"  {value}")

    return "\n".join(output)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 preferences_manager.py get")
        print("  python3 preferences_manager.py display")
        print("  python3 preferences_manager.py has")
        print("  python3 preferences_manager.py reset")
        sys.exit(1)

    command = sys.argv[1]

    if command == "get":
        prefs = get_preferences()
        print(json.dumps(prefs, indent=2))
    elif command == "display":
        print(display_preferences())
    elif command == "has":
        print("true" if has_preferences() else "false")
    elif command == "reset":
        reset_preferences()
        print("Preferences have been reset.")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
