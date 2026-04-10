#!/usr/bin/env python3
"""
Ontology Integration Wrapper for OpenClaw
Provides simple functions to interact with the ontology system
"""

import subprocess
import json
import sys
from pathlib import Path

ONTOLOGY_SCRIPT = Path.home() / ".openclaw" / "workspace" / "skills" / "ontology" / "scripts" / "ontology.py"

def run_ontology_command(args):
    """Run an ontology command and return the result"""
    try:
        cmd = [sys.executable, str(ONTOLOGY_SCRIPT)] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path.home() / ".openclaw" / "workspace"))
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                try:
                    return json.loads(output)
                except json.JSONDecodeError:
                    return output
            return output
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"

def create_entity(entity_type, properties):
    """Create a new entity in the ontology"""
    props_json = json.dumps(properties)
    return run_ontology_command(["create", "--type", entity_type, "--props", props_json])

def query_entities(entity_type, where_clause=None):
    """Query entities of a specific type"""
    args = ["query", "--type", entity_type]
    if where_clause:
        where_json = json.dumps(where_clause)
        args.extend(["--where", where_json])
    return run_ontology_command(args)

def get_entity(entity_id):
    """Get a specific entity by ID"""
    return run_ontology_command(["get", "--id", entity_id])

def relate_entities(from_id, relation, to_id):
    """Create a relationship between entities"""
    return run_ontology_command(["relate", "--from", from_id, "--rel", relation, "--to", to_id])

def get_related(entity_id, relation):
    """Get entities related to the given entity"""
    return run_ontology_command(["related", "--id", entity_id, "--rel", relation])

def validate_ontology():
    """Validate the entire ontology graph"""
    return run_ontology_command(["validate"])

def list_entities(entity_type):
    """List all entities of a specific type"""
    return run_ontology_command(["list", "--type", entity_type])

def delete_entity(entity_id):
    """Delete an entity from the ontology"""
    return run_ontology_command(["delete", "--id", entity_id])

if __name__ == "__main__":
    print("Testing ontology integration...")
    
    # Test validation
    print("\n1. Validating ontology:")
    result = validate_ontology()
    print(f"   Result: {result}")
    
    # Test query
    print("\n2. Querying projects:")
    projects = query_entities("Project", {"status": "active"})
    print(f"   Active projects: {json.dumps(projects, indent=2) if projects else 'None'}")
    
    # Test get related
    if isinstance(projects, list) and len(projects) > 0:
        project_id = projects[0]["id"]
        print(f"\n3. Getting owner of project {project_id}:")
        owner = get_related(project_id, "has_owner")
        print(f"   Owner: {json.dumps(owner, indent=2) if owner else 'None'}")
    
    print("\n✅ Ontology integration test completed!")