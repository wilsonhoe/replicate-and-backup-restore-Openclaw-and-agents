#!/usr/bin/env python3
"""Notion Planner — /schedule-meeting: Smart meeting scheduling.

Detects when meetings are needed, checks availability, finds optimal times,
and creates meetings in Notion with buffer time.

Usage:
  python3 notion_schedule_meeting.py                    # Auto-detect needed meetings
  python3 notion_schedule_meeting.py --project "X"     # Schedule for specific project
  python3 notion_schedule_meeting.py --type kickoff --attendees "Wilson,Lisa AI" --date 2026-04-15
"""
import json, sys, argparse
from datetime import datetime, timedelta, timezone, time as dtime

sys.path.insert(0, "/home/wls/.openclaw/workspace-lisa/scripts")
from notion_api import *

SGT = timezone(timedelta(hours=8))
WORK_START = dtime(9, 0)
WORK_END = dtime(19, 0)
BUFFER_MINUTES = 15
MEETING_DURATION_DEFAULT = 60  # minutes

def get_team_members():
    """Fetch all team members with availability."""
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
        })
    return members

def get_meetings(date_str=None):
    """Get existing meetings, optionally filtered by date."""
    body = {}
    if date_str:
        body["filter"] = {
            "property": "Time",
            "date": {"equals": date_str}
        }
    data = query_db(DB_IDS["meetings"], body.get("filter"))
    meetings = []
    for p in data.get("results", []):
        dt = extract_date(p, "Time")
        meetings.append({
            "id": p["id"],
            "title": extract_title(p, "Title") or extract_title(p, "Name"),
            "type": extract_select(p, "Type"),
            "status": extract_select(p, "Status"),
            "time": dt,
            "attendees": extract_relation(p, "Attendees"),
            "project": extract_relation(p, "Project"),
        })
    return meetings

def get_projects():
    """Get all projects."""
    data = query_db(DB_IDS["projects"])
    projects = []
    for p in data.get("results", []):
        projects.append({
            "id": p["id"],
            "name": extract_title(p, "Name"),
            "status": extract_select(p, "Status"),
            "priority": extract_select(p, "Priority"),
            "due_date": extract_date(p, "Due Date"),
        })
    return projects

def detect_needed_meetings():
    """Auto-detect projects that need meetings scheduled."""
    projects = get_projects()
    meetings = get_meetings()
    meeting_project_ids = {m["project"][0] for m in meetings if m["project"]}
    
    needed = []
    for proj in projects:
        if proj["status"] in ("Planning", "Active") and proj["id"] not in meeting_project_ids:
            # No meeting yet for active/planning project
            if proj["status"] == "Planning":
                needed.append({"project": proj, "type": "Kickoff", "reason": "Project in Planning phase needs kickoff meeting"})
            elif proj["status"] == "Active":
                # Check if there's a review meeting scheduled
                needed.append({"project": proj, "type": "Review", "reason": "Active project without scheduled review"})
    
    return needed

def find_available_slots(date_str, attendee_ids, duration_min=60):
    """Find available time slots on a given date respecting work hours and buffer."""
    existing = get_meetings(date_str)
    
    # Build busy blocks
    busy = []
    for m in existing:
        if m["time"] and any(a in m["attendees"] for a in attendee_ids):
            start = datetime.fromisoformat(m["time"]["start"].replace("Z", "+00:00")).astimezone(SGT)
            end_dt = start + timedelta(minutes=duration_min)  # approximate
            if m["time"].get("end"):
                end_dt = datetime.fromisoformat(m["time"]["end"].replace("Z", "+00:00")).astimezone(SGT)
            busy.append((start.time(), (end_dt + timedelta(minutes=BUFFER_MINUTES)).time()))
    
    # Generate available slots
    day = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=SGT)
    slots = []
    current = datetime.combine(day.date(), WORK_START, tzinfo=SGT)
    end_of_day = datetime.combine(day.date(), WORK_END, tzinfo=SGT)
    
    while current + timedelta(minutes=duration_min) <= end_of_day:
        slot_start = current.time()
        slot_end = (current + timedelta(minutes=duration_min)).time()
        
        # Check conflicts
        conflict = False
        for busy_start, busy_end in busy:
            if slot_start < busy_end and slot_end > busy_start:
                conflict = True
                break
        
        if not conflict:
            slots.append({
                "start": current.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                "end": (current + timedelta(minutes=duration_min)).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                "display": f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')} SGT",
            })
        
        current += timedelta(minutes=30)  # 30-min increments
    
    return slots

