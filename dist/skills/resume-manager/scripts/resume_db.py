#!/usr/bin/env python3
"""
Resume Database Manager

Manages user's professional profile, experiences, projects, education,
skills, and other resume-relevant information.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_FILE = Path.home() / ".claude" / "resume_data.json"


def ensure_db_file() -> None:
    """Ensure the database file exists."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        default_data = {
            "initialized": False,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "personal_info": {},
            "experiences": [],
            "projects": [],
            "education": [],
            "skills": {},
            "certifications": [],
            "publications": [],
            "awards": [],
            "volunteer": [],
            "languages": [],
            "interests": []
        }
        DB_FILE.write_text(json.dumps(default_data, indent=2))


def load_data() -> Dict[str, Any]:
    """Load resume data from file."""
    ensure_db_file()
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_data(data: Dict[str, Any]) -> None:
    """Save resume data to file."""
    ensure_db_file()
    data["last_updated"] = datetime.now().isoformat()
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# ============================================================================
# INITIALIZATION & PROFILE
# ============================================================================

def is_initialized() -> bool:
    """Check if resume data is initialized."""
    data = load_data()
    return data.get("initialized", False)


def initialize_from_data(resume_data: Dict[str, Any]) -> None:
    """Initialize database with parsed resume data."""
    data = load_data()
    data.update(resume_data)
    data["initialized"] = True
    save_data(data)


def get_personal_info() -> Dict[str, Any]:
    """Get personal information."""
    data = load_data()
    return data.get("personal_info", {})


def update_personal_info(info: Dict[str, Any]) -> None:
    """Update personal information."""
    data = load_data()
    data["personal_info"].update(info)
    save_data(data)


# ============================================================================
# WORK EXPERIENCE
# ============================================================================

def get_experiences() -> List[Dict[str, Any]]:
    """Get all work experiences."""
    data = load_data()
    return data.get("experiences", [])


def add_experience(experience: Dict[str, Any]) -> None:
    """Add a work experience."""
    data = load_data()
    experience["id"] = datetime.now().timestamp()
    experience["added_at"] = datetime.now().isoformat()
    data["experiences"].append(experience)
    save_data(data)


def update_experience(exp_id: float, updates: Dict[str, Any]) -> bool:
    """Update a work experience."""
    data = load_data()
    for exp in data["experiences"]:
        if exp.get("id") == exp_id:
            exp.update(updates)
            save_data(data)
            return True
    return False


def delete_experience(exp_id: float) -> bool:
    """Delete a work experience."""
    data = load_data()
    for i, exp in enumerate(data["experiences"]):
        if exp.get("id") == exp_id:
            data["experiences"].pop(i)
            save_data(data)
            return True
    return False


def get_relevant_experiences(keywords: List[str], limit: int = None) -> List[Dict[str, Any]]:
    """Get experiences relevant to given keywords."""
    experiences = get_experiences()
    scored_experiences = []

    for exp in experiences:
        score = 0
        searchable_text = (
            exp.get("company", "") + " " +
            exp.get("position", "") + " " +
            exp.get("description", "") + " " +
            " ".join(exp.get("highlights", [])) + " " +
            " ".join(exp.get("technologies", []))
        ).lower()

        for keyword in keywords:
            if keyword.lower() in searchable_text:
                score += searchable_text.count(keyword.lower())

        if score > 0:
            exp_with_score = exp.copy()
            exp_with_score["_relevance_score"] = score
            scored_experiences.append(exp_with_score)

    # Sort by relevance score
    scored_experiences.sort(key=lambda x: x["_relevance_score"], reverse=True)

    if limit:
        return scored_experiences[:limit]
    return scored_experiences


# ============================================================================
# PROJECTS
# ============================================================================

def get_projects() -> List[Dict[str, Any]]:
    """Get all projects."""
    data = load_data()
    return data.get("projects", [])


def add_project(project: Dict[str, Any]) -> None:
    """Add a project."""
    data = load_data()
    project["id"] = datetime.now().timestamp()
    project["added_at"] = datetime.now().isoformat()
    data["projects"].append(project)
    save_data(data)


