#!/usr/bin/env python3
"""
Quick Task Management Helper

Provides convenient functions for common task operations.
"""

import sys
from pathlib import Path

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from assistant_db import (
    add_task, get_tasks, update_task, complete_task,
    delete_task, add_context
)
import json
from datetime import datetime, timedelta


def list_tasks_formatted() -> str:
    """Return formatted list of pending tasks."""
    tasks_data = get_tasks()
    tasks = tasks_data.get("tasks", [])

    if not tasks:
        return "No pending tasks."

    output = ["=== Pending Tasks ===\n"]

    # Sort by priority and due date
    priority_order = {"high": 0, "medium": 1, "low": 2, "": 3}
    sorted_tasks = sorted(
        tasks,
        key=lambda t: (
            priority_order.get(t.get("priority", ""), 3),
            t.get("due_date", "9999-12-31")
        )
    )

    for i, task in enumerate(sorted_tasks, 1):
        priority = task.get("priority", "")
        priority_str = f"[{priority.upper()}] " if priority else ""

        due_date = task.get("due_date", "")
        due_str = f" (Due: {due_date})" if due_date else ""

        category = task.get("category", "")
        cat_str = f" [{category}]" if category else ""

        output.append(f"{i}. {priority_str}{task.get('title', 'Untitled')}{due_str}{cat_str}")

        if task.get("description"):
            output.append(f"   {task['description']}")

        output.append(f"   ID: {task['id']}\n")

    return "\n".join(output)


def add_quick_task(title: str, priority: str = "", due_date: str = "",
                   category: str = "", description: str = "") -> str:
    """Add a task with convenient parameters."""
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "pending"
    }

    if due_date:
        task["due_date"] = due_date

    add_task(task)
    add_context("interaction", f"Added task: {title}", "normal")

    return f"✓ Task added: {title}"


def get_overdue_tasks() -> List[Dict]:
    """Get tasks that are overdue."""
    tasks_data = get_tasks()
    tasks = tasks_data.get("tasks", [])
    today = datetime.now().date()

    overdue = []
    for task in tasks:
        if "due_date" in task:
            due = datetime.fromisoformat(task["due_date"]).date()
            if due < today:
                overdue.append(task)

    return overdue


def get_tasks_by_category(category: str) -> List[Dict]:
    """Get tasks filtered by category."""
    tasks_data = get_tasks()
    tasks = tasks_data.get("tasks", [])

    return [t for t in tasks if t.get("category", "").lower() == category.lower()]


def get_today_tasks() -> List[Dict]:
    """Get tasks due today."""
    tasks_data = get_tasks()
    tasks = tasks_data.get("tasks", [])
    today = datetime.now().date().isoformat()

    return [t for t in tasks if t.get("due_date", "") == today]


def get_this_week_tasks() -> List[Dict]:
    """Get tasks due this week."""
    tasks_data = get_tasks()
    tasks = tasks_data.get("tasks", [])

    today = datetime.now().date()
    week_end = today + timedelta(days=7)

    week_tasks = []
    for task in tasks:
        if "due_date" in task:
            due = datetime.fromisoformat(task["due_date"]).date()
            if today <= due <= week_end:
                week_tasks.append(task)

    return week_tasks


def mark_complete_by_title(title: str) -> str:
    """Complete a task by its title (fuzzy match)."""
    tasks_data = get_tasks()
    tasks = tasks_data.get("tasks", [])

    title_lower = title.lower()
    for task in tasks:
        if title_lower in task.get("title", "").lower():
            complete_task(task["id"])
            add_context("interaction", f"Completed task: {task['title']}", "normal")
            return f"✓ Completed: {task['title']}"

    return f"✗ Task not found: {title}"


if __name__ == "__main__":
    import sys
    from typing import List

    if len(sys.argv) < 2:
        print("Task Helper")
        print("\nUsage:")
        print("  python3 task_helper.py list")
        print("  python3 task_helper.py add <title> [priority] [due_date] [category]")
        print("  python3 task_helper.py complete <task_id>")
        print("  python3 task_helper.py overdue")
        print("  python3 task_helper.py today")
        print("  python3 task_helper.py week")
        print("  python3 task_helper.py category <category_name>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        print(list_tasks_formatted())
    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: Title required")
            sys.exit(1)
        title = sys.argv[2]
        priority = sys.argv[3] if len(sys.argv) > 3 else ""
        due_date = sys.argv[4] if len(sys.argv) > 4 else ""
        category = sys.argv[5] if len(sys.argv) > 5 else ""
        print(add_quick_task(title, priority, due_date, category))
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: Task ID required")
            sys.exit(1)
        task_id = float(sys.argv[2])
        if complete_task(task_id):
            print(f"✓ Task {task_id} completed")
        else:
            print(f"✗ Task {task_id} not found")
    elif command == "overdue":
        tasks = get_overdue_tasks()
        print(json.dumps(tasks, indent=2))
    elif command == "today":
        tasks = get_today_tasks()
        print(json.dumps(tasks, indent=2))
    elif command == "week":
        tasks = get_this_week_tasks()
        print(json.dumps(tasks, indent=2))
    elif command == "category":
        if len(sys.argv) < 3:
            print("Error: Category name required")
            sys.exit(1)
        category = sys.argv[2]
        tasks = get_tasks_by_category(category)
        print(json.dumps(tasks, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
