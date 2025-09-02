#!/usr/bin/env python3
"""
Dynamic Agent Loader - Loads agents from JSON for easy coaching updates
"""
import json
import os
from typing import Dict, Optional
from datetime import datetime

class AgentRegistry:
    """
    Dynamic agent registry that loads from JSON
    Allows for coaching updates without code changes
    """
    
    def __init__(self, registry_path: str = None):
        if registry_path is None:
            # Default to agent_registry.json in same directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            registry_path = os.path.join(current_dir, 'agent_registry.json')
        
        self.registry_path = registry_path
        self.agents = self.load_agents()
    
    def load_agents(self) -> Dict:
        """Load agents from JSON file"""
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['agents']
    
    def get_agent(self, agent_name: str) -> Optional[Dict]:
        """Get a specific agent configuration"""
        return self.agents.get(agent_name)
    
    def get_agent_prompt(self, agent_name: str) -> Optional[str]:
        """Get the prompt for a specific agent"""
        agent = self.get_agent(agent_name)
        return agent['prompt'] if agent else None
    
    def update_agent_prompt(self, agent_name: str, new_prompt: str, coaching_note: str = ""):
        """Update an agent's prompt after coaching"""
        if agent_name in self.agents:
            # Save old prompt to history
            old_prompt = self.agents[agent_name]['prompt']
            coaching_entry = {
                "timestamp": datetime.now().isoformat(),
                "old_prompt": old_prompt,
                "new_prompt": new_prompt,
                "note": coaching_note
            }
            self.agents[agent_name]['coaching_history'].append(coaching_entry)
            
            # Update prompt
            self.agents[agent_name]['prompt'] = new_prompt
            
            # Save to file
            self.save_agents()
    
    def save_agents(self):
        """Save agents back to JSON file"""
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data['agents'] = self.agents
        data['last_updated'] = datetime.now().isoformat()
        
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_all_agents(self) -> Dict:
        """Get all agents"""
        return self.agents
    
    def get_agents_by_priority(self, priority: int) -> Dict:
        """Get agents with specific priority"""
        return {
            name: agent 
            for name, agent in self.agents.items() 
            if agent['priority'] == priority
        }
    
    def generate_sql_inserts(self) -> str:
        """Generate SQL to insert/update agents in PostgreSQL"""
        sql_lines = [
            "-- Golden Agent Registry Update",
            "-- Generated: " + datetime.now().isoformat(),
            "",
            "BEGIN;",
            "",
            "-- Clear existing agents",
            "TRUNCATE TABLE agent_registry CASCADE;",
            ""
        ]
        
        for agent_name, agent_config in self.agents.items():
            handles = "ARRAY[" + ", ".join([f"'{h}'" for h in agent_config['handles']]) + "]"
            prompt = agent_config['prompt'].replace("'", "''")  # Escape single quotes
            
            sql_lines.append(f"""
INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    '{agent_name}',
    {agent_config['priority']},
    {handles},
    '{agent_config['description']}',
    '{prompt}',
    NOW(),
    NOW()
);""")
        
        sql_lines.append("")
        sql_lines.append("COMMIT;")
        sql_lines.append("")
        sql_lines.append("-- Verify insertion")
        sql_lines.append("SELECT COUNT(*) as agent_count FROM agent_registry;")
        
        return "\n".join(sql_lines)

# Example usage
if __name__ == "__main__":
    registry = AgentRegistry()
    
    print("🤖 GOLDEN AGENT REGISTRY")
    print("="*60)
    print(f"Total agents: {len(registry.get_all_agents())}")
    
    # Show agents by priority
    for priority in [1, 2, 3]:
        agents = registry.get_agents_by_priority(priority)
        print(f"\nPriority {priority}: {len(agents)} agents")
        for name in agents:
            print(f"  - {name}")
    
    # Check for suppliers agent
    suppliers = registry.get_agent("suppliers_vendors_agent")
    if suppliers:
        print(f"\n⭐ Suppliers agent present: {suppliers['description']}")
    
    # Generate SQL
    sql_file = os.path.join(os.path.dirname(__file__), 'update_postgres_agents.sql')
    with open(sql_file, 'w') as f:
        f.write(registry.generate_sql_inserts())
    print(f"\n💾 SQL update script generated: {sql_file}")