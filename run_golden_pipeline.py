#!/usr/bin/env python3
"""
Golden Orchestrator Pipeline - Main Entry Point
Run this to test the complete system
"""
import sys
import os

# Add Golden directories to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sectionizer'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'orchestrator'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

def main():
    print("🎯 GOLDEN ORCHESTRATOR PIPELINE")
    print("="*60)
    
    # Import and run the mega test
    from tests.golden_mega_test import MegaOrchestratorTest
    
    tester = MegaOrchestratorTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ GOLDEN PIPELINE READY FOR PRODUCTION!")
    else:
        print("\n⚠️ Some tests failed - check logs")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
