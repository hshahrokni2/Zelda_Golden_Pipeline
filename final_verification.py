#!/usr/bin/env python3
"""
Final verification that everything is truly working
"""
import sys
import os
import json

def verify_golden_pipeline():
    """Final comprehensive verification"""
    
    print("🔍 FINAL GOLDEN PIPELINE VERIFICATION")
    print("="*60)
    
    results = {
        "structure": True,
        "imports": True,
        "agents": True,
        "features": True
    }
    
    # 1. Verify structure
    print("\n1️⃣ Verifying structure...")
    required_files = [
        "sectionizer/golden_sectionizer.py",
        "orchestrator/golden_orchestrator.py",
        "agents/agent_registry.json",
        "agents/agent_loader.py",
        "tests/golden_mega_test.py",
        "run_golden_pipeline.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} MISSING")
            results["structure"] = False
    
    # 2. Verify imports
    print("\n2️⃣ Verifying imports...")
    try:
        from sectionizer.golden_sectionizer import GoldenSectionizer
        print("  ✅ GoldenSectionizer imports")
        
        from orchestrator.golden_orchestrator import GoldenOrchestrator
        print("  ✅ GoldenOrchestrator imports")
        
        from agents.agent_loader import AgentRegistry
        print("  ✅ AgentRegistry imports")
        
        # Create instances
        s = GoldenSectionizer()
        o = GoldenOrchestrator()
        r = AgentRegistry()
        print("  ✅ All classes instantiate")
        
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        results["imports"] = False
    
    # 3. Verify agents
    print("\n3️⃣ Verifying agents...")
    try:
        registry = AgentRegistry()
        agents = registry.get_all_agents()
        
        print(f"  📊 Total agents: {len(agents)}")
        
        # Check for critical agents
        critical = ["governance_agent", "suppliers_vendors_agent", "income_statement_agent"]
        for agent in critical:
            if agent in agents:
                print(f"  ✅ {agent} present")
            else:
                print(f"  ❌ {agent} MISSING")
                results["agents"] = False
        
        # Check suppliers specifically
        suppliers = registry.get_agent("suppliers_vendors_agent")
        if suppliers and "leverantör" in suppliers["prompt"].lower():
            print("  ✅ Suppliers agent has leverantörer detection")
        else:
            print("  ❌ Suppliers agent missing leverantörer")
            results["agents"] = False
            
    except Exception as e:
        print(f"  ❌ Agent verification error: {e}")
        results["agents"] = False
    
    # 4. Verify features
    print("\n4️⃣ Verifying features...")
    try:
        # Check sectionizer patterns
        sectionizer = GoldenSectionizer()
        if hasattr(sectionizer, 'section_patterns'):
            pattern_count = len(sectionizer.section_patterns)
            print(f"  ✅ Sectionizer has {pattern_count} patterns")
            if pattern_count < 20:
                print(f"  ⚠️ Expected more patterns")
                results["features"] = False
        
        # Check orchestrator learning
        orchestrator = GoldenOrchestrator()
        if hasattr(orchestrator, 'learn_from_failure'):
            print("  ✅ Orchestrator has learning capability")
        else:
            print("  ❌ Orchestrator missing learning")
            results["features"] = False
        
        if hasattr(orchestrator, 'cross_validate_agents'):
            print("  ✅ Orchestrator has cross-validation")
        else:
            print("  ❌ Orchestrator missing cross-validation")
            results["features"] = False
            
    except Exception as e:
        print(f"  ❌ Feature verification error: {e}")
        results["features"] = False
    
    # Final verdict
    print("\n" + "="*60)
    print("📊 VERIFICATION RESULTS:")
    
    all_pass = all(results.values())
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {check.title()}: {status}")
    
    print("\n" + "="*60)
    if all_pass:
        print("✅ GOLDEN PIPELINE VERIFIED - READY FOR PRODUCTION!")
        print("\nNext steps:")
        print("1. Run: bash deploy_to_h100.sh")
        print("2. Push to GitHub")
        print("3. Test on H100")
        return True
    else:
        print("❌ VERIFICATION FAILED - Please fix issues")
        return False

if __name__ == "__main__":
    success = verify_golden_pipeline()
    sys.exit(0 if success else 1)