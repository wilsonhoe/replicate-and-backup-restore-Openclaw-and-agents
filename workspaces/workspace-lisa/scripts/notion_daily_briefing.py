#!/usr/bin/env python3
"""Daily Briefing Generator — queries Notion Tasks & Meetings, sends summary via Telegram."""

import argparse, json, os, sys
from datetime import datetime, timezone, timedelta

# Add scripts dir to path for notion_api
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from notion_api import query_db, extract_title, extract_select, extract_date, extract_rich_text

SGT = timezone(timedelta(hours=8))

# Hardcoded token from working system
TELEGRAM_BOT_TOKEN = "8606848979:AAHIwphVuvYIhYgJ-6XvlJcdYnS8Dk7464E"
TELEGRAM_CHAT_ID = "507276036"

TASKS_DB = "33e99ce8-2630-8179-9ac6-cb9eee12c346"
MEETINGS_DB = "33e99ce8-2630-81eb-b990-c2c6e6a094ca"


def today_sgt():
    return datetime.now(SGT).strftime("%Y-%m-%d")


def query_tasks_due_today():
    today = today_sgt()
    # Tasks due today
    filter_today = {
        "property": "Due Date",
        "date": {"equals": today}
    }
    result = query_db(TASKS_DB, filter_today)
    return result.get("results", [])


def query_overdue_tasks():
    today = today_sgt()
    filter_overdue = {
        "and": [
            {"property": "Due Date", "date": {"before": today}},
            {"property": "Status", "select": {"does_not_equal": "Done"}}
        ]
    }
    result = query_db(TASKS_DB, filter_overdue)
    return result.get("results", [])


def query_meetings_today():
    today = today_sgt()
    filter_today = {
        "property": "Time",
        "date": {"equals": today}
    }
    result = query_db(MEETINGS_DB, filter_today)
    return result.get("results", [])


def priority_emoji(p):
    return {"urgent": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get((p or "").lower(), "⚪")


def status_emoji(s):
    return {"to do": "📋", "in progress": "🔄", "review": "👀", "blocked": "🚫", "done": "✅"}.get((s or "").lower(), "❓")


def format_task(task):
    name = extract_title(task, "Name")
    status = extract_select(task, "Status")
    priority = extract_select(task, "Priority")
    due = extract_date(task, "Due Date")
    due_str = due.get("start", "")[:10] if due else "—"
    return f"  {status_emoji(status)} {name} | {priority_emoji(priority)}{priority} | Due: {due_str}"


def format_meeting(meeting):
    name = extract_title(meeting, "Title") or extract_title(meeting, "Name")
    mtype = extract_select(meeting, "Type")
    status = extract_select(meeting, "Status")
    time = extract_date(meeting, "Time")
    time_str = time.get("start", "") if time else "—"
    # Extract just time portion if it contains date
    if "T" in time_str:
        try:
            dt = datetime.fromisoformat(time_str)
            time_str = dt.strftime("%H:%M")
        except:
            pass
    return f"  📅 {name} ({mtype}) @ {time_str} [{status}]"


def generate_daily_briefing():
    today = today_sgt()
    day_name = datetime.now(SGT).strftime("%A")

    tasks = query_tasks_due_today()
    meetings = query_meetings_today()
    overdue = query_overdue_tasks()

    lines = [
        f"☀️ Good morning! Today's briefing — {day_name}, {today}",
        ""
    ]

    # Meetings
    if meetings:
        lines.append(f"📅 Meetings ({len(meetings)}):")
        for m in meetings:
            lines.append(format_meeting(m))
        lines.append("")
    else:
        lines.append("📅 No meetings today.")
        lines.append("")

    # Tasks due today
    if tasks:
        lines.append(f"📋 Tasks due today ({len(tasks)}):")
        for t in tasks:
            lines.append(format_task(t))
        lines.append("")
    else:
        lines.append("📋 No tasks due today.")
        lines.append("")

    # Overdue
    if overdue:
        lines.append(f"⚠️ OVERDUE ({len(overdue)}):")
        for t in overdue:
            lines.append(format_task(t))
        lines.append("")

    lines.append("— Lisa ✨")

    return "\n".join(lines)


def send_telegram(message):
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()


def log_briefing(message, sent=False):
    log_dir = os.path.expanduser("~/.openclaw/workspace-lisa/memory")
    os.makedirs(log_dir, exist_ok=True)
    today = today_sgt()
    log_path = os.path.join(log_dir, f"{today}.md")
    entry = f"\n## Daily Briefing ({'sent' if sent else 'dry-run'})\n{datetime.now(SGT).strftime('%H:%M')} — Briefing generated\n```\n{message[:500]}\n```\n"
    with open(log_path, "a") as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="Notion Daily Briefing")
    parser.add_argument("--send", action="store_true", help="Send via Telegram")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    try:
        briefing = generate_daily_briefing()
    except Exception as e:
        print(f"ERROR generating briefing: {e}")
        sys.exit(1)

    print(briefing)

    if args.send:
        try:
            send_telegram(briefing)
            log_briefing(briefing, sent=True)
            print("\n✅ Briefing sent via Telegram!")
        except Exception as e:
            print(f"\n❌ Failed to send: {e}")
            sys.exit(1)
    elif args.dry_run:
        log_briefing(briefing, sent=False)
        print("\n📋 Dry run — not sent.")
    else:
        print("\nUse --send to deliver or --dry-run to preview.")


if __name__ == "__main__":
    main()