#!/usr/bin/env python3
"""Notion Planner — /create-project [name] command: create project with auto-timeline and tasks."""
import sys, json
from datetime import datetime, timedelta
sys.path.insert(0, "/home/wls/.openclaw/workspace-lisa/scripts")
from notion_api import *

# Default task templates by project type
PROJECT_TEMPLATES = {
    "default": [
        ("Project Kickoff", "High", 0),
        ("Research & Planning", "High", 2),
        ("Design/Architecture", "Medium", 7),
        ("Implementation", "High", 14),
        ("Testing & QA", "Medium", 21),
        ("Review & Launch", "High", 28),
    ],
    "marketing": [
        ("Market Research", "High", 0),
        ("Content Strategy", "Medium", 3),
        ("Content Creation", "High", 7),
        ("Distribution Plan", "Medium", 14),
        ("Launch Campaign", "High", 21),
        ("Analytics Review", "Medium", 28),
    ],
    "software": [
        ("Requirements Gathering", "High", 0),
        ("System Design", "High", 5),
        ("Development Sprint 1", "High", 10),
        ("Development Sprint 2", "High", 17),
        ("Testing & QA", "High", 24),
        ("Deployment", "Medium", 28),
    ],
}

def create_project(name, project_type="default", priority="High", owner="Wilson", duration_days=30):
    start = datetime.now()
    due = start + timedelta(days=duration_days)
    start_str = start.strftime("%Y-%m-%d")
    due_str = due.strftime("%Y-%m-%d")

    print(f"🚀 Creating Project: {name}")
    print(f"   Type: {project_type} | Priority: {priority} | Duration: {duration_days} days")
    print(f"   Start: {start_str} → Due: {due_str}\n")

    # 1. Create project page
    project_props = {
        "Name": make_title_prop(name),
        "Status": make_select_prop("Planning"),
        "Start Date": make_date_prop(start_str),
        "Due Date": make_date_prop(due_str),
        "Priority": make_select_prop(priority),
        "Owner": make_rich_text_prop(owner),
        "Description": make_rich_text_prop(f"Auto-created {project_type} project"),
    }
    
    project = create_page(DB_IDS["projects"], project_props)
    project_id = project["id"]
    print(f"✅ Project created: {name} (ID: {project_id[:8]}...)\n")

    # 2. Create task templates
    template = PROJECT_TEMPLATES.get(project_type, PROJECT_TEMPLATES["default"])
    task_ids = []
    print(f"📋 Creating {len(template)} tasks:")
    
    for task_name, task_priority, offset_days in template:
        task_due = start + timedelta(days=offset_days)
        task_props = {
            "Name": make_title_prop(f"{name} — {task_name}"),
            "Status": make_select_prop("To Do"),
            "Due Date": make_date_prop(task_due.strftime("%Y-%m-%d")),
            "Priority": make_select_prop(task_priority),
            "Project": make_relation_prop([project_id]),
            "Description": make_rich_text_prop(f"Auto-generated task for {name}"),
        }
        
        task = create_page(DB_IDS["tasks"], task_props)
        task_id = task["id"]
        task_ids.append(task_id)
        print(f"  ✓ {task_name} (due: {task_due.strftime('%Y-%m-%d')}, priority: {task_priority})")

    # 3. Link tasks back to project
    print(f"\n🔗 Linking {len(task_ids)} tasks to project...")
    # Update project with related tasks
    http.patch(
        f"https://api.notion.com/v1/pages/{project_id}",
        headers=HEADERS_OLD,
        json={"properties": {"Related Tasks": make_relation_prop(task_ids)}}
    ).raise_for_status()
    
    # Update project status to Active
    http.patch(
        f"https://api.notion.com/v1/pages/{project_id}",
        headers=HEADERS_OLD,
        json={"properties": {"Status": make_select_prop("Active")}}
    ).raise_for_status()
    print(f"✅ Project status set to Active")

    # 4. Summary
    print(f"\n{'='*50}")
    print(f"📊 PROJECT CREATED SUCCESSFULLY")
    print(f"   Name: {name}")
    print(f"   Type: {project_type}")
    print(f"   Timeline: {start_str} → {due_str}")
    print(f"   Tasks: {len(task_ids)} auto-generated")
    print(f"   Priority: {priority}")
    print(f"   Owner: {owner}")
    print(f"{'='*50}")
    
    return {"project_id": project_id, "task_ids": task_ids, "name": name, "start": start_str, "due": due_str}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: notion_create_project.py <name> [type] [priority] [duration_days]")
        print("Types: default, marketing, software")
        sys.exit(1)
    
    name = sys.argv[1]
    ptype = sys.argv[2] if len(sys.argv) > 2 else "default"
    priority = sys.argv[3] if len(sys.argv) > 3 else "High"
    duration = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    
    result = create_project(name, ptype, priority, duration_days=duration)
    # Save result
    path = "/home/wls/.openclaw/workspace-lisa/memory/notion-last-project.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Project data saved to {path}")