def update_project(proj_id: float, updates: Dict[str, Any]) -> bool:
    """Update a project."""
    data = load_data()
    for proj in data["projects"]:
        if proj.get("id") == proj_id:
            proj.update(updates)
            save_data(data)
            return True
    return False


def delete_project(proj_id: float) -> bool:
    """Delete a project."""
    data = load_data()
    for i, proj in enumerate(data["projects"]):
        if proj.get("id") == proj_id:
            data["projects"].pop(i)
            save_data(data)
            return True
    return False


def get_relevant_projects(keywords: List[str], limit: int = None) -> List[Dict[str, Any]]:
    """Get projects relevant to given keywords."""
    projects = get_projects()
    scored_projects = []

    for proj in projects:
        score = 0
        searchable_text = (
            proj.get("name", "") + " " +
            proj.get("description", "") + " " +
            " ".join(proj.get("highlights", [])) + " " +
            " ".join(proj.get("technologies", []))
        ).lower()

        for keyword in keywords:
            if keyword.lower() in searchable_text:
                score += searchable_text.count(keyword.lower())

        if score > 0:
            proj_with_score = proj.copy()
            proj_with_score["_relevance_score"] = score
            scored_projects.append(proj_with_score)

    scored_projects.sort(key=lambda x: x["_relevance_score"], reverse=True)

    if limit:
        return scored_projects[:limit]
    return scored_projects


# ============================================================================
# EDUCATION
# ============================================================================

def get_education() -> List[Dict[str, Any]]:
    """Get all education entries."""
    data = load_data()
    return data.get("education", [])


def add_education(edu: Dict[str, Any]) -> None:
    """Add an education entry."""
    data = load_data()
    edu["id"] = datetime.now().timestamp()
    data["education"].append(edu)
    save_data(data)


def update_education(edu_id: float, updates: Dict[str, Any]) -> bool:
    """Update an education entry."""
    data = load_data()
    for edu in data["education"]:
        if edu.get("id") == edu_id:
            edu.update(updates)
            save_data(data)
            return True
    return False


def delete_education(edu_id: float) -> bool:
    """Delete an education entry."""
    data = load_data()
    for i, edu in enumerate(data["education"]):
        if edu.get("id") == edu_id:
            data["education"].pop(i)
            save_data(data)
            return True
    return False


# ============================================================================
# SKILLS
# ============================================================================

def get_skills() -> Dict[str, List[str]]:
    """Get all skills categorized."""
    data = load_data()
    return data.get("skills", {})


def add_skill(category: str, skill: str) -> None:
    """Add a skill to a category."""
    data = load_data()
    if "skills" not in data:
        data["skills"] = {}
    if category not in data["skills"]:
        data["skills"][category] = []
    if skill not in data["skills"][category]:
        data["skills"][category].append(skill)
    save_data(data)


def update_skills(skills: Dict[str, List[str]]) -> None:
    """Update entire skills dictionary."""
    data = load_data()
    data["skills"] = skills
    save_data(data)


def get_relevant_skills(keywords: List[str]) -> Dict[str, List[str]]:
    """Get skills relevant to given keywords."""
    all_skills = get_skills()
    relevant_skills = {}

    for category, skills_list in all_skills.items():
        relevant = []
        for skill in skills_list:
            for keyword in keywords:
                if keyword.lower() in skill.lower() or skill.lower() in keyword.lower():
                    relevant.append(skill)
                    break
        if relevant:
            relevant_skills[category] = relevant

    return relevant_skills


# ============================================================================
# OTHER SECTIONS
# ============================================================================

def get_certifications() -> List[Dict[str, Any]]:
    """Get all certifications."""
    data = load_data()
    return data.get("certifications", [])


def add_certification(cert: Dict[str, Any]) -> None:
    """Add a certification."""
    data = load_data()
    cert["id"] = datetime.now().timestamp()
    data["certifications"].append(cert)
    save_data(data)


def get_awards() -> List[Dict[str, Any]]:
    """Get all awards."""
    data = load_data()
    return data.get("awards", [])


def add_award(award: Dict[str, Any]) -> None:
    """Add an award."""
    data = load_data()
    award["id"] = datetime.now().timestamp()
    data["awards"].append(award)
    save_data(data)


def get_publications() -> List[Dict[str, Any]]:
    """Get all publications."""
    data = load_data()
    return data.get("publications", [])


def add_publication(pub: Dict[str, Any]) -> None:
    """Add a publication."""
    data = load_data()
    pub["id"] = datetime.now().timestamp()
    data["publications"].append(pub)
    save_data(data)


def get_volunteer() -> List[Dict[str, Any]]:
    """Get all volunteer experiences."""
    data = load_data()
    return data.get("volunteer", [])


def add_volunteer(vol: Dict[str, Any]) -> None:
    """Add a volunteer experience."""
    data = load_data()
    vol["id"] = datetime.now().timestamp()
    data["volunteer"].append(vol)
    save_data(data)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def export_all() -> Dict[str, Any]:
    """Export all resume data."""
    return load_data()


def get_summary() -> Dict[str, Any]:
    """Get a summary of stored data."""
    data = load_data()
    return {
        "initialized": data.get("initialized", False),
        "experiences_count": len(data.get("experiences", [])),
        "projects_count": len(data.get("projects", [])),
        "education_count": len(data.get("education", [])),
        "skill_categories": len(data.get("skills", {})),
        "total_skills": sum(len(v) for v in data.get("skills", {}).values()),
        "certifications_count": len(data.get("certifications", [])),
        "last_updated": data.get("last_updated", "Never")
    }


def reset_all() -> None:
    """Reset all data (use with caution)."""
    if DB_FILE.exists():
        DB_FILE.unlink()
    ensure_db_file()


def search_all(query: str) -> Dict[str, List[Dict[str, Any]]]:
    """Search across all resume data."""
    query_lower = query.lower()
    results = {
        "experiences": [],
        "projects": [],
        "education": []
    }

    # Search experiences
    for exp in get_experiences():
        searchable = json.dumps(exp).lower()
        if query_lower in searchable:
            results["experiences"].append(exp)

    # Search projects
    for proj in get_projects():
        searchable = json.dumps(proj).lower()
        if query_lower in searchable:
            results["projects"].append(proj)

    # Search education
    for edu in get_education():
        searchable = json.dumps(edu).lower()
        if query_lower in searchable:
            results["education"].append(edu)

    return results


# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Resume Database Manager")
        print("\nUsage:")
        print("  python3 resume_db.py is_initialized")
        print("  python3 resume_db.py summary")
        print("  python3 resume_db.py export")
        print("  python3 resume_db.py get_personal_info")
        print("  python3 resume_db.py get_experiences")
        print("  python3 resume_db.py get_projects")
        print("  python3 resume_db.py get_education")
        print("  python3 resume_db.py get_skills")
        print("  python3 resume_db.py search <query>")
        print("  python3 resume_db.py reset")
        sys.exit(1)

    command = sys.argv[1]

    if command == "is_initialized":
        print("true" if is_initialized() else "false")
    elif command == "summary":
        print(json.dumps(get_summary(), indent=2))
    elif command == "export":
        print(json.dumps(export_all(), indent=2))
    elif command == "get_personal_info":
        print(json.dumps(get_personal_info(), indent=2))
    elif command == "get_experiences":
        print(json.dumps(get_experiences(), indent=2))
    elif command == "get_projects":
        print(json.dumps(get_projects(), indent=2))
    elif command == "get_education":
        print(json.dumps(get_education(), indent=2))
    elif command == "get_skills":
        print(json.dumps(get_skills(), indent=2))
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Query required")
            sys.exit(1)
        query = sys.argv[2]
        print(json.dumps(search_all(query), indent=2))
    elif command == "reset":
        confirm = input("Are you sure you want to reset all resume data? (yes/no): ")
        if confirm.lower() == "yes":
            reset_all()
            print("All resume data has been reset.")
        else:
            print("Reset cancelled.")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
