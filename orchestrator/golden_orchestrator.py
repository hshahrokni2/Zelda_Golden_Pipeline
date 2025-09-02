#!/usr/bin/env python3
"""
Intelligent Learning Orchestrator with Autonomous Improvement
Maps sections to agents and learns from extraction failures
"""
import json
import hashlib
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class GoldenOrchestrator:
    """
    Orchestrator that:
    1. Maps sections to agents intelligently
    2. Validates and cross-checks results
    3. Learns from failures and improves
    4. Provides feedback for future extractions
    """
    
    def __init__(self, db_config: Optional[Dict] = None):
        self.learning_db = {}  # In production, use PostgreSQL
        self.validation_rules = self._init_validation_rules()
        self.agent_dependencies = self._init_dependencies()
        self.max_parallel = 4  # H100 constraint
        
        # Initialize Card G4 Reinforced Coach if enabled
        self.coach = None
        if os.getenv('COACHING_ENABLED') == 'true' and db_config:
            try:
                from coaching.card_g4_reinforced_coach import Card_G4_ReinforcedCoach
                self.coach = Card_G4_ReinforcedCoach(db_config)
                print("✅ Card G4 Reinforced Coach initialized")
            except Exception as e:
                print(f"⚠️ Coaching disabled: {e}")
        
    def _init_validation_rules(self) -> Dict:
        """Define validation rules for agent outputs"""
        return {
            "balance_check": {
                "rule": "total_assets == total_equity + total_liabilities",
                "agents": ["balance_sheet_agent"],
                "tolerance": 1000  # SEK tolerance for rounding
            },
            "cash_flow_check": {
                "rule": "opening_cash + total_cash_flow == closing_cash",
                "agents": ["cash_flow_agent"],
                "tolerance": 100
            },
            "income_check": {
                "rule": "total_revenues - total_costs == net_income",
                "agents": ["income_statement_agent"],
                "tolerance": 1000
            },
            "board_members_check": {
                "rule": "len(board_members) >= 3",  # Swedish law minimum
                "agents": ["governance_agent"]
            },
            "loan_total_check": {
                "rule": "sum(individual_loans) == total_loans",
                "agents": ["note_loans_agent"],
                "tolerance": 1000
            }
        }
    
    def _init_dependencies(self) -> Dict:
        """Define agent dependencies and relationships"""
        return {
            # Agents that should validate each other
            "cross_validation": [
                {
                    "agents": ["balance_sheet_agent", "note_loans_agent"],
                    "field": "long_term_debt",
                    "tolerance": 1000
                },
                {
                    "agents": ["income_statement_agent", "note_revenue_agent"],
                    "field": "total_revenues",
                    "tolerance": 1000
                },
                {
                    "agents": ["property_agent", "governance_agent"],
                    "field": "property_designation",
                    "exact_match": True
                }
            ],
            # Agents that share data
            "data_sharing": {
                "governance_agent": ["property_agent", "member_info_agent"],
                "balance_sheet_agent": ["ratio_kpi_agent"],
                "income_statement_agent": ["ratio_kpi_agent"],
                "multi_year_overview_agent": ["ratio_kpi_agent"]
            }
        }
    
    def map_sections_to_agents(self, sections: List[Dict]) -> Dict[str, Dict]:
        """
        Intelligent section-to-agent mapping with priority and dependencies
        """
        from sectionizer.golden_sectionizer import GoldenSectionizer
        sectionizer = GoldenSectionizer()
        
        # Get basic mapping
        agent_assignments = sectionizer.map_sections_to_agents(sections)
        
        # Enhance with page ranges and extraction zones
        enhanced_assignments = {}
        
        for agent_name, assigned_sections in agent_assignments.items():
            # Calculate page range for this agent
            all_pages = set()
            for section in assigned_sections:
                start = section.get("start_page", section.get("page", 1))
                end = section.get("end_page", start)
                all_pages.update(range(start, end + 1))
            
            enhanced_assignments[agent_name] = {
                "sections": assigned_sections,
                "pages": sorted(list(all_pages)),
                "extraction_zone": {
                    "start": min(all_pages) if all_pages else 1,
                    "end": max(all_pages) if all_pages else 1
                },
                "priority": self._get_agent_priority(agent_name),
                "expected_output": self._get_expected_fields(agent_name)
            }
        
        # Add learning hints from previous failures
        self._add_learning_hints(enhanced_assignments)
        
        return enhanced_assignments
    
    def _get_agent_priority(self, agent_name: str) -> int:
        """Get execution priority for agent"""
        priorities = {
            "governance_agent": 1,
            "income_statement_agent": 1,
            "balance_sheet_agent": 1,
            "cash_flow_agent": 1,
            "property_agent": 2,
            "multi_year_overview_agent": 2,
            "maintenance_events_agent": 2,
            "note_loans_agent": 2,
            "note_depreciation_agent": 2,
            "note_costs_agent": 2,
            "note_revenue_agent": 2,
            "suppliers_vendors_agent": 2,
            "audit_report_agent": 3,
            "ratio_kpi_agent": 3,
            "member_info_agent": 3,
            "pledged_assets_agent": 3
        }
        return priorities.get(agent_name, 4)
    
    def _get_expected_fields(self, agent_name: str) -> List[str]:
        """Get expected output fields for validation"""
        expected = {
            "governance_agent": ["chairman", "board_members", "auditor_name", "org_number"],
            "income_statement_agent": ["annual_fees", "total_revenues", "net_income"],
            "balance_sheet_agent": ["total_assets", "total_equity", "total_liabilities", "cash_and_bank"],
            "cash_flow_agent": ["operating_activities", "closing_cash"],
            "property_agent": ["property_designation", "address", "apartments_count"],
            "suppliers_vendors_agent": ["banking", "insurance", "utilities", "property_services"],
            "note_loans_agent": ["loans", "total_loans", "weighted_avg_rate"],
            "multi_year_overview_agent": ["years", "net_revenue", "solidity_percent"]
        }
        return expected.get(agent_name, [])
    
    def _add_learning_hints(self, assignments: Dict):
        """Add hints from previous learning to improve extraction"""
        for agent_name, config in assignments.items():
            # Check learning database for this agent
            hints = self.learning_db.get(agent_name, {}).get("hints", [])
            if hints:
                config["learning_hints"] = hints
    
    def validate_agent_output(self, agent_name: str, output: Dict, 
                             expected_fields: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate agent output and identify issues
        Returns: (is_valid, issues_list)
        """
        issues = []
        
        # Check for empty output
        if not output or output == {}:
            issues.append(f"Empty output from {agent_name}")
            return False, issues
        
        # Check for expected fields
        missing_fields = []
        empty_fields = []
        
        for field in expected_fields:
            if field not in output:
                missing_fields.append(field)
            elif not output[field] or output[field] == 0:
                empty_fields.append(field)
        
        if missing_fields:
            issues.append(f"Missing fields: {missing_fields}")
        if len(empty_fields) > len(expected_fields) * 0.5:  # More than 50% empty
            issues.append(f"Too many empty fields: {empty_fields}")
        
        # Apply validation rules
        for rule_name, rule_config in self.validation_rules.items():
            if agent_name in rule_config.get("agents", []):
                if not self._apply_validation_rule(output, rule_config):
                    issues.append(f"Failed validation: {rule_name}")
        
        return len(issues) == 0, issues
    
    def _apply_validation_rule(self, output: Dict, rule: Dict) -> bool:
        """Apply a specific validation rule"""
        try:
            if rule["rule"] == "total_assets == total_equity + total_liabilities":
                assets = output.get("total_assets", 0)
                equity = output.get("total_equity", 0)
                liabilities = output.get("total_liabilities", 0)
                return abs(assets - (equity + liabilities)) <= rule.get("tolerance", 0)
            
            elif rule["rule"] == "len(board_members) >= 3":
                members = output.get("board_members", [])
                return len(members) >= 3
            
            # Add more rule implementations as needed
            
        except Exception as e:
            print(f"Validation rule error: {e}")
            return False
        
        return True
    
    def learn_from_failure(self, agent_name: str, issues: List[str], 
                          section_content: str = "") -> Dict:
        """
        Learn from extraction failure and generate improvements
        """
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "issues": issues,
            "improvements": []
        }
        
        # Analyze issues and generate improvements
        if "Empty output" in str(issues):
            learning_entry["improvements"].append({
                "type": "prompt_enhancement",
                "suggestion": "Add more specific Swedish terms to search for",
                "hint": "Check if section contains tables that need special handling"
            })
            
            # Check if section might be in unexpected format
            if section_content:
                if "tabell" in section_content.lower():
                    learning_entry["improvements"].append({
                        "type": "table_detection",
                        "suggestion": "Section contains table - use table extractor",
                        "hint": "Tables need specialized extraction logic"
                    })
        
        if "Missing fields" in str(issues):
            learning_entry["improvements"].append({
                "type": "field_mapping",
                "suggestion": "Update field mappings for Swedish variations",
                "hint": "Common variations: årsstämma/stämma, ordförande/ordf"
            })
        
        if "Failed validation" in str(issues):
            learning_entry["improvements"].append({
                "type": "calculation_check",
                "suggestion": "Check for rounding or thousands separator issues",
                "hint": "Swedish uses space as thousands separator"
            })
        
        # Store learning
        if agent_name not in self.learning_db:
            self.learning_db[agent_name] = {"failures": [], "hints": []}
        
        self.learning_db[agent_name]["failures"].append(learning_entry)
        
        # Generate hint for next run
        new_hint = self._generate_hint_from_learning(learning_entry)
        if new_hint:
            self.learning_db[agent_name]["hints"].append(new_hint)
        
        return learning_entry
    
    def _generate_hint_from_learning(self, learning_entry: Dict) -> Optional[str]:
        """Generate actionable hint from learning entry"""
        if learning_entry["improvements"]:
            improvement = learning_entry["improvements"][0]
            return f"{improvement['type']}: {improvement['hint']}"
        return None
    
    def cross_validate_agents(self, results: Dict[str, Dict]) -> List[Dict]:
        """
        Cross-validate results between related agents
        """
        validations = []
        
        for validation_config in self.agent_dependencies["cross_validation"]:
            agents = validation_config["agents"]
            field = validation_config["field"]
            
            if all(agent in results for agent in agents):
                values = [results[agent].get(field) for agent in agents]
                
                if validation_config.get("exact_match"):
                    if len(set(values)) > 1:  # Not all same
                        validations.append({
                            "type": "mismatch",
                            "agents": agents,
                            "field": field,
                            "values": values,
                            "severity": "warning"
                        })
                else:
                    # Numeric comparison with tolerance
                    tolerance = validation_config.get("tolerance", 0)
                    if values[0] is not None and values[1] is not None:
                        if abs(values[0] - values[1]) > tolerance:
                            validations.append({
                                "type": "mismatch",
                                "agents": agents,
                                "field": field,
                                "values": values,
                                "severity": "warning",
                                "difference": abs(values[0] - values[1])
                            })
        
        return validations
    
    def generate_execution_plan(self, assignments: Dict) -> List[List[str]]:
        """
        Generate execution plan respecting priorities and H100 limits
        """
        # Group by priority
        by_priority = {}
        for agent, config in assignments.items():
            priority = config["priority"]
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(agent)
        
        # Create batches
        execution_batches = []
        for priority in sorted(by_priority.keys()):
            agents = by_priority[priority]
            for i in range(0, len(agents), self.max_parallel):
                batch = agents[i:i+self.max_parallel]
                execution_batches.append(batch)
        
        return execution_batches
    
    def process_with_coaching(self, doc_id: str, agent_name: str, 
                              extraction: Dict, ground_truth: Optional[Dict] = None) -> Dict:
        """
        Process extraction with Card G4 coaching if enabled
        """
        if not self.coach:
            return extraction
        
        try:
            # Apply coaching to improve extraction
            coached_extraction = self.coach.coach_extraction(
                doc_id=doc_id,
                agent_id=agent_name,
                current_extraction=extraction,
                ground_truth=ground_truth
            )
            
            # Log improvement
            if coached_extraction != extraction:
                print(f"  ✨ Coaching improved {agent_name} extraction")
            
            return coached_extraction
            
        except Exception as e:
            print(f"  ⚠️ Coaching failed for {agent_name}: {e}")
            return extraction
    
    def generate_coaching_feedback(self, agent_name: str, issues: List[str]) -> str:
        """
        Generate coaching prompt improvements based on issues
        """
        coaching = f"Coaching for {agent_name}:\n"
        
        if "Empty output" in str(issues):
            coaching += """
- Add fallback search terms in Swedish and English
- Look for tables and lists, not just text
- Check multiple pages if section spans pages
- Try OCR-friendly extraction for scanned documents
"""
        
        if "Missing fields" in str(issues):
            coaching += """
- Search for field variations: 
  * ordförande/styrelseordförande/chairman
  * årsstämma/bolagsstämma/stämma
  * revisor/auktoriserad revisor/godkänd revisor
- Check if data is in a table format
- Look in both current and previous year columns
"""
        
        if "Too many empty" in str(issues):
            coaching += """
- Section might be incorrectly identified
- Data might be on adjacent pages
- Consider that some documents use different terminology
- Check if this is a summary vs detailed section
"""
        
        return coaching
    
    def generate_test_scenario(self) -> Dict:
        """Generate comprehensive test scenario"""
        return {
            "test_name": "Intelligent Orchestrator Test",
            "test_sections": [
                {"name": "Förvaltningsberättelse", "start_page": 3, "end_page": 8, "type": "text"},
                {"name": "Styrelsen", "page": 4, "type": "subsection"},
                {"name": "Resultaträkning", "start_page": 9, "end_page": 10, "type": "table"},
                {"name": "Balansräkning", "start_page": 11, "end_page": 12, "type": "table"},
                {"name": "Noter", "start_page": 14, "end_page": 20, "type": "text"},
                {"name": "Leverantörer", "page": 28, "type": "list"}  # Suppliers!
            ],
            "expected_agents": [
                "governance_agent", "income_statement_agent", "balance_sheet_agent",
                "property_agent", "note_loans_agent", "suppliers_vendors_agent"
            ],
            "validation_checks": [
                "balance_sheet_validation",
                "cross_agent_validation",
                "supplier_detection"
            ]
        }

def main():
    """Test the intelligent orchestrator"""
    orchestrator = GoldenOrchestrator()
    
    print("INTELLIGENT LEARNING ORCHESTRATOR")
    print("="*60)
    
    # Generate test scenario
    test = orchestrator.generate_test_scenario()
    
    print(f"\n📋 TEST SCENARIO: {test['test_name']}")
    print(f"  Sections to process: {len(test['test_sections'])}")
    print(f"  Expected agents: {len(test['expected_agents'])}")
    
    # Map sections to agents
    assignments = orchestrator.map_sections_to_agents(test["test_sections"])
    
    print(f"\n🎯 SECTION-TO-AGENT MAPPING:")
    for agent, config in assignments.items():
        sections = [s["name"] for s in config["sections"]]
        print(f"  {agent}:")
        print(f"    Sections: {', '.join(sections)}")
        print(f"    Pages: {config['pages']}")
        print(f"    Priority: {config['priority']}")
    
    # Generate execution plan
    batches = orchestrator.generate_execution_plan(assignments)
    
    print(f"\n🔄 EXECUTION PLAN ({len(batches)} batches):")
    for i, batch in enumerate(batches, 1):
        print(f"  Batch {i}: {', '.join(batch)}")
    
    # Simulate validation failure and learning
    print(f"\n🧠 LEARNING SIMULATION:")
    
    # Simulate empty output from suppliers agent
    issues = ["Empty output from suppliers_vendors_agent"]
    learning = orchestrator.learn_from_failure("suppliers_vendors_agent", issues)
    
    print(f"  Issue: {issues[0]}")
    print(f"  Learning: {learning['improvements'][0]['suggestion']}")
    
    # Generate coaching
    coaching = orchestrator.generate_coaching_feedback("suppliers_vendors_agent", issues)
    print(f"\n📝 COACHING FEEDBACK:")
    print(coaching)
    
    # Save test configuration
    with open("/tmp/orchestrator_test.json", "w") as f:
        json.dump({
            "test_scenario": test,
            "assignments": {k: {
                "sections": [s["name"] for s in v["sections"]], 
                "pages": v["pages"],
                "priority": v["priority"]
            } for k, v in assignments.items()},
            "execution_batches": batches,
            "learning_example": learning
        }, f, indent=2)
    
    print(f"\n💾 Test configuration saved to /tmp/orchestrator_test.json")

if __name__ == "__main__":
    main()