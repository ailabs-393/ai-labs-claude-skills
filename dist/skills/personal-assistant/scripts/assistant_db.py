#!/usr/bin/env python3
"""
Personal Assistant Database Manager

Manages user profile, schedule, preferences, tasks, and context information
with intelligent data retention and cleanup.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

DB_DIR = Path.home() / ".claude" / "personal_assistant"
PROFILE_FILE = DB_DIR / "profile.json"
TASKS_FILE = DB_DIR / "tasks.json"
SCHEDULE_FILE = DB_DIR / "schedule.json"
CONTEXT_FILE = DB_DIR / "context.json"


def ensure_db_files() -> None:
    """Ensure all database files exist."""
    DB_DIR.mkdir(parents=True, exist_ok=True)

    default_files = {
        PROFILE_FILE: {
            "initialized": False,
            "created_at": datetime.now().isoformat()
        },
        TASKS_FILE: {
            "tasks": [],
            "completed_tasks": []
        },
        SCHEDULE_FILE: {
            "working_hours": {},
            "recurring_events": [],
            "one_time_events": []
        },
        CONTEXT_FILE: {
            "recent_interactions": [],
            "important_notes": [],
            "temporary_context": []
        }
    }

    for file_path, default_data in default_files.items():
        if not file_path.exists():
            file_path.write_text(json.dumps(default_data, indent=2))


def load_json(file_path: Path) -> Dict[str, Any]:
    """Load JSON from file."""
    ensure_db_files()
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_json(file_path: Path, data: Dict[str, Any]) -> None:
    """Save JSON to file."""
    ensure_db_files()
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


# ============================================================================
# PROFILE MANAGEMENT
# ============================================================================

def get_profile() -> Dict[str, Any]:
    """Get user profile."""
    return load_json(PROFILE_FILE)


def save_profile(profile_data: Dict[str, Any]) -> None:
    """Save user profile."""
    profile = load_json(PROFILE_FILE)
    profile.update(profile_data)
    profile["initialized"] = True
    profile["last_updated"] = datetime.now().isoformat()
    save_json(PROFILE_FILE, profile)


def has_profile() -> bool:
    """Check if profile is initialized."""
    profile = load_json(PROFILE_FILE)
    return profile.get("initialized", False)


# ============================================================================
# TASK MANAGEMENT
# ============================================================================

def get_tasks(include_completed: bool = False) -> Dict[str, List[Dict]]:
    """Get all tasks."""
    tasks_data = load_json(TASKS_FILE)
    if include_completed:
        return tasks_data
    return {"tasks": tasks_data.get("tasks", [])}


def add_task(task: Dict[str, Any]) -> None:
    """Add a new task."""
    tasks_data = load_json(TASKS_FILE)
    task["id"] = datetime.now().timestamp()
    task["created_at"] = datetime.now().isoformat()
    task["status"] = task.get("status", "pending")
    tasks_data["tasks"].append(task)
    save_json(TASKS_FILE, tasks_data)


def update_task(task_id: float, updates: Dict[str, Any]) -> bool:
    """Update an existing task."""
    tasks_data = load_json(TASKS_FILE)
    for task in tasks_data["tasks"]:
        if task["id"] == task_id:
            task.update(updates)
            task["updated_at"] = datetime.now().isoformat()
            save_json(TASKS_FILE, tasks_data)
            return True
    return False


def complete_task(task_id: float) -> bool:
    """Mark a task as completed and move it to completed tasks."""
    tasks_data = load_json(TASKS_FILE)
    for i, task in enumerate(tasks_data["tasks"]):
        if task["id"] == task_id:
            task["status"] = "completed"
            task["completed_at"] = datetime.now().isoformat()
            tasks_data["tasks"].pop(i)
            tasks_data["completed_tasks"].append(task)
            save_json(TASKS_FILE, tasks_data)
            return True
    return False


def delete_task(task_id: float) -> bool:
    """Delete a task."""
    tasks_data = load_json(TASKS_FILE)
    for i, task in enumerate(tasks_data["tasks"]):
        if task["id"] == task_id:
            tasks_data["tasks"].pop(i)
            save_json(TASKS_FILE, tasks_data)
            return True
    return False


# ============================================================================
# SCHEDULE MANAGEMENT
# ============================================================================

def get_schedule() -> Dict[str, Any]:
    """Get user schedule."""
    return load_json(SCHEDULE_FILE)


def save_schedule(schedule_data: Dict[str, Any]) -> None:
    """Save schedule information."""
    schedule = load_json(SCHEDULE_FILE)
    schedule.update(schedule_data)
    save_json(SCHEDULE_FILE, schedule)


def add_event(event: Dict[str, Any], recurring: bool = False) -> None:
    """Add a calendar event."""
    schedule = load_json(SCHEDULE_FILE)
    event["id"] = datetime.now().timestamp()
    event["created_at"] = datetime.now().isoformat()

    if recurring:
        schedule["recurring_events"].append(event)
    else:
        schedule["one_time_events"].append(event)

    save_json(SCHEDULE_FILE, schedule)


def get_events(days_ahead: int = 7) -> List[Dict[str, Any]]:
    """Get upcoming events for the next N days."""
    schedule = load_json(SCHEDULE_FILE)
    cutoff_date = datetime.now() + timedelta(days=days_ahead)

    upcoming = []
    for event in schedule.get("one_time_events", []):
        if "date" in event:
            event_date = datetime.fromisoformat(event["date"])
            if event_date <= cutoff_date:
                upcoming.append(event)

    # Include all recurring events
    upcoming.extend(schedule.get("recurring_events", []))

    return upcoming


# ============================================================================
# CONTEXT MANAGEMENT (Intelligent Data Retention)
# ============================================================================

def add_context(context_type: str, content: str, importance: str = "normal") -> None:
    """
    Add context information.

    Args:
        context_type: "interaction", "note", or "temporary"
        content: The context content
        importance: "low", "normal", or "high"
    """
    context_data = load_json(CONTEXT_FILE)

    context_item = {
        "id": datetime.now().timestamp(),
        "content": content,
        "importance": importance,
        "timestamp": datetime.now().isoformat()
    }

    if context_type == "interaction":
        context_data["recent_interactions"].append(context_item)
    elif context_type == "note":
        context_data["important_notes"].append(context_item)
    elif context_type == "temporary":
        context_data["temporary_context"].append(context_item)

    save_json(CONTEXT_FILE, context_data)


def get_context(context_type: Optional[str] = None) -> Dict[str, Any]:
    """Get context information."""
    context_data = load_json(CONTEXT_FILE)
    if context_type:
        return {context_type: context_data.get(context_type, [])}
    return context_data


def cleanup_old_data(days_to_keep: int = 30) -> Dict[str, int]:
    """
    Intelligently clean up old data.

    - Remove completed tasks older than days_to_keep
    - Remove old temporary context
    - Keep important notes regardless of age
    - Remove old one-time events

    Returns count of items removed.
    """
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    removed_counts = {
        "tasks": 0,
        "events": 0,
        "interactions": 0,
        "temporary": 0
    }

    # Clean up old completed tasks
    tasks_data = load_json(TASKS_FILE)
    original_count = len(tasks_data.get("completed_tasks", []))
    tasks_data["completed_tasks"] = [
        task for task in tasks_data.get("completed_tasks", [])
        if datetime.fromisoformat(task.get("completed_at", datetime.now().isoformat())) > cutoff_date
    ]
    removed_counts["tasks"] = original_count - len(tasks_data["completed_tasks"])
    save_json(TASKS_FILE, tasks_data)

    # Clean up old one-time events
    schedule = load_json(SCHEDULE_FILE)
    original_count = len(schedule.get("one_time_events", []))
    schedule["one_time_events"] = [
        event for event in schedule.get("one_time_events", [])
        if "date" not in event or datetime.fromisoformat(event["date"]) > cutoff_date
    ]
    removed_counts["events"] = original_count - len(schedule["one_time_events"])
    save_json(SCHEDULE_FILE, schedule)

    # Clean up old context (keep important notes)
    context_data = load_json(CONTEXT_FILE)

    # Keep only recent interactions
    original_count = len(context_data.get("recent_interactions", []))
    context_data["recent_interactions"] = [
        item for item in context_data.get("recent_interactions", [])
        if datetime.fromisoformat(item.get("timestamp", datetime.now().isoformat())) > cutoff_date
        or item.get("importance") == "high"
    ]
    removed_counts["interactions"] = original_count - len(context_data["recent_interactions"])

    # Remove all temporary context older than 7 days
    temp_cutoff = datetime.now() - timedelta(days=7)
    original_count = len(context_data.get("temporary_context", []))
    context_data["temporary_context"] = [
        item for item in context_data.get("temporary_context", [])
        if datetime.fromisoformat(item.get("timestamp", datetime.now().isoformat())) > temp_cutoff
    ]
    removed_counts["temporary"] = original_count - len(context_data["temporary_context"])

    save_json(CONTEXT_FILE, context_data)

    return removed_counts


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def reset_all() -> None:
    """Reset all data (use with caution)."""
    for file_path in [PROFILE_FILE, TASKS_FILE, SCHEDULE_FILE, CONTEXT_FILE]:
        if file_path.exists():
            file_path.unlink()
    ensure_db_files()


def export_all() -> Dict[str, Any]:
    """Export all data as a single JSON object."""
    return {
        "profile": get_profile(),
        "tasks": get_tasks(include_completed=True),
        "schedule": get_schedule(),
        "context": get_context(),
        "exported_at": datetime.now().isoformat()
    }


def get_summary() -> Dict[str, Any]:
    """Get a summary of all stored data."""
    tasks_data = get_tasks(include_completed=True)
    schedule = get_schedule()
    context_data = get_context()

    return {
        "profile_initialized": has_profile(),
        "pending_tasks": len(tasks_data.get("tasks", [])),
        "completed_tasks": len(tasks_data.get("completed_tasks", [])),
        "recurring_events": len(schedule.get("recurring_events", [])),
        "upcoming_events": len(schedule.get("one_time_events", [])),
        "recent_interactions": len(context_data.get("recent_interactions", [])),
        "important_notes": len(context_data.get("important_notes", [])),
        "temporary_context": len(context_data.get("temporary_context", []))
    }


# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Personal Assistant Database Manager")
        print("\nUsage:")
        print("  python3 assistant_db.py has_profile")
        print("  python3 assistant_db.py get_profile")
        print("  python3 assistant_db.py get_tasks")
        print("  python3 assistant_db.py get_schedule")
        print("  python3 assistant_db.py get_context")
        print("  python3 assistant_db.py summary")
        print("  python3 assistant_db.py cleanup [days]")
        print("  python3 assistant_db.py export")
        print("  python3 assistant_db.py reset")
        sys.exit(1)

    command = sys.argv[1]

    if command == "has_profile":
        print("true" if has_profile() else "false")
    elif command == "get_profile":
        print(json.dumps(get_profile(), indent=2))
    elif command == "get_tasks":
        print(json.dumps(get_tasks(include_completed=True), indent=2))
    elif command == "get_schedule":
        print(json.dumps(get_schedule(), indent=2))
    elif command == "get_context":
        print(json.dumps(get_context(), indent=2))
    elif command == "summary":
        print(json.dumps(get_summary(), indent=2))
    elif command == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        removed = cleanup_old_data(days)
        print(f"Cleaned up old data (kept last {days} days):")
        print(json.dumps(removed, indent=2))
    elif command == "export":
        print(json.dumps(export_all(), indent=2))
    elif command == "reset":
        confirm = input("Are you sure you want to reset all data? (yes/no): ")
        if confirm.lower() == "yes":
            reset_all()
            print("All data has been reset.")
        else:
            print("Reset cancelled.")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
