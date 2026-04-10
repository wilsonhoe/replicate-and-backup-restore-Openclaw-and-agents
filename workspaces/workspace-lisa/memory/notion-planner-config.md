# Notion Planner AI Agent - Configuration

**Created:** 2026-04-10
**Status:** Phase 2 Complete

## Notion Workspace

**Workspace URL:** https://www.notion.so/Notion-Planner-AI-Workspace-33e99ce82630814383f2cc122210a29e

## Database IDs (v2 - working)

| Database | ID | Data Source ID |
|----------|----|----|
| Team Members | 33e99ce8-2630-819e-8d95-c9371938928f | 54323a59-3407-418e-b39f-c34e24907028 (v1) |
| Projects | 33e99ce8-2630-8164-ad01-c67b77a86e2a | - |
| Tasks | 33e99ce8-2630-8179-9ac6-cb9eee12c346 | - |
| Meetings | 33e99ce8-2630-81eb-b990-c2c6e6a094ca | - |

## Database Schemas

### Team Members
- Name (title)
- Role (rich text)
- Availability (select: Available, Busy, On Leave, Part-time)
- Timezone (select: UTC+8 SGT, UTC-5 EST, UTC+0 GMT, UTC+9 JST, UTC-8 PST)
- Email (email)
- Skills (multi_select: Design, Frontend, Backend, DevOps, Marketing, Management)
- Assigned Tasks (relation → Tasks)
- Meeting Attendance (relation → Meetings)

### Projects
- Name (title)
- Status (select: Planning, Active, On Hold, Completed, Cancelled)
- Start Date (date)
- Due Date (date)
- Owner (rich text)
- Priority (select: Low, Medium, High, Critical)
- Description (rich text)
- Related Tasks (relation → Tasks)
- Meetings (relation → Meetings)

### Tasks
- Name (title)
- Status (select: To Do, In Progress, Review, Done, Blocked)
- Due Date (date)
- Priority (select: Low, Medium, High, Urgent)
- Description (rich text)
- Project (relation → Projects)
- Assignee (relation → Team Members)

### Meetings
- Title (title)
- Type (select: Kickoff, Standup, Review, Handoff, 1-on-1)
- Time (date with time)
- Status (select: Scheduled, Confirmed, Completed, Cancelled)
- Notes (rich text)
- Project (relation → Projects)
- Attendees (relation → Team Members)

## Sample Data

**Team Members:**
- Wilson (Owner/CEO, Available, UTC+8 SGT)
- Lisa AI (AI Secretary, Available, UTC+8 SGT)

**Project:**
- Notion Planner AI Agent (Active, Apr 10 - May 8, High priority)

**Tasks:**
- Design Notion database schema (Done)
- Configure API integration (In Progress)
- Build workspace inspection agent (To Do)

**Meeting:**
- Notion Planner Kickoff (Apr 10, 9:00-10:00 SGT)

## API Configuration

**Token:** Configured at `~/.config/notion/api_key` (ntn_...)
**API Version:** Use `2022-06-28` for database creation with properties; `2025-09-03` has data source model that doesn't support property creation properly
**Rate Limit:** ~3 requests/second

## Key Learnings

5. **Phase 2 Scripts:** `notion_api.py` (shared lib), `notion_inspect.py` (`/inspect`), `notion_create_project.py` (`/create-project`), `notion_assign_tasks.py` (`/assign-tasks`)

1. **API Version Compatibility:** The 2025-09-03 API version uses "data sources" instead of "databases" for property management. Creating databases with properties requires the `2022-06-28` version. Once created, both versions can read/write data.
2. **Database Creation:** Use `POST /v1/databases` with `2022-06-28` to create databases with full property definitions including relations.
3. **Relation Properties:** Must be added after both referenced databases exist. Use PATCH on the database to add relation properties.
4. **Page Creation:** Use `database_id` as parent (not `data_source_id`) when creating pages, even with newer API version.