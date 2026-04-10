#!/usr/bin/env python3
"""Notion Planner — /inspect command: workspace intelligence."""
import json, sys
sys.path.insert(0, "/home/wls/.openclaw/workspace-lisa/scripts")
from notion_api import *

def inspect():
    print("=== Notion Workspace Inspection ===\n")
    
    # 1. Query all databases
    workspace_map = {}
    for name, db_id in DB_IDS.items():
        print(f"📂 {name.upper()} ({db_id[:8]}...)")
        db = get_db(db_id)
        # Schema
        props = db.get("properties", {})
        print(f"   Schema: {len(props)} properties")
        for pname, pdef in props.items():
            ptype = pdef.get("type", "unknown")
            extra = ""
            if ptype == "relation":
                rel_db = pdef.get("relation", {}).get("database_id", "?")
                extra = f" → {rel_db[:8]}..."
            elif ptype == "select":
                opts = [o["name"] for o in pdef.get("select", {}).get("options", [])]
                extra = f" [{', '.join(opts)}]"
            elif ptype == "multi_select":
                opts = [o["name"] for o in pdef.get("multi_select", {}).get("options", [])]
                extra = f" [{', '.join(opts)}]"
            print(f"   - {pname} ({ptype}){extra}")
        
        # Data
        data = query_db(db_id)
        pages = data.get("results", [])
        print(f"   Records: {len(pages)}")
        for p in pages[:5]:  # Show first 5
            title = extract_title(p, "Name") or extract_title(p, "Title") or "(untitled)"
            print(f"     • {title}")
        if len(pages) > 5:
            print(f"     ... and {len(pages)-5} more")
        
        # Store in map
        workspace_map[name] = {
            "id": db_id,
            "properties": {pn: pd.get("type") for pn, pd in props.items()},
            "page_count": len(pages),
            "sample_titles": [extract_title(p, "Name") or extract_title(p, "Title") or "" for p in pages[:10]],
        }
        print()

    # 2. Map team members
    print("👥 TEAM MEMBERS:")
    team_data = query_db(DB_IDS["team_members"])
    members = []
    for p in team_data.get("results", []):
        name = extract_title(p, "Name")
        role = extract_rich_text(p, "Role")
        avail = extract_select(p, "Availability")
        tz = extract_select(p, "Timezone")
        skills = extract_multi_select(p, "Skills")
        email = extract_email(p, "Email")
        members.append({"name": name, "role": role, "availability": avail, "timezone": tz, "skills": skills, "email": email, "id": p["id"]})
        print(f"  {name}: {role} | {avail} | {tz} | Skills: {', '.join(skills) if skills else 'none'}")
    
    # 3. Map relationships
    print("\n🔗 RELATIONSHIPS:")
    for name, info in workspace_map.items():
        rels = [f"{pn}→{pd}" for pn, pd in info["properties"].items() if pd == "relation"]
        if rels:
            print(f"  {name}: {', '.join(rels)}")
    
    # 4. Store workspace map
    map_path = "/home/wls/.openclaw/workspace-lisa/memory/notion-workspace-map.json"
    with open(map_path, "w") as f:
        json.dump({"workspace_map": workspace_map, "team_members": members, "inspected_at": __import__("datetime").datetime.now().isoformat()}, f, indent=2)
    print(f"\n💾 Workspace map saved to {map_path}")
    print("\n✅ Inspection complete.")

if __name__ == "__main__":
    inspect()