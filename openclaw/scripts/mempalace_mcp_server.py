#!/usr/bin/env python3
"""
MemPalace MCP Server — FastMCP wrapper
=======================================
Bridges the existing MemPalace tools to the standard MCP SDK protocol.
This replaces the custom JSON-RPC implementation with proper MCP SDK integration.

Usage: claude mcp add mempalace -- python3 /home/wls/.openclaw/scripts/mempalace_mcp_server.py
"""

import json
import logging
import sys

from mcp.server.fastmcp import FastMCP

# Import all existing tool handlers from the installed mempalace package
from mempalace.mcp_server import TOOLS

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)
logger = logging.getLogger("mempalace_mcp_fastmcp")

# Create FastMCP server
mcp = FastMCP("mempalace")


# --- Read tools ---


@mcp.tool()
def mempalace_status() -> str:
    """Get total drawers, wing/room breakdown, and palace health."""
    return json.dumps(TOOLS["mempalace_status"]["handler"](), indent=2)


@mcp.tool()
def mempalace_list_wings() -> str:
    """List all wings with their drawer counts."""
    return json.dumps(TOOLS["mempalace_list_wings"]["handler"](), indent=2)


@mcp.tool()
def mempalace_list_rooms(wing: str) -> str:
    """List rooms within a specific wing.

    Args:
        wing: The wing name to list rooms for
    """
    return json.dumps(TOOLS["mempalace_list_rooms"]["handler"](wing=wing), indent=2)


@mcp.tool()
def mempalace_get_taxonomy() -> str:
    """Get the full wing -> room -> count taxonomy tree."""
    return json.dumps(TOOLS["mempalace_get_taxonomy"]["handler"](), indent=2)


@mcp.tool()
def mempalace_get_aaak_spec() -> str:
    """Get the AAAK compression dialect specification."""
    return json.dumps(TOOLS["mempalace_get_aaak_spec"]["handler"](), indent=2)


# --- Knowledge graph tools ---


@mcp.tool()
def mempalace_kg_query(entity: str, as_of: str = "", direction: str = "both") -> str:
    """Query the knowledge graph for facts about an entity.

    Args:
        entity: The entity name to query
        as_of: Optional temporal reference (e.g. '2026-01-01')
        direction: Direction of relationships — 'both', 'outgoing', or 'incoming'
    """
    kwargs = {"entity": entity, "direction": direction}
    if as_of:
        kwargs["as_of"] = as_of
    return json.dumps(TOOLS["mempalace_kg_query"]["handler"](**kwargs), indent=2)


@mcp.tool()
def mempalace_kg_add(
    subject: str, predicate: str, object: str, valid_from: str = "", source_closet: str = ""
) -> str:
    """Add a triple to the knowledge graph.

    Args:
        subject: The subject entity
        predicate: The relationship type
        object: The object entity
        valid_from: Optional start date for temporal facts
        source_closet: Optional source attribution
    """
    kwargs = {"subject": subject, "predicate": predicate, "object": object}
    if valid_from:
        kwargs["valid_from"] = valid_from
    if source_closet:
        kwargs["source_closet"] = source_closet
    return json.dumps(TOOLS["mempalace_kg_add"]["handler"](**kwargs), indent=2)


@mcp.tool()
def mempalace_kg_invalidate(
    subject: str, predicate: str, object: str, ended: str = ""
) -> str:
    """Invalidate (mark as outdated) a triple in the knowledge graph.

    Args:
        subject: The subject entity
        predicate: The relationship type
        object: The object entity
        ended: Optional end date for temporal invalidation
    """
    kwargs = {"subject": subject, "predicate": predicate, "object": object}
    if ended:
        kwargs["ended"] = ended
    return json.dumps(TOOLS["mempalace_kg_invalidate"]["handler"](**kwargs), indent=2)


@mcp.tool()
def mempalace_kg_timeline(entity: str) -> str:
    """Get the timeline of statements for an entity in the knowledge graph.

    Args:
        entity: The entity name to get timeline for
    """
    return json.dumps(
        TOOLS["mempalace_kg_timeline"]["handler"](entity=entity), indent=2
    )


@mcp.tool()
def mempalace_kg_stats() -> str:
    """Get knowledge graph statistics."""
    return json.dumps(TOOLS["mempalace_kg_stats"]["handler"](), indent=2)


# --- Graph traversal tools ---


@mcp.tool()
def mempalace_traverse(start_room: str, max_hops: int = 2) -> str:
    """Traverse the palace graph from a starting node.

    Args:
        start_room: Starting node name (wing, room, or drawer)
        max_hops: Maximum traversal depth (default: 2)
    """
    return json.dumps(
        TOOLS["mempalace_traverse"]["handler"](start_room=start_room, max_hops=max_hops),
        indent=2,
    )


@mcp.tool()
def mempalace_find_tunnels(wing_a: str = "", wing_b: str = "") -> str:
    """Find tunnels (paths) between two wings in the palace graph.

    Args:
        wing_a: Starting wing (optional)
        wing_b: Target wing (optional)
    """
    kwargs = {}
    if wing_a:
        kwargs["wing_a"] = wing_a
    if wing_b:
        kwargs["wing_b"] = wing_b
    return json.dumps(TOOLS["mempalace_find_tunnels"]["handler"](**kwargs), indent=2)


@mcp.tool()
def mempalace_graph_stats() -> str:
    """Get palace graph statistics."""
    return json.dumps(TOOLS["mempalace_graph_stats"]["handler"](), indent=2)


# --- Search tools ---


@mcp.tool()
def mempalace_search(query: str, wing: str = "", room: str = "", limit: int = 5) -> str:
    """Semantic search across all drawers, optional wing/room filter.

    Args:
        query: Search query text
        wing: Optional wing filter
        room: Optional room filter
        limit: Number of results (default: 5)
    """
    kwargs = {"query": query, "limit": limit}
    if wing:
        kwargs["wing"] = wing
    if room:
        kwargs["room"] = room
    return json.dumps(TOOLS["mempalace_search"]["handler"](**kwargs), indent=2)


@mcp.tool()
def mempalace_check_duplicate(content: str) -> str:
    """Check if content already exists in the palace before filing.

    Args:
        content: Content to check for duplicates
    """
    return json.dumps(
        TOOLS["mempalace_check_duplicate"]["handler"](content=content), indent=2
    )


# --- Write tools ---


@mcp.tool()
def mempalace_add_drawer(
    content: str, wing: str, room: str, source: str = ""
) -> str:
    """File verbatim content into a wing/room drawer.

    Args:
        content: The content to store
        wing: Wing name (category)
        room: Room name (subcategory)
        source: Optional source attribution
    """
    kwargs = {"content": content, "wing": wing, "room": room}
    if source:
        kwargs["source"] = source
    return json.dumps(TOOLS["mempalace_add_drawer"]["handler"](**kwargs), indent=2)


@mcp.tool()
def mempalace_delete_drawer(drawer_id: str) -> str:
    """Remove a drawer by ID.

    Args:
        drawer_id: ID of the drawer to delete
    """
    return json.dumps(
        TOOLS["mempalace_delete_drawer"]["handler"](drawer_id=drawer_id), indent=2
    )


# --- Diary tools ---


@mcp.tool()
def mempalace_diary_write(
    agent_name: str, entry: str, topic: str = "general"
) -> str:
    """Write to your personal agent diary in AAAK format.

    Args:
        agent_name: Your name — each agent gets their own diary wing
        entry: Your diary entry in AAAK format — compressed, entity-coded, emotion-marked
        topic: Topic tag (default: general)
    """
    return json.dumps(
        TOOLS["mempalace_diary_write"]["handler"](
            agent_name=agent_name, entry=entry, topic=topic
        ),
        indent=2,
    )


@mcp.tool()
def mempalace_diary_read(agent_name: str, last_n: int = 10) -> str:
    """Read your recent diary entries (in AAAK).

    Args:
        agent_name: Your name — each agent gets their own diary wing
        last_n: Number of recent entries to read (default: 10)
    """
    return json.dumps(
        TOOLS["mempalace_diary_read"]["handler"](agent_name=agent_name, last_n=last_n),
        indent=2,
    )


if __name__ == "__main__":
    logger.info("MemPalace MCP Server (FastMCP) starting...")
    mcp.run(transport="stdio")