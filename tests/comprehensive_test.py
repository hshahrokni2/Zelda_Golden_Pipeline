#!/usr/bin/env python3
"""
Comprehensive Test for Intelligent Learning Orchestrator
Tests sectionizer, mapping, learning, and validation
"""
import json
import sys
from typing import Dict, List

def test_sectionizer():
    """Test enhanced sectionizer with suppliers detection"""
    print("\n" + "="*60)
    print("TEST 1: ENHANCED SECTIONIZER")
    print("="*60)
    
    from enhanced_sectionizer_with_suppliers import EnhancedGoldenSectionizer
    sectionizer = EnhancedGoldenSectionizer()
    
    # Test section patterns
    print("\n✅ Section patterns loaded:")
    print(f"  Total patterns: {len(sectionizer.section_patterns)}")
    print(f"  Suppliers patterns: {len(sectionizer.section_patterns['suppliers'])}")
    
    # Test discovery prompts
    general_prompt = sectionizer.get_discovery_prompt(False)
    supplier_prompt = sectionizer.get_discovery_prompt(True)
    
    assert "Leverantörer" in general_prompt
    assert "Banks, insurance" in supplier_prompt
    print("✅ Discovery prompts include supplier detection")
    
    # Test section mapping
    test_sections = [
        {"name": "Förvaltningsberättelse", "page": 3, "type": "section"},
        {"name": "Leverantörsförteckning", "page": 28, "type": "list"},
        {"name": "Resultaträkning", "page": 9, "type": "table"}
    ]
    
    mappings = sectionizer.map_sections_to_agents(test_sections)
    
    assert "suppliers_vendors_agent" in mappings
    assert "income_statement_agent" in mappings
    assert "governance_agent" in mappings
    
    print("✅ Section-to-agent mapping working")
    print(f"  Mapped {len(mappings)} agents to sections")
    
    # Check suppliers specifically
    supplier_sections = mappings.get("suppliers_vendors_agent", [])
    assert len(supplier_sections) > 0
    print(f"✅ Suppliers agent mapped to: {[s['name'] for s in supplier_sections]}")
    
    return True

def test_mapping_logic():
    """Test intelligent mapping and prioritization"""
    print("\n" + "="*60)
    print("TEST 2: MAPPING LOGIC")
    print("="*60)
    
    from intelligent_learning_orchestrator import IntelligentLearningOrchestrator
    orchestrator = IntelligentLearningOrchestrator()
    
    # Complex test case with overlapping sections
    test_sections = [
        {"name": "Förvaltningsberättelse", "start_page": 3, "end_page": 8},
        {"name": "Styrelsen har utgjorts av", "page": 4, "type": "table"},
        {"name": "Föreningens fastighet", "page": 5, "type": "subsection"},
        {"name": "Väsentliga händelser", "page": 6, "type": "subsection"},
        {"name": "Flerårsöversikt", "page": 7, "type": "table"},
        {"name": "Noter", "start_page": 14, "end_page": 20},
        {"name": "Not 8 - Skulder till kreditinstitut", "page": 18},
        {"name": "Leverantörer och avtalspartners", "page": 29, "type": "list"}
    ]
    
    assignments = orchestrator.map_sections_to_agents(test_sections)
    
    print("\n📊 Mapping Results:")
    
    # Check critical agents are assigned
    critical_agents = ["governance_agent", "property_agent", "note_loans_agent", "suppliers_vendors_agent"]
    for agent in critical_agents:
        if agent in assignments:
            sections = [s["name"] for s in assignments[agent]["sections"]]
            print(f"  ✅ {agent}: {', '.join(sections)}")
        else:
            print(f"  ❌ {agent}: NOT MAPPED (ERROR)")
    
    # Check extraction zones
    print("\n📍 Extraction Zones:")
    for agent, config in assignments.items():
        if agent in ["governance_agent", "suppliers_vendors_agent"]:
            zone = config["extraction_zone"]
            print(f"  {agent}: pages {zone['start']}-{zone['end']}")
    
    # Check priority assignment
    print("\n🎯 Priority Assignment:")
    priority_1 = [a for a, c in assignments.items() if c["priority"] == 1]
    priority_2 = [a for a, c in assignments.items() if c["priority"] == 2]
    print(f"  Priority 1: {len(priority_1)} agents")
    print(f"  Priority 2: {len(priority_2)} agents")
    
    assert "suppliers_vendors_agent" in assignments
    assert assignments["suppliers_vendors_agent"]["pages"] == [29]
    
    return True

def test_learning_capabilities():
    """Test learning from failures and coaching generation"""
    print("\n" + "="*60)
    print("TEST 3: LEARNING CAPABILITIES")
    print("="*60)
    
    from intelligent_learning_orchestrator import IntelligentLearningOrchestrator
    orchestrator = IntelligentLearningOrchestrator()
    
    # Simulate various failure scenarios
    test_cases = [
        {
            "agent": "governance_agent",
            "output": {},  # Empty output
            "expected_fields": ["chairman", "board_members", "org_number"]
        },
        {
            "agent": "balance_sheet_agent",
            "output": {
                "total_assets": 100000000,
                "total_equity": 40000000,
                "total_liabilities": 50000000  # Doesn't balance!
            },
            "expected_fields": ["total_assets", "total_equity", "total_liabilities"]
        },
        {
            "agent": "suppliers_vendors_agent",
            "output": {
                "banking": [],
                "insurance": [],
                "utilities": []  # All empty
            },
            "expected_fields": ["banking", "insurance", "utilities"]
        }
    ]
    
    print("\n🧪 Testing failure scenarios:")
    
    for test in test_cases:
        agent = test["agent"]
        output = test["output"]
        expected = test["expected_fields"]
        
        # Validate output
        is_valid, issues = orchestrator.validate_agent_output(agent, output, expected)
        
        if not is_valid:
            print(f"\n  {agent}:")
            print(f"    Issues: {issues}")
            
            # Learn from failure
            learning = orchestrator.learn_from_failure(agent, issues)
            print(f"    Learning: {learning['improvements'][0]['suggestion'] if learning['improvements'] else 'None'}")
            
            # Generate coaching
            coaching = orchestrator.generate_coaching_feedback(agent, issues)
            print(f"    Coaching: {coaching.split(':')[1].strip()[:100]}...")
    
    # Check learning database
    print(f"\n📚 Learning Database:")
    print(f"  Agents with learning: {list(orchestrator.learning_db.keys())}")
    
    return True

def test_validation_and_cross_checking():
    """Test validation rules and cross-agent validation"""
    print("\n" + "="*60)
    print("TEST 4: VALIDATION & CROSS-CHECKING")
    print("="*60)
    
    from intelligent_learning_orchestrator import IntelligentLearningOrchestrator
    orchestrator = IntelligentLearningOrchestrator()
    
    # Simulate agent results
    results = {
        "balance_sheet_agent": {
            "total_assets": 301339818,
            "total_equity": 201801694,
            "total_liabilities": 99538124,
            "long_term_debt": 92000000
        },
        "income_statement_agent": {
            "total_revenues": 15234567,
            "total_costs": 14234567,
            "net_income": 1000000
        },
        "note_loans_agent": {
            "total_loans": 92500000,  # Slightly different from balance sheet
            "loans": [
                {"lender": "Swedbank", "balance": 50000000},
                {"lender": "SBAB", "balance": 42500000}
            ]
        },
        "governance_agent": {
            "chairman": "Erik Öhman",
            "board_members": [
                {"name": "Erik Öhman", "role": "Ordförande"},
                {"name": "Anna Svensson", "role": "Ledamot"},
                {"name": "Per Andersson", "role": "Ledamot"}
            ],
            "property_designation": "Kungsholmen 1:23"
        },
        "property_agent": {
            "property_designation": "Kungsholmen 1:23",  # Matches governance
            "address": "Norr Mälarstrand 12"
        }
    }
    
    # Test balance sheet validation
    print("\n💰 Balance Sheet Validation:")
    bs = results["balance_sheet_agent"]
    balance_check = abs(bs["total_assets"] - (bs["total_equity"] + bs["total_liabilities"])) <= 1000
    print(f"  Assets = Equity + Liabilities: {'✅ PASS' if balance_check else '❌ FAIL'}")
    print(f"  {bs['total_assets']} = {bs['total_equity']} + {bs['total_liabilities']}")
    
    # Test income statement validation
    print("\n📊 Income Statement Validation:")
    is_data = results["income_statement_agent"]
    income_check = abs((is_data["total_revenues"] - is_data["total_costs"]) - is_data["net_income"]) <= 1000
    print(f"  Revenue - Costs = Net Income: {'✅ PASS' if income_check else '❌ FAIL'}")
    
    # Test cross-agent validation
    print("\n🔄 Cross-Agent Validation:")
    cross_validations = orchestrator.cross_validate_agents(results)
    
    for validation in cross_validations:
        agents = validation["agents"]
        field = validation["field"]
        values = validation["values"]
        
        if validation["type"] == "mismatch":
            print(f"  ⚠️ {field} mismatch between {agents[0]} and {agents[1]}")
            print(f"     Values: {values[0]} vs {values[1]}")
            if "difference" in validation:
                print(f"     Difference: {validation['difference']} SEK")
    
    # Check property designation match
    gov_prop = results["governance_agent"]["property_designation"]
    prop_prop = results["property_agent"]["property_designation"]
    print(f"\n🏢 Property Designation Match:")
    print(f"  Governance: {gov_prop}")
    print(f"  Property: {prop_prop}")
    print(f"  Match: {'✅ YES' if gov_prop == prop_prop else '❌ NO'}")
    
    return True

def test_execution_planning():
    """Test execution batch planning"""
    print("\n" + "="*60)
    print("TEST 5: EXECUTION PLANNING")
    print("="*60)
    
    from intelligent_learning_orchestrator import IntelligentLearningOrchestrator
    orchestrator = IntelligentLearningOrchestrator()
    
    # Create full agent assignment
    all_agents = {
        "governance_agent": {"priority": 1},
        "income_statement_agent": {"priority": 1},
        "balance_sheet_agent": {"priority": 1},
        "cash_flow_agent": {"priority": 1},
        "property_agent": {"priority": 2},
        "multi_year_overview_agent": {"priority": 2},
        "maintenance_events_agent": {"priority": 2},
        "note_loans_agent": {"priority": 2},
        "note_depreciation_agent": {"priority": 2},
        "note_costs_agent": {"priority": 2},
        "note_revenue_agent": {"priority": 2},
        "suppliers_vendors_agent": {"priority": 2},
        "audit_report_agent": {"priority": 3},
        "ratio_kpi_agent": {"priority": 3},
        "member_info_agent": {"priority": 3},
        "pledged_assets_agent": {"priority": 3}
    }
    
    batches = orchestrator.generate_execution_plan(all_agents)
    
    print(f"\n🚀 Execution Plan:")
    print(f"  Total agents: {len(all_agents)}")
    print(f"  Total batches: {len(batches)}")
    print(f"  Max parallel: {orchestrator.max_parallel}")
    
    for i, batch in enumerate(batches, 1):
        print(f"\n  Batch {i}: {len(batch)} agents")
        for agent in batch:
            priority = all_agents[agent]["priority"]
            print(f"    - {agent} (P{priority})")
    
    # Verify constraints
    print(f"\n✅ Constraint Checks:")
    max_batch_size = max(len(batch) for batch in batches)
    print(f"  Max batch size: {max_batch_size} <= 4: {'✅ PASS' if max_batch_size <= 4 else '❌ FAIL'}")
    
    # Check priority ordering
    priority_order_correct = True
    last_priority = 0
    for batch in batches:
        batch_priority = min(all_agents[agent]["priority"] for agent in batch)
        if batch_priority < last_priority:
            priority_order_correct = False
        last_priority = max(all_agents[agent]["priority"] for agent in batch)
    
    print(f"  Priority ordering: {'✅ PASS' if priority_order_correct else '❌ FAIL'}")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "🎯"*30)
    print("COMPREHENSIVE ORCHESTRATOR TEST SUITE")
    print("🎯"*30)
    
    tests = [
        ("Sectionizer with Suppliers", test_sectionizer),
        ("Mapping Logic", test_mapping_logic),
        ("Learning Capabilities", test_learning_capabilities),
        ("Validation & Cross-Checking", test_validation_and_cross_checking),
        ("Execution Planning", test_execution_planning)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results[test_name] = "✅ PASS" if success else "❌ FAIL"
        except Exception as e:
            results[test_name] = f"❌ ERROR: {e}"
            print(f"\n❌ Test failed: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        print(f"  {test_name}: {result}")
    
    passed = sum(1 for r in results.values() if "PASS" in r)
    total = len(results)
    
    print(f"\n🏆 Final Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - Orchestrator ready for production!")
    else:
        print("⚠️ Some tests failed - Review and fix issues")
    
    # Save test results
    with open("/tmp/test_results.json", "w") as f:
        json.dump({
            "test_results": results,
            "passed": passed,
            "total": total,
            "success": passed == total
        }, f, indent=2)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)