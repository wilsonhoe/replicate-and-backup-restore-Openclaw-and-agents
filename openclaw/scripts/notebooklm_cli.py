#!/usr/bin/env python3
"""
NotebookLM CLI wrapper for OpenClaw agents
Provides simple interface to notebooklm-py
"""

import subprocess
import sys
import json
import argparse
from typing import Optional, List


def run_cmd(args: List[str]) -> tuple[bool, str]:
    """Run notebooklm command and return success, output"""
    result = subprocess.run(
        ["notebooklm"] + args,
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout.strip() if result.stdout else result.stderr.strip()


def cmd_login():
    """Authenticate with NotebookLM"""
    success, output = run_cmd(["login"])
    print(output if success else f"Error: {output}")
    return 0 if success else 1


def cmd_list():
    """List notebooks"""
    success, output = run_cmd(["list"])
    print(output)
    return 0 if success else 1


def cmd_create(name: str):
    """Create a new notebook"""
    success, output = run_cmd(["create", name])
    print(output)
    return 0 if success else 1


def cmd_use(notebook_id: str):
    """Set active notebook"""
    success, output = run_cmd(["use", notebook_id])
    print(output)
    return 0 if success else 1


def cmd_status():
    """Show current status"""
    success, output = run_cmd(["status"])
    print(output)
    return 0 if success else 1


def cmd_ask(question: str):
    """Ask the notebook a question"""
    success, output = run_cmd(["ask", question])
    print(output)
    return 0 if success else 1


def cmd_summary():
    """Get notebook summary"""
    success, output = run_cmd(["summary"])
    print(output)
    return 0 if success else 1


def cmd_source_add(path: str):
    """Add a source"""
    success, output = run_cmd(["source", "add", path])
    print(output)
    return 0 if success else 1


def cmd_source_list():
    """List sources"""
    success, output = run_cmd(["source", "list"])
    print(output)
    return 0 if success else 1


def cmd_source_research(query: str):
    """Add research source (auto web search)"""
    success, output = run_cmd(["source", "add-research", query])
    print(output)
    return 0 if success else 1


def cmd_source_wait():
    """Wait for sources to process"""
    success, output = run_cmd(["source", "wait"])
    print(output)
    return 0 if success else 1


def cmd_history():
    """Get conversation history"""
    success, output = run_cmd(["history"])
    print(output)
    return 0 if success else 1


def main():
    parser = argparse.ArgumentParser(description="NotebookLM CLI for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # login
    subparsers.add_parser("login", help="Authenticate with NotebookLM")

    # list
    subparsers.add_parser("list", help="List notebooks")

    # create
    create_parser = subparsers.add_parser("create", help="Create notebook")
    create_parser.add_argument("name", help="Notebook name")

    # use
    use_parser = subparsers.add_parser("use", help="Set active notebook")
    use_parser.add_argument("notebook_id", help="Notebook ID")

    # status
    subparsers.add_parser("status", help="Show current status")

    # ask
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("question", help="Question to ask")

    # summary
    subparsers.add_parser("summary", help="Get notebook summary")

    # history
    subparsers.add_parser("history", help="Get conversation history")

    # source commands
    source_parser = subparsers.add_parser("source", help="Source commands")
    source_subparsers = source_parser.add_subparsers(dest="source_command")

    # source add
    source_add = source_subparsers.add_parser("add", help="Add source")
    source_add.add_argument("path", help="File path or URL")

    # source list
    source_subparsers.add_parser("list", help="List sources")

    # source research
    source_research = source_subparsers.add_parser("research", help="Add research source")
    source_research.add_argument("query", help="Research query")

    # source wait
    source_subparsers.add_parser("wait", help="Wait for sources to process")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "login":
        return cmd_login()
    elif args.command == "list":
        return cmd_list()
    elif args.command == "create":
        return cmd_create(args.name)
    elif args.command == "use":
        return cmd_use(args.notebook_id)
    elif args.command == "status":
        return cmd_status()
    elif args.command == "ask":
        return cmd_ask(args.question)
    elif args.command == "summary":
        return cmd_summary()
    elif args.command == "history":
        return cmd_history()
    elif args.command == "source":
        if args.source_command == "add":
            return cmd_source_add(args.path)
        elif args.source_command == "list":
            return cmd_source_list()
        elif args.source_command == "research":
            return cmd_source_research(args.query)
        elif args.source_command == "wait":
            return cmd_source_wait()
        else:
            source_parser.print_help()
            return 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
