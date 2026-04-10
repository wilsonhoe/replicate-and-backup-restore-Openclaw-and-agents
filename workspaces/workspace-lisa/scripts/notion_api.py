"""Notion API helper — shared by all planner commands."""
import os, json, requests as http

TOKEN = open(os.path.expanduser("~/.config/notion/api_key")).read().strip()
HEADERS_NEW = {"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}
HEADERS_OLD = {**HEADERS_NEW, "Notion-Version": "2022-06-28"}

DB_IDS = {
    "team_members": "33e99ce8-2630-819e-8d95-c9371938928f",
    "projects":     "33e99ce8-2630-8164-ad01-c67b77a86e2a",
    "tasks":        "33e99ce8-2630-8179-9ac6-cb9eee12c346",
    "meetings":     "33e99ce8-2630-81eb-b990-c2c6e6a094ca",
}

def api(method, path, body=None, headers=None):
    r = getattr(http, method)(f"https://api.notion.com/v1{path}", headers=headers or HEADERS_OLD, json=body)
    if r.status_code >= 400:
        print(f"API Error {r.status_code}: {r.text[:300]}")
    r.raise_for_status()
    return r.json()

def query_db(db_id, filter_obj=None):
    body = {}
    if filter_obj:
        body["filter"] = filter_obj
    return api("post", f"/databases/{db_id}/query", body or None)

def create_page(parent_db, properties):
    return api("post", "/pages", {"parent": {"database_id": parent_db}, "properties": properties})

def get_db(db_id):
    return api("get", f"/databases/{db_id}")

def extract_title(page, prop="Name"):
    """Extract title text from a page."""
    props = page.get("properties", {})
    title_prop = props.get(prop, props.get("title", {}))
    arr = title_prop.get("title", []) if isinstance(title_prop, dict) else []
    return arr[0].get("plain_text", "") if arr else ""

def extract_rich_text(page, prop):
    arr = page.get("properties", {}).get(prop, {}).get("rich_text", [])
    return arr[0].get("plain_text", "") if arr else ""

def extract_select(page, prop):
    obj = page.get("properties", {}).get(prop, {}).get("select")
    return obj.get("name", "") if obj else ""

def extract_date(page, prop):
    d = page.get("properties", {}).get(prop, {}).get("date")
    return d  # {start, end} or None

def extract_relation(page, prop):
    return [r["id"] for r in page.get("properties", {}).get(prop, {}).get("relation", [])]

def extract_multi_select(page, prop):
    return [s["name"] for s in page.get("properties", {}).get(prop, {}).get("multi_select", [])]

def extract_email(page, prop):
    return page.get("properties", {}).get(prop, {}).get("email", "")

def make_title_prop(text):
    return {"title": [{"text": {"content": text}}]}

def make_rich_text_prop(text):
    return {"rich_text": [{"text": {"content": text}}]}

def make_select_prop(name):
    return {"select": {"name": name}}

def make_date_prop(start, end=None):
    d = {"start": start}
    if end:
        d["end"] = end
    return {"date": d}

def make_relation_prop(page_ids):
    return {"relation": [{"id": pid} for pid in page_ids]}

def make_email_prop(email):
    return {"email": email}

def make_multi_select_prop(names):
    return {"multi_select": [{"name": n} for n in names]}