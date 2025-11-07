#!/usr/bin/env python3
"""
Script Writer Database Manager

Manages user scriptwriting preferences and past scripts.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_FILE = Path.home() / ".claude" / "script_writer.json"


def ensure_db_file() -> None:
    """Ensure the database file exists."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        default_data = {
            "initialized": False,
            "created_at": datetime.now().isoformat(),
            "preferences": {
                "script_types": [],
                "tone": "",
                "target_audience": "",
                "style": "",
                "video_length": "",
                "channel_niche": "",
                "hook_style": "",
                "call_to_action_preference": "",
                "personality": "",
                "use_humor": False,
                "include_statistics": False,
                "storytelling_approach": ""
            },
            "scripts": [],
            "templates": []
        }
        DB_FILE.write_text(json.dumps(default_data, indent=2))


def load_data() -> Dict[str, Any]:
    """Load data from file."""
    ensure_db_file()
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_data(data: Dict[str, Any]) -> None:
    """Save data to file."""
    ensure_db_file()
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# ============================================================================
# PREFERENCES
# ============================================================================

def is_initialized() -> bool:
    """Check if preferences are initialized."""
    data = load_data()
    return data.get("initialized", False)


def get_preferences() -> Dict[str, Any]:
    """Get user preferences."""
    data = load_data()
    return data.get("preferences", {})


def save_preferences(preferences: Dict[str, Any]) -> None:
    """Save user preferences."""
    data = load_data()
    data["preferences"].update(preferences)
    data["initialized"] = True
    data["last_updated"] = datetime.now().isoformat()
    save_data(data)


# ============================================================================
# SCRIPTS
# ============================================================================

def add_script(script: Dict[str, Any]) -> str:
    """Add a new script."""
    data = load_data()
    script_id = str(datetime.now().timestamp())
    script["id"] = script_id
    script["created_at"] = datetime.now().isoformat()
    data["scripts"].append(script)
    save_data(data)
    return script_id


def get_scripts() -> List[Dict[str, Any]]:
    """Get all scripts."""
    data = load_data()
    return data.get("scripts", [])


def get_script_by_id(script_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific script."""
    data = load_data()
    for script in data.get("scripts", []):
        if script.get("id") == script_id:
            return script
    return None


def update_script(script_id: str, updates: Dict[str, Any]) -> bool:
    """Update a script."""
    data = load_data()
    for script in data["scripts"]:
        if script.get("id") == script_id:
            script.update(updates)
            script["updated_at"] = datetime.now().isoformat()
            save_data(data)
            return True
    return False


def delete_script(script_id: str) -> bool:
    """Delete a script."""
    data = load_data()
    for i, script in enumerate(data["scripts"]):
        if script.get("id") == script_id:
            data["scripts"].pop(i)
            save_data(data)
            return True
    return False


# ============================================================================
# TEMPLATES
# ============================================================================

def add_template(template: Dict[str, Any]) -> str:
    """Add a custom template."""
    data = load_data()
    template_id = str(datetime.now().timestamp())
    template["id"] = template_id
    template["created_at"] = datetime.now().isoformat()
    data["templates"].append(template)
    save_data(data)
    return template_id


def get_templates() -> List[Dict[str, Any]]:
    """Get all templates."""
    data = load_data()
    return data.get("templates", [])


# ============================================================================
# STATISTICS
# ============================================================================

def get_stats() -> Dict[str, Any]:
    """Get script statistics."""
    data = load_data()
    scripts = data.get("scripts", [])

    script_types = {}
    tones = {}

    for script in scripts:
        script_type = script.get("type", "Unknown")
        tone = script.get("tone", "Unknown")

        script_types[script_type] = script_types.get(script_type, 0) + 1
        tones[tone] = tones.get(tone, 0) + 1

    return {
        "total_scripts": len(scripts),
        "by_type": script_types,
        "by_tone": tones
    }


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Script Writer Database Manager")
        print("\nUsage:")
        print("  python3 script_db.py is_initialized")
        print("  python3 script_db.py get_preferences")
        print("  python3 script_db.py get_scripts")
        print("  python3 script_db.py stats")
        sys.exit(1)

    command = sys.argv[1]

    if command == "is_initialized":
        print("true" if is_initialized() else "false")
    elif command == "get_preferences":
        print(json.dumps(get_preferences(), indent=2))
    elif command == "get_scripts":
        print(json.dumps(get_scripts(), indent=2))
    elif command == "stats":
        print(json.dumps(get_stats(), indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
