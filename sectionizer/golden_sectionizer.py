#!/usr/bin/env python3
"""
Enhanced Two-Pass Sectionizer with Suppliers Detection
Includes all sections needed for the 16 essential agents
"""
import json
from typing import Dict, List, Optional

class GoldenSectionizer:
    """
    Enhanced sectionizer that detects all sections including suppliers
    """
    
    def __init__(self):
        # Define all possible section patterns to detect
        self.section_patterns = {
            # Level 1 - Main sections
            "table_of_contents": ["innehållsförteckning", "innehåll"],
            "management_report": ["förvaltningsberättelse", "verksamhetsberättelse"],
            "income_statement": ["resultaträkning"],
            "balance_sheet": ["balansräkning"],
            "cash_flow": ["kassaflödesanalys", "kassaflöde"],
            "notes": ["noter", "tilläggsupplysningar", "notupplysningar"],
            "signatures": ["underskrifter", "styrelsens underskrifter"],
            "audit_report": ["revisionsberättelse", "revisorns rapport"],
            
            # Level 2 - Subsections within management report
            "general_operations": ["allmänt om verksamheten", "verksamhet"],
            "board_info": ["styrelsen", "styrelseledamöter", "styrelsens sammansättning"],
            "property_info": ["föreningens fastighet", "fastigheten", "fastighetsinformation"],
            "member_info": ["medlemsinformation", "medlemmar", "antal medlemmar"],
            "significant_events": ["väsentliga händelser", "händelser under året"],
            "multi_year": ["flerårsöversikt", "femårsöversikt", "ekonomisk flerårsöversikt"],
            "economic_position": ["ekonomisk ställning", "nyckeltal"],
            
            # Level 2 - Subsections within notes
            "accounting_principles": ["redovisningsprinciper", "redovisnings- och värderingsprinciper"],
            "revenue_note": ["nettoomsättning", "rörelseintäkter", "intäkter"],
            "cost_note": ["driftskostnader", "kostnader", "rörelsekostnader"],
            "staff_note": ["personalkostnader", "anställda", "arvoden"],
            "buildings_note": ["byggnader och mark", "materiella anläggningstillgångar"],
            "depreciation_note": ["avskrivningar", "avskrivningsprinciper"],
            "loans_note": ["skulder till kreditinstitut", "långfristiga skulder", "lån"],
            "pledged_assets_note": ["ställda säkerheter", "panter", "ansvarsförbindelser"],
            
            # CRITICAL: Supplier sections (often in appendix or notes)
            "suppliers": [
                "leverantörer", 
                "leverantörsförteckning",
                "avtalspartners",
                "samarbetspartners",
                "tjänsteleverantörer",
                "entreprenörer",
                "serviceavtal",
                "avtalsparter"
            ],
            
            # Tables to detect
            "board_table": ["styrelsen har utgjorts av", "styrelsens sammansättning"],
            "multi_year_table": ["flerårsöversikt", "femårsöversikt"],
            "loan_table": ["låneförteckning", "kreditförteckning", "lån"],
            "cost_table": ["kostnadsspecifikation", "driftskostnader"],
            "supplier_table": ["leverantörslista", "avtalslista"]
        }
        
        # Agent mapping for each section type
        self.section_to_agents = {
            # Main sections
            "management_report": ["governance_agent", "property_agent", "maintenance_events_agent"],
            "income_statement": ["income_statement_agent"],
            "balance_sheet": ["balance_sheet_agent"],
            "cash_flow": ["cash_flow_agent"],
            "notes": ["note_loans_agent", "note_depreciation_agent", "note_costs_agent", 
                     "note_revenue_agent", "pledged_assets_agent"],
            "audit_report": ["audit_report_agent"],
            
            # Subsections
            "board_info": ["governance_agent"],
            "property_info": ["property_agent"],
            "member_info": ["member_info_agent"],
            "significant_events": ["maintenance_events_agent"],
            "multi_year": ["multi_year_overview_agent"],
            "economic_position": ["ratio_kpi_agent"],
            
            # Note subsections
            "loans_note": ["note_loans_agent"],
            "depreciation_note": ["note_depreciation_agent"],
            "cost_note": ["note_costs_agent"],
            "revenue_note": ["note_revenue_agent"],
            "pledged_assets_note": ["pledged_assets_agent"],
            
            # SUPPLIERS - Critical
            "suppliers": ["suppliers_vendors_agent"],
            "supplier_table": ["suppliers_vendors_agent"],
            
            # Tables
            "board_table": ["governance_agent"],
            "multi_year_table": ["multi_year_overview_agent"],
            "loan_table": ["note_loans_agent"],
            "cost_table": ["note_costs_agent"]
        }
    
    def get_discovery_prompt(self, focus_suppliers=False) -> str:
        """Get discovery prompt for Pass 1"""
        if focus_suppliers:
            # Special prompt for supplier detection
            return """Find ALL mentions of suppliers, vendors, and service providers in this document.
Look for:
- Leverantörer / Leverantörsförteckning
- Lists of company names providing services
- Avtalspartners / Samarbetspartners
- Banks, insurance companies, utilities, cleaning, maintenance companies
- Any table or list with company names and services

Return: [{"text": "section or company name", "page": N, "type": "supplier/vendor"}]"""
        
        return """Extract ALL section headers from these Swedish BRF annual report pages.
Look for main sections AND subsections:
- Förvaltningsberättelse, Resultaträkning, Balansräkning, Kassaflödesanalys
- Noter (and all individual notes), Revisionsberättelse
- Styrelsen, Fastigheten, Medlemsinformation, Väsentliga händelser
- Flerårsöversikt, Ekonomisk ställning, Nyckeltal
- IMPORTANT: Leverantörer, Leverantörsförteckning, Avtalspartners

Return: [{"text": "header text", "page": N, "level": 1/2/3, "type": "section/table/list"}]"""
    
    def get_verification_prompt(self, section_name: str) -> str:
        """Get verification prompt for Pass 2"""
        prompts = {
            "management_report": """Verify subsections in Förvaltningsberättelse:
- Allmänt om verksamheten (property details)
- Styrelsen (board composition)  
- Medlemsinformation (member statistics)
- Väsentliga händelser (significant events)
- Tables: Board members, Multi-year overview
Return: [{"text": "subsection", "page": N, "type": "text/table"}]""",
            
            "notes": """Verify individual notes (Noter):
Look for Note 1, 2, 3... or notes about:
- Redovisningsprinciper (accounting)
- Skulder till kreditinstitut (loans)
- Byggnader och mark (buildings)
- Driftskostnader (operating costs)
- Ställda säkerheter (pledged assets)
Return: [{"text": "Note X - Title", "page": N, "content_preview": "first line"}]""",
            
            "suppliers": """Find ALL supplier and vendor information:
- Company names providing services to the BRF
- Banks, insurance, utilities, maintenance contractors
- Contact information if available
- Service descriptions
Return: [{"company": "name", "service": "type", "page": N, "in_table": true/false}]"""
        }
        
        return prompts.get(section_name, f"Verify subsections for {section_name}")
    
    def map_sections_to_agents(self, sections: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Intelligent mapping of sections to agents
        Returns: {agent_name: [sections_to_process]}
        """
        agent_assignments = {}
        
        for section in sections:
            section_name = section.get("name", "").lower()
            section_type = section.get("type", "")
            
            # Find matching agents for this section
            matched_agents = []
            
            # Direct pattern matching
            for pattern_key, patterns in self.section_patterns.items():
                if any(p in section_name for p in patterns):
                    agents = self.section_to_agents.get(pattern_key, [])
                    matched_agents.extend(agents)
            
            # Special handling for suppliers (may be hidden)
            if any(supplier_keyword in section_name for supplier_keyword in 
                   ["leverantör", "avtal", "partner", "tjänst", "entreprenör"]):
                matched_agents.append("suppliers_vendors_agent")
            
            # Special handling for tables
            if section_type == "table":
                if "styrelse" in section_name:
                    matched_agents.append("governance_agent")
                elif "flerårs" in section_name:
                    matched_agents.append("multi_year_overview_agent")
                elif "lån" in section_name or "kredit" in section_name:
                    matched_agents.append("note_loans_agent")
            
            # Assign sections to agents
            for agent in set(matched_agents):  # Remove duplicates
                if agent not in agent_assignments:
                    agent_assignments[agent] = []
                agent_assignments[agent].append(section)
        
        # Ensure critical agents always run on their expected sections
        self._ensure_critical_coverage(agent_assignments, sections)
        
        return agent_assignments
    
    def _ensure_critical_coverage(self, assignments: Dict, all_sections: List[Dict]):
        """Ensure critical agents have sections even if not perfectly matched"""
        
        critical_mappings = {
            "governance_agent": ["förvaltning", "styrelse", "organisation"],
            "income_statement_agent": ["resultat"],
            "balance_sheet_agent": ["balans", "tillgång", "skuld"],
            "cash_flow_agent": ["kassa", "flöde"],
            "suppliers_vendors_agent": ["leverantör", "avtal", "tjänst", "service"]
        }
        
        for agent, keywords in critical_mappings.items():
            if agent not in assignments or not assignments[agent]:
                # Try to find sections for this agent
                for section in all_sections:
                    section_name = section.get("name", "").lower()
                    if any(kw in section_name for kw in keywords):
                        if agent not in assignments:
                            assignments[agent] = []
                        assignments[agent].append(section)
                        break

def generate_sectionizer_config():
    """Generate configuration for enhanced sectionizer"""
    
    sectionizer = GoldenSectionizer()
    
    config = {
        "section_patterns": sectionizer.section_patterns,
        "section_to_agents": sectionizer.section_to_agents,
        "discovery_prompts": {
            "general": sectionizer.get_discovery_prompt(False),
            "suppliers": sectionizer.get_discovery_prompt(True)
        },
        "special_instructions": {
            "suppliers": "Run supplier detection as additional pass if not found in main sections",
            "tables": "Identify tables by structure, not just headers",
            "notes": "Each note is a separate entity for targeted extraction"
        }
    }
    
    with open("/tmp/sectionizer_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("Enhanced Sectionizer Configuration Generated")
    print(f"Total section patterns: {len(sectionizer.section_patterns)}")
    print(f"Total agent mappings: {len(sectionizer.section_to_agents)}")
    print("✅ Suppliers detection included")

if __name__ == "__main__":
    generate_sectionizer_config()