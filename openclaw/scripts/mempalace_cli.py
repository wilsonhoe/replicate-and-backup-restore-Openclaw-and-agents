#!/usr/bin/env python3
"""
MemPalace CLI Wrapper for OpenClaw Agents
==========================================
Provides command-line access to MemPalace memory system since OpenClaw
doesn't support MCP servers natively.

Usage: python3 /home/wls/.openclaw/scripts/mempalace_cli.py <command> [args]

Commands:
  status                          - Show palace status
  search <query> [--limit N]      - Search memories
  kg-query <entity>               - Query knowledge graph
  kg-add <subject> <predicate> <object>  - Add fact to KG
  kg-timeline <entity>           - Get timeline for entity
  add-drawer <wing> <room> <content>      - Add a memory drawer
  diary-write <agent> <entry>    - Write diary entry
  diary-read <agent> [--last-n N] - Read diary entries
"""

import argparse
import json
import os
import sys

# Set up MemPalace path
os.environ["MEM_PALACE"] = "/home/wls/.openclaw"

# Import MemPalace tools
try:
    from mempalace.mcp_server import TOOLS
except ImportError as e:
    print(f"Error: MemPalace not installed. Run: pip3 install mempalace --break-system-packages", file=sys.stderr)
    sys.exit(1)


def cmd_status(args):
    result = TOOLS["mempalace_status"]["handler"]()
    print(json.dumps(result, indent=2))


def cmd_search(args):
    kwargs = {"query": args.query}
    if args.wing:
        kwargs["wing"] = args.wing
    if args.room:
        kwargs["room"] = args.room
    if args.limit:
        kwargs["limit"] = args.limit
    result = TOOLS["mempalace_search"]["handler"](**kwargs)
    print(json.dumps(result, indent=2))


def cmd_kg_query(args):
    kwargs = {"entity": args.entity}
    if args.as_of:
        kwargs["as_of"] = args.as_of
    if args.direction:
        kwargs["direction"] = args.direction
    result = TOOLS["mempalace_kg_query"]["handler"](**kwargs)
    print(json.dumps(result, indent=2))


def cmd_kg_add(args):
    kwargs = {
        "subject": args.subject,
        "predicate": args.predicate,
        "object": args.object
    }
    if args.valid_from:
        kwargs["valid_from"] = args.valid_from
    result = TOOLS["mempalace_kg_add"]["handler"](**kwargs)
    print(json.dumps(result, indent=2))


def cmd_kg_invalidate(args):
    kwargs = {
        "subject": args.subject,
        "predicate": args.predicate,
        "object": args.object
    }
    if args.ended:
        kwargs["ended"] = args.ended
    result = TOOLS["mempalace_kg_invalidate"]["handler"](**kwargs)
    print(json.dumps(result, indent=2))


def cmd_kg_timeline(args):
    result = TOOLS["mempalace_kg_timeline"]["handler"](entity=args.entity)
    print(json.dumps(result, indent=2))


def cmd_kg_stats(args):
    result = TOOLS["mempalace_kg_stats"]["handler"]()
    print(json.dumps(result, indent=2))


def cmd_add_drawer(args):
    kwargs = {
        "wing": args.wing,
        "room": args.room,
        "content": args.content
    }
    if args.source_file:
        kwargs["source_file"] = args.source_file
    result = TOOLS["mempalace_add_drawer"]["handler"](**kwargs)
    print(json.dumps(result, indent=2))


def cmd_delete_drawer(args):
    result = TOOLS["mempalace_delete_drawer"]["handler"](drawer_id=args.drawer_id)
    print(json.dumps(result, indent=2))


def cmd_list_wings(args):
    result = TOOLS["mempalace_list_wings"]["handler"]()
    print(json.dumps(result, indent=2))


def cmd_list_rooms(args):
    kwargs = {}
    if args.wing:
        kwargs["wing"] = args.wing
    result = TOOLS["mempalace_list_rooms"]["handler"](**kwargs)
    print(json.dumps(result, indent=2))


def cmd_traverse(args):
    kwargs = {"start_room": args.start_room}
    if args.max_hops:
        kwargs["max_hops"] = args.max_hops
    result = TOOLS["mempalace_traverse"]["handler"](**kwargs)
    print(json.dumps(result, indent=2))


def cmd_find_tunnels(args):
    kwargs = {}
    if args.wing_a:
        kwargs["wing_a"] = args.wing_a
    if args.wing_b:
        kwargs["wing_b"] = args.wing_b
    result = TOOLS["mempalace_find_tunnels"]["handler"](**kwargs)
    print(json.dumps(result, indent=2))


def cmd_graph_stats(args):
    result = TOOLS["mempalace_graph_stats"]["handler"]()
    print(json.dumps(result, indent=2))


def cmd_diary_write(args):
    result = TOOLS["mempalace_diary_write"]["handler"](
        agent_name=args.agent,
        entry=args.entry,
        topic=args.topic or "general"
    )
    print(json.dumps(result, indent=2))


def cmd_diary_read(args):
    result = TOOLS["mempalace_diary_read"]["handler"](
        agent_name=args.agent,
        last_n=args.last_n
    )
    print(json.dumps(result, indent=2))


def cmd_check_duplicate(args):
    result = TOOLS["mempalace_check_duplicate"]["handler"](content=args.content)
    print(json.dumps(result, indent=2))


def cmd_get_taxonomy(args):
    result = TOOLS["mempalace_get_taxonomy"]["handler"]()
    print(json.dumps(result, indent=2))


def cmd_get_aaak_spec(args):
    result = TOOLS["mempalace_get_aaak_spec"]["handler"]()
    print(result)


def main():
    parser = argparse.ArgumentParser(
        description="MemPalace CLI for OpenClaw Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # status
    subparsers.add_parser("status", help="Show palace status")

    # search
    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--wing", help="Filter by wing")
    search_parser.add_argument("--room", help="Filter by room")
    search_parser.add_argument("--limit", type=int, default=5, help="Max results")

    # kg-query
    kg_query_parser = subparsers.add_parser("kg-query", help="Query knowledge graph")
    kg_query_parser.add_argument("entity", help="Entity to query")
    kg_query_parser.add_argument("--as-of", help="Date filter (YYYY-MM-DD)")
    kg_query_parser.add_argument("--direction", choices=["incoming", "outgoing", "both"],
                                  default="both", help="Relationship direction")

    # kg-add
    kg_add_parser = subparsers.add_parser("kg-add", help="Add fact to knowledge graph")
    kg_add_parser.add_argument("subject", help="Subject entity")
    kg_add_parser.add_argument("predicate", help="Relationship type")
    kg_add_parser.add_argument("object", help="Object entity")
    kg_add_parser.add_argument("--valid-from", help="When fact became true (YYYY-MM-DD)")

    # kg-invalidate
    kg_inv_parser = subparsers.add_parser("kg-invalidate", help="Invalidate a fact")
    kg_inv_parser.add_argument("subject", help="Subject entity")
    kg_inv_parser.add_argument("predicate", help="Relationship type")
    kg_inv_parser.add_argument("object", help="Object entity")
    kg_inv_parser.add_argument("--ended", help="When fact stopped being true (YYYY-MM-DD)")

    # kg-timeline
    kg_tl_parser = subparsers.add_parser("kg-timeline", help="Get timeline for entity")
    kg_tl_parser.add_argument("entity", help="Entity name")

    # kg-stats
    subparsers.add_parser("kg-stats", help="Get knowledge graph statistics")

    # add-drawer
    add_drawer_parser = subparsers.add_parser("add-drawer", help="Add a memory drawer")
    add_drawer_parser.add_argument("wing", help="Wing name")
    add_drawer_parser.add_argument("room", help="Room name")
    add_drawer_parser.add_argument("content", help="Drawer content")
    add_drawer_parser.add_argument("--source-file", help="Source file path")

    # delete-drawer
    del_drawer_parser = subparsers.add_parser("delete-drawer", help="Delete a drawer")
    del_drawer_parser.add_argument("drawer_id", help="Drawer ID to delete")

    # list-wings
    subparsers.add_parser("list-wings", help="List all wings")

    # list-rooms
    list_rooms_parser = subparsers.add_parser("list-rooms", help="List rooms")
    list_rooms_parser.add_argument("--wing", help="Filter by wing")

    # traverse
    traverse_parser = subparsers.add_parser("traverse", help="Traverse palace graph")
    traverse_parser.add_argument("start_room", help="Starting room")
    traverse_parser.add_argument("--max-hops", type=int, default=2, help="Max hops")

    # find-tunnels
    tunnels_parser = subparsers.add_parser("find-tunnels", help="Find connections between wings")
    tunnels_parser.add_argument("--wing-a", help="First wing")
    tunnels_parser.add_argument("--wing-b", help="Second wing")

    # graph-stats
    subparsers.add_parser("graph-stats", help="Get graph statistics")

    # diary-write
    diary_write_parser = subparsers.add_parser("diary-write", help="Write diary entry")
    diary_write_parser.add_argument("agent", help="Agent name")
    diary_write_parser.add_argument("entry", help="Entry content (AAAK format)")
    diary_write_parser.add_argument("--topic", help="Topic tag")

    # diary-read
    diary_read_parser = subparsers.add_parser("diary-read", help="Read diary entries")
    diary_read_parser.add_argument("agent", help="Agent name")
    diary_read_parser.add_argument("--last-n", type=int, default=10, help="Number of entries")

    # check-duplicate
    dup_parser = subparsers.add_parser("check-duplicate", help="Check if content exists")
    dup_parser.add_argument("content", help="Content to check")

    # get-taxonomy
    subparsers.add_parser("get-taxonomy", help="Get palace taxonomy")

    # get-aaak-spec
    subparsers.add_parser("get-aaak-spec", help="Get AAAK dialect specification")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Map commands to functions
    commands = {
        "status": cmd_status,
        "search": cmd_search,
        "kg-query": cmd_kg_query,
        "kg-add": cmd_kg_add,
        "kg-invalidate": cmd_kg_invalidate,
        "kg-timeline": cmd_kg_timeline,
        "kg-stats": cmd_kg_stats,
        "add-drawer": cmd_add_drawer,
        "delete-drawer": cmd_delete_drawer,
        "list-wings": cmd_list_wings,
        "list-rooms": cmd_list_rooms,
        "traverse": cmd_traverse,
        "find-tunnels": cmd_find_tunnels,
        "graph-stats": cmd_graph_stats,
        "diary-write": cmd_diary_write,
        "diary-read": cmd_diary_read,
        "check-duplicate": cmd_check_duplicate,
        "get-taxonomy": cmd_get_taxonomy,
        "get-aaak-spec": cmd_get_aaak_spec,
    }

    try:
        commands[args.command](args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
