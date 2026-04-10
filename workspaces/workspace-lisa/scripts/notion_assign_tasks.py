#!/usr/bin/env python3
"""Notion Planner — /assign-tasks: auto-assign tasks based on team availability & skills."""
import sys, json
from datetime import datetime
sys.path.insert(0, "/home/wls/.openclaw/workspace-lisa/scripts")
from notion_api import *

# Timezone UTC offsets
TZ_OFFSETS = {
    "UTC+8 SGT": 8, "UTC-5 EST": -5, "UTC+0 GMT": 0,
    "UTC+9 JST": 9, "UTC-8 PST": -8,
}

# Skill keywords for task matching
SKILL_KEYWORDS = {
    "Design": ["design", "ui", "ux", "visual", "layout", "style", "creative"],
    "Frontend": ["frontend", "front-end", "ui", "web", "react", "vue", "css", "html"],
    "Backend": ["backend", "back-end", "api", "server", "database", "infra"],
    "DevOps": ["devops", "deploy", "ci", "cd", "infrastructure", "docker", "cloud"],
    "Marketing": ["marketing", "content", "social", "campaign", "seo", "outreach"],
    "Management": ["manage", "plan", "coordinate", "review", "lead", "organize"],
}

def get_team():
    """Get all team members with availability."""
    data = query_db(DB_IDS["team_members"])
    members = []
    for p in data.get("results", []):
        members.append({
            "id": p["id"],
            "name": extract_title(p, "Name"),
            "role": extract_rich_text(p, "Role"),
            "availability": extract_select(p, "Availability"),
            "timezone": extract_select(p, "Timezone"),
            "skills": extract_multi_select(p, "Skills"),
            "email": extract_email(p, "Email"),
            "task_ids": extract_relation(p, "Assigned Tasks"),
        })
    return members

def get_unassigned_tasks():
    """Get all To Do / In Progress tasks without assignees."""
    data = query_db(DB_IDS["tasks"], {
        "and": [
            {"property": "Status", "select": {"does_not_equal": "Done"}},
            {"property": "Status", "select": {"does_not_equal": "Blocked"}},
        ]
    })
    tasks = []
    for p in data.get("results", []):
        assignees = extract_relation(p, "Assignee")
        if not assignees:
            tasks.append({
                "id": p["id"],
                "name": extract_title(p, "Name"),
                "status": extract_select(p, "Status"),
                "priority": extract_select(p, "Priority"),
                "due": extract_date(p, "Due Date"),
                "project_ids": extract_relation(p, "Project"),
                "description": extract_rich_text(p, "Description"),
            })
    return tasks

def match_task_to_member(task, members):
    """Score each member for a task based on skills, availability, workload."""
    scores = []
    task_text = (task["name"] + " " + task["description"]).lower()
    
    for m in members:
        score = 0
        reasons = []
        
        # Availability filter
        if m["availability"] == "On Leave":
            continue
        if m["availability"] == "Available":
            score += 10
            reasons.append("available")
        elif m["availability"] == "Part-time":
            score += 5
            reasons.append("part-time")
        elif m["availability"] == "Busy":
            score += 1
            reasons.append("busy")
        
        # Skill matching
        for skill in m.get("skills", []):
            keywords = SKILL_KEYWORDS.get(skill, [skill.lower()])
            for kw in keywords:
                if kw in task_text:
                    score += 5
                    reasons.append(f"skill:{skill}")
                    break
        
        # Workload (fewer tasks = higher score)
        load = len(m.get("task_ids", []))
        score += max(0, 5 - load)
        if load > 0:
            reasons.append(f"load:{load}")
        
        scores.append((m, score, reasons))
    
    scores.sort(key=lambda x: -x[1])
    return scores

def assign_tasks(dry_run=False):
    print("📋 Notion Task Assignment Engine\n")
    print("=" * 50)
    
    # 1. Get team
    members = get_team()
    print(f"👥 Team Members ({len(members)}):")
    for m in members:
        load = len(m.get("task_ids", []))
        print(f"  {m['name']}: {m['availability']} | {m['timezone']} | Skills: {', '.join(m['skills'])} | Tasks: {load}")
    print()
    
    # 2. Get unassigned tasks
    tasks = get_unassigned_tasks()
    print(f"📝 Unassigned Tasks ({len(tasks)}):")
    for t in tasks:
        due_str = t["due"]["start"][:10] if t["due"] else "no date"
        print(f"  [{t['status']}] {t['name']} (due: {due_str}, priority: {t['priority']})")
    print()
    
    if not tasks:
        print("✅ No unassigned tasks found. All tasks have assignees!")
        return
    
    # 3. Match and assign
    print("🎯 Assignment Recommendations:\n")
    assignments = []
    
    for task in tasks:
        scores = match_task_to_member(task, members)
        if not scores:
            print(f"  ⚠️ {task['name']}: No available members!")
            continue
        
        best_member, best_score, reasons = scores[0]
        print(f"  ✅ {task['name'][:50]}")
        print(f"     → {best_member['name']} (score: {best_score}, {', '.join(reasons[:3])})")
        
        if len(scores) > 1:
            alt = scores[1]
            print(f"     Alt: {alt[0]['name']} (score: {alt[1]})")
        
        assignments.append((task, best_member, best_score, reasons))
    
    if dry_run:
        print(f"\n🔄 DRY RUN — {len(assignments)} assignments recommended (none applied)")
        return
    
    # 4. Apply assignments
    print(f"\n🚀 Applying {len(assignments)} assignments...")
    applied = 0
    for task, member, score, reasons in assignments:
        try:
            # Update task with assignee
            import requests as http
            http.patch(
                f"https://api.notion.com/v1/pages/{task['id']}",
                headers=HEADERS_OLD,
                json={"properties": {"Assignee": make_relation_prop([member["id"]])}}
            ).raise_for_status()
            print(f"  ✓ Assigned '{task['name'][:40]}' → {member['name']}")
            applied += 1
        except Exception as e:
            print(f"  ✗ Failed to assign '{task['name']}': {e}")
    
    print(f"\n✅ {applied}/{len(assignments)} tasks assigned successfully!")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    assign_tasks(dry_run=dry_run)