def schedule_meeting(title, meeting_type, start_iso, end_iso, project_id=None, attendee_ids=None, notes=""):
    """Create a meeting in Notion."""
    props = {
        "Title": make_title_prop(title),
        "Type": make_select_prop(meeting_type),
        "Time": make_date_prop(start_iso, end_iso),
        "Status": make_select_prop("Scheduled"),
    }
    if notes:
        props["Notes"] = make_rich_text_prop(notes)
    if project_id:
        props["Project"] = make_relation_prop([project_id])
    if attendee_ids:
        props["Attendees"] = make_relation_prop(attendee_ids)
    
    return create_page(DB_IDS["meetings"], props)

def main():
    parser = argparse.ArgumentParser(description="Smart meeting scheduling")
    parser.add_argument("--project", help="Project name to schedule meeting for")
    parser.add_argument("--type", choices=["Kickoff", "Standup", "Review", "Handoff", "1-on-1"], help="Meeting type")
    parser.add_argument("--attendees", help="Comma-separated attendee names")
    parser.add_argument("--date", help="Date YYYY-MM-DD (default: tomorrow)")
    parser.add_argument("--duration", type=int, default=60, help="Duration in minutes")
    parser.add_argument("--auto", action="store_true", help="Auto-detect and schedule needed meetings")
    args = parser.parse_args()
    
    members = get_team_members()
    member_map = {m["name"]: m for m in members}
    
    if args.auto or (not args.project and not args.attendees):
        # Auto-detect mode
        needed = detect_needed_meetings()
        if not needed:
            print("✅ No meetings needed — all projects have meetings scheduled.")
            return
        
        print(f"📋 {len(needed)} meeting(s) needed:\n")
        for i, n in enumerate(needed, 1):
            print(f"  {i}. {n['project']['name']} → {n['type']}")
            print(f"     Reason: {n['reason']}")
        
        # Auto-schedule the first needed meeting
        target = needed[0]
        proj = target["project"]
        meeting_type = args.type or target["type"]
        title = f"{proj['name']} {meeting_type}"
        date_str = args.date or (datetime.now(SGT) + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Find available attendees
        available = [m for m in members if m["availability"] in ("Available", None, "")]
        attendee_ids = [m["id"] for m in available]
        attendee_names = [m["name"] for m in available]
        
        print(f"\n🗓️  Scheduling: {title}")
        print(f"   Date: {date_str}")
        print(f"   Attendees: {', '.join(attendee_names)}")
        
        slots = find_available_slots(date_str, attendee_ids, args.duration)
        if not slots:
            # Try next day
            date_str = (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
            slots = find_available_slots(date_str, attendee_ids, args.duration)
            print(f"   No slots today, trying {date_str}")
        
        if not slots:
            print("❌ No available slots found in next 2 days.")
            return
        
        slot = slots[0]
        print(f"   Slot: {slot['display']}")
        
        result = schedule_meeting(
            title=title,
            meeting_type=meeting_type,
            start_iso=slot["start"],
            end_iso=slot["end"],
            project_id=proj["id"],
            attendee_ids=attendee_ids,
            notes=f"Auto-scheduled {meeting_type} for {proj['name']}",
        )
        print(f"\n✅ Meeting created: {title}")
        print(f"   Time: {slot['display']}")
        print(f"   Type: {meeting_type}")
        print(f"   Attendees: {', '.join(attendee_names)}")
        print(f"   Buffer: {BUFFER_MINUTES} min before next meeting")
        return
    
    # Manual mode
    title = args.project or "Meeting"
    meeting_type = args.type or "1-on-1"
    date_str = args.date or (datetime.now(SGT) + timedelta(days=1)).strftime("%Y-%m-%d")
    
    attendee_ids = []
    attendee_names = []
    if args.attendees:
        for name in args.attendees.split(","):
            name = name.strip()
            if name in member_map:
                attendee_ids.append(member_map[name]["id"])
                attendee_names.append(name)
    else:
        available = [m for m in members if m["availability"] in ("Available", None, "")]
        attendee_ids = [m["id"] for m in available]
        attendee_names = [m["name"] for m in available]
    
    slots = find_available_slots(date_str, attendee_ids, args.duration)
    if not slots:
        print(f"❌ No available slots on {date_str}. Try another date.")
        return
    
    slot = slots[0]
    result = schedule_meeting(
        title=f"{title} {meeting_type}",
        meeting_type=meeting_type,
        start_iso=slot["start"],
        end_iso=slot["end"],
        attendee_ids=attendee_ids,
    )
    print(f"✅ Meeting created: {title} {meeting_type}")
    print(f"   Time: {slot['display']}")
    print(f"   Attendees: {', '.join(attendee_names)}")

def schedule_meeting_smart(project_id, meeting_type, duration_minutes=60):
    """Smart meeting scheduler — the core function for programmatic use.
    
    Args:
        project_id: Notion page ID of the project
        meeting_type: One of Kickoff, Standup, Review, Handoff, 1-on-1
        duration_minutes: Meeting duration in minutes
    
    Returns:
        dict with meeting details including url, or None on failure
    """
    # 1. Query project from Notion
    proj_data = api("get", f"/pages/{project_id}")
    proj_name = extract_title(proj_data, "Name")
    
    # 2. Detect attendees from project relations (Meetings → Team Members via Attendees)
    #    Also check team members assigned to project's tasks
    attendee_ids = set()
    
    # Get team members and find those available
    members = get_team_members()
    available_members = [m for m in members if m["availability"] in ("Available", None, "")]
    
    # If project has related tasks, get assignees
    project_task_ids = extract_relation(proj_data, "Related Tasks")
    for task_id in project_task_ids:
        try:
            task_data = api("get", f"/pages/{task_id}")
            task_assignees = extract_relation(task_data, "Assignee")
            attendee_ids.update(task_assignees)
        except:
            pass
    
    # Add all available members as fallback if no task assignees found
    if not attendee_ids:
        attendee_ids = {m["id"] for m in available_members}
    else:
        # Also ensure available members are included
        attendee_ids.update(m["id"] for m in available_members)
    
    attendee_ids = list(attendee_ids)
    attendee_names = []
    member_id_map = {m["id"]: m for m in members}
    for aid in attendee_ids:
        if aid in member_id_map:
            attendee_names.append(member_id_map[aid]["name"])
    
    # 3. Check each attendee's availability (from Team Members db)
    #    Already filtered to Available/Part-time members above
    
    # 4. Find first available slot (9am-7pm, with 15min buffer)
    #    Start from tomorrow
    start_date = (datetime.now(SGT) + timedelta(days=1)).strftime("%Y-%m-%d")
    slots = find_available_slots(start_date, attendee_ids, duration_minutes)
    
    # Try up to 7 days ahead
    for delta in range(1, 8):
        date_str = (datetime.now(SGT) + timedelta(days=delta)).strftime("%Y-%m-%d")
        slots = find_available_slots(date_str, attendee_ids, duration_minutes)
        if slots:
            break
    
    if not slots:
        return None
    
    slot = slots[0]
    title = f"{proj_name} {meeting_type}"
    
    # 5. Buffer is already accounted for in find_available_slots
    
    # 6. Create meeting in Notion
    result = schedule_meeting(
        title=title,
        meeting_type=meeting_type,
        start_iso=slot["start"],
        end_iso=slot["end"],
        project_id=project_id,
        attendee_ids=attendee_ids,
        notes=f"Auto-scheduled {meeting_type} for {proj_name} ({duration_minutes}min + {BUFFER_MINUTES}min buffer)",
    )
    
    # 7. Return meeting URL
    meeting_url = result.get("url", "")
    return {
        "title": title,
        "meeting_type": meeting_type,
        "start": slot["start"],
        "end": slot["end"],
        "display": slot["display"],
        "attendees": attendee_names,
        "project": proj_name,
        "url": meeting_url,
        "page_id": result.get("id", ""),
    }


if __name__ == "__main__":
    main()