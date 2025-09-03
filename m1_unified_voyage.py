#!/usr/bin/env python3
"""
🚢 M1 UNIFIED VOYAGE - Testing Golden Fortress System
Combines Golden Orchestrator + Twin-Pipeline Card G4
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add paths for both systems
sys.path.append('/tmp/Golden_Orchestrator_Pipeline')
sys.path.append('/tmp/twin-pipeline')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class UnifiedVoyage:
    """Unified maiden voyage for Golden Fortress system"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'performance': {},
            'errors': []
        }
        self.pdf_path = None
        
    def find_test_pdf(self) -> str:
        """Find a test PDF to use"""
        candidates = [
            '/tmp/Golden_Orchestrator_Pipeline/test_document.pdf',
            '/tmp/twin-pipeline/sample_brf_document.pdf',
            'test_document.pdf'
        ]
        
        for path in candidates:
            if os.path.exists(path):
                logger.info(f"✅ Found test PDF: {path}")
                return path
                
        logger.error("❌ No test PDF found")
        return None
        
    def test_golden_sectionizer(self) -> bool:
        """Test Golden Sectionizer with 29 patterns"""
        logger.info("📌 Testing Golden Sectionizer...")
        try:
            from sectionizer.golden_sectionizer import GoldenSectionizer
            
            sectionizer = GoldenSectionizer()
            logger.info("  ✅ Golden Sectionizer loaded")
            
            # Check patterns
            import json
            with open('/tmp/twin-pipeline/src/sectionizer/golden_patterns.json', 'r') as f:
                patterns = json.load(f)
                pattern_count = len(patterns.get('section_patterns', []))
                logger.info(f"  ✅ {pattern_count} patterns available")
                
            self.results['tests']['golden_sectionizer'] = {
                'status': 'PASS',
                'patterns': pattern_count
            }
            return True
            
        except Exception as e:
            logger.error(f"  ❌ Sectionizer failed: {e}")
            self.results['tests']['golden_sectionizer'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
            
    def test_card_g4_coaching(self) -> bool:
        """Test Card G4 Reinforced Learning"""
        logger.info("📌 Testing Card G4 Coaching...")
        try:
            # Try twin-pipeline version first
            sys.path.insert(0, '/tmp/twin-pipeline')
            from src.coaching.card_g4_reinforced_coach_fixed import Card_G4_ReinforcedCoach
            
            # FIXED: Use standard database config dict, not connection object
            db_config = {
                'host': 'localhost',
                'port': 5432,
                'database': 'zelda_arsredovisning',
                'user': 'postgres',
                'password': 'h100pass'
            }
            
            coach = Card_G4_ReinforcedCoach(db_config)
            phase = coach.learning_phase
            logger.info(f"  ✅ Card G4 initialized - Phase {phase}")
            
            # Test performance analysis
            mock_extraction = {'test': 'data'}
            performance = coach.analyze_performance(mock_extraction, None)
            logger.info(f"  ✅ Performance analysis working")
            
            self.results['tests']['card_g4_coaching'] = {
                'status': 'PASS',
                'learning_phase': phase
            }
            return True
            
        except Exception as e:
            logger.error(f"  ❌ Card G4 failed: {e}")
            self.results['tests']['card_g4_coaching'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
            
    def test_unified_coach(self) -> bool:
        """Test Unified Coach integration"""
        logger.info("📌 Testing Unified Coach...")
        try:
            sys.path.insert(0, '/tmp/twin-pipeline')
            from src.orchestrator.unified_coach import UnifiedCoach
            
            db_config = {
                'host': 'localhost',
                'port': 5432,
                'database': 'zelda_arsredovisning',
                'user': 'postgres',
                'password': 'h100pass'
            }
            
            coach = UnifiedCoach(db_config)
            status = coach.get_status()
            
            logger.info(f"  ✅ Card G4: {'Available' if status['card_g4_available'] else 'Not available'}")
            logger.info(f"  ✅ DB Coach: {'Available' if status['db_coach_available'] else 'Not available'}")
            
            self.results['tests']['unified_coach'] = {
                'status': 'PASS',
                'card_g4': status['card_g4_available'],
                'db_coach': status['db_coach_available']
            }
            return True
            
        except Exception as e:
            logger.error(f"  ❌ Unified Coach failed: {e}")
            self.results['tests']['unified_coach'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
            
    def test_agent_registry(self) -> bool:
        """Test 16-agent registry"""
        logger.info("📌 Testing Agent Registry...")
        try:
            with open('/tmp/twin-pipeline/src/agents/golden_registry.json', 'r') as f:
                registry = json.load(f)
                agent_count = len(registry['agents'])
                
            logger.info(f"  ✅ {agent_count} agents in registry")
            
            # Count by priority
            priorities = {}
            for agent_name, agent_data in registry['agents'].items():
                p = agent_data['priority']
                priorities[p] = priorities.get(p, 0) + 1
                
            for p in sorted(priorities.keys()):
                logger.info(f"    - Priority {p}: {priorities[p]} agents")
                
            self.results['tests']['agent_registry'] = {
                'status': 'PASS',
                'total_agents': agent_count,
                'by_priority': priorities
            }
            return True
            
        except Exception as e:
            logger.error(f"  ❌ Agent registry failed: {e}")
            self.results['tests']['agent_registry'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
            
    def run_voyage(self) -> Dict:
        """Execute the complete unified voyage"""
        logger.info("=" * 80)
        logger.info("🚢 M1 UNIFIED VOYAGE - GOLDEN FORTRESS SYSTEM")
        logger.info("=" * 80)
        logger.info("")
        
        start_time = time.time()
        
        # Find test PDF
        self.pdf_path = self.find_test_pdf()
        if not self.pdf_path:
            logger.error("Cannot proceed without test PDF")
            return self.results
            
        # Run tests
        tests = [
            ('Golden Sectionizer', self.test_golden_sectionizer),
            ('Card G4 Coaching', self.test_card_g4_coaching),
            ('Unified Coach', self.test_unified_coach),
            ('Agent Registry', self.test_agent_registry)
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            logger.info("")
            if test_func():
                passed += 1
            else:
                failed += 1
                
        # Calculate performance
        duration = time.time() - start_time
        self.results['performance'] = {
            'duration_seconds': round(duration, 2),
            'tests_passed': passed,
            'tests_failed': failed,
            'success_rate': round(passed / (passed + failed) * 100, 1)
        }
        
        # Determine success level
        if passed == len(tests):
            success_level = "EXCELLENT"
        elif passed >= len(tests) * 0.75:
            success_level = "GOOD"
        elif passed >= len(tests) * 0.5:
            success_level = "MINIMUM"
        else:
            success_level = "FAILED"
            
        logger.info("")
        logger.info("=" * 80)
        logger.info("🏁 VOYAGE COMPLETE")
        logger.info("=" * 80)
        logger.info(f"  ✅ Tests Passed: {passed}/{len(tests)}")
        logger.info(f"  ⏱️ Duration: {duration:.2f}s")
        logger.info(f"  🎯 Success Level: {success_level}")
        logger.info("")
        
        # Save results
        results_file = f'/tmp/m1_unified_voyage_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"📊 Results saved to: {results_file}")
        
        return self.results

def main():
    """Main entry point"""
    voyage = UnifiedVoyage()
    results = voyage.run_voyage()
    
    # Exit with appropriate code
    if results['performance'].get('tests_failed', 1) > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()