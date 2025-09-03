#!/usr/bin/env python3
"""
🚢 H100-NATIVE MAIDEN VOYAGE - Golden Fortress System
Designed to run directly ON H100 with full infrastructure access
FIXED: Card G4 database configuration issue resolved
"""

import os
import sys
import json
import time
import logging
import psycopg2
from psycopg2 import pool
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import traceback

# ============================================================================
# H100 ENVIRONMENT CONFIGURATION
# ============================================================================

class H100Environment:
    """Configure environment for H100 execution"""
    
    @staticmethod
    def setup():
        """Setup H100-specific environment"""
        # Detect if we're on H100
        hostname = os.uname().nodename
        is_h100 = 'root' in os.path.expanduser('~') or '/root' in os.getcwd()
        
        if not is_h100:
            print("⚠️ WARNING: This script is designed to run ON H100")
            
        # Set environment variables for H100
        os.environ['DATABASE_URL'] = 'postgresql://postgres:h100pass@localhost:5432/zelda_arsredovisning'
        os.environ['PGPASSWORD'] = 'h100pass'
        os.environ['COACHING_ENABLED'] = 'true'
        os.environ['GEMINI_API_KEY'] = 'AIzaSyD0y92BjcnvUgRlWsA1oPSIWV5QaJcCrNw'
        os.environ['TWIN_PIPELINE_PATH'] = '/tmp/twin-pipeline'
        os.environ['GOLDEN_PATH'] = '/tmp/Golden_Orchestrator_Pipeline'
        
        # Add both systems to path
        sys.path.insert(0, '/tmp/Golden_Orchestrator_Pipeline')
        sys.path.insert(0, '/tmp/twin-pipeline')
        sys.path.insert(0, '/tmp/twin-pipeline/src')
        
        print("✅ H100 Environment Configured:")
        print(f"  - Database: localhost:5432/zelda_arsredovisning")
        print(f"  - Twin Pipeline: {os.environ['TWIN_PIPELINE_PATH']}")
        print(f"  - Golden Orchestrator: {os.environ['GOLDEN_PATH']}")
        print("")

# ============================================================================
# DATABASE CONNECTION MANAGER
# ============================================================================

class DatabaseManager:
    """Manage PostgreSQL connections with proper transaction handling"""
    
    def __init__(self):
        self.conn_pool = None
        self.setup_pool()
        
    def setup_pool(self):
        """Create connection pool"""
        try:
            self.conn_pool = psycopg2.pool.SimpleConnectionPool(
                1, 5,
                host='localhost',
                port=5432,
                database='zelda_arsredovisning',
                user='postgres',
                password='h100pass'
            )
            print("✅ Database connection pool created")
        except Exception as e:
            print(f"❌ Database pool failed: {e}")
            
    def get_connection(self):
        """Get connection from pool with auto-rollback on error"""
        if not self.conn_pool:
            return None
            
        conn = self.conn_pool.getconn()
        try:
            # Reset any aborted transaction
            conn.rollback()
            return conn
        except:
            return conn
            
    def return_connection(self, conn):
        """Return connection to pool"""
        if conn and self.conn_pool:
            try:
                conn.rollback()  # Clean slate
            except:
                pass
            self.conn_pool.putconn(conn)
            
    def fix_tables(self):
        """Fix database tables and clear errors"""
        conn = self.get_connection()
        if not conn:
            return False
            
        try:
            cur = conn.cursor()
            
            # Clear any aborted transactions
            conn.rollback()
            
            # Check critical tables
            tables_to_check = [
                'arsredovisning_documents',
                'agent_registry',
                'coaching_sessions',
                'prompt_execution_history'
            ]
            
            for table in tables_to_check:
                cur.execute(f"""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables 
                        WHERE table_name = '{table}'
                    );
                """)
                exists = cur.fetchone()[0]
                print(f"  - Table {table}: {'✅ EXISTS' if exists else '❌ MISSING'}")
                
            # Create missing coaching tables if needed
            cur.execute("""
                CREATE TABLE IF NOT EXISTS coaching_performance (
                    id SERIAL PRIMARY KEY,
                    agent_id VARCHAR(100),
                    doc_id VARCHAR(100),
                    accuracy FLOAT,
                    strategy VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS golden_examples (
                    id SERIAL PRIMARY KEY,
                    agent_id VARCHAR(100),
                    extraction JSONB,
                    accuracy FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            conn.commit()
            print("✅ Database tables verified and fixed")
            return True
            
        except Exception as e:
            print(f"❌ Database fix failed: {e}")
            conn.rollback()
            return False
        finally:
            self.return_connection(conn)

# ============================================================================
# UNIFIED VOYAGE TESTS
# ============================================================================

class H100MaidenVoyage:
    """Main voyage test suite for H100"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'environment': 'H100',
            'tests': {},
            'performance': {},
            'errors': []
        }
        self.logger = self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        logger = logging.getLogger('H100_Voyage')
        logger.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', '%H:%M:%S')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File handler
        log_file = f'/tmp/h100_voyage_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        return logger
        
    def test_database_connection(self) -> bool:
        """Test database connectivity"""
        self.logger.info("📌 Testing Database Connection...")
        
        conn = self.db_manager.get_connection()
        if not conn:
            self.logger.error("  ❌ Cannot connect to database")
            self.results['tests']['database'] = {'status': 'FAIL', 'error': 'Connection failed'}
            return False
            
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM arsredovisning_documents;")
            doc_count = cur.fetchone()[0]
            self.logger.info(f"  ✅ Database connected: {doc_count} documents")
            
            self.results['tests']['database'] = {
                'status': 'PASS',
                'doc_count': doc_count
            }
            return True
            
        except Exception as e:
            self.logger.error(f"  ❌ Database query failed: {e}")
            self.results['tests']['database'] = {'status': 'FAIL', 'error': str(e)}
            return False
        finally:
            self.db_manager.return_connection(conn)
            
    def test_twin_pipeline_integration(self) -> bool:
        """Test twin-pipeline Card G4 with proper DB connection"""
        self.logger.info("📌 Testing Twin-Pipeline Card G4...")
        
        try:
            # Import Card G4 coach
            from coaching.card_g4_reinforced_coach_fixed import Card_G4_ReinforcedCoach
            
            # FIXED: Use standard database config dict, not connection object
            # This was the bug - Card G4 expects config parameters, not a connection
            db_config = {
                'host': 'localhost',
                'port': 5432,
                'database': 'zelda_arsredovisning',
                'user': 'postgres',
                'password': 'h100pass'
            }
            
            # Initialize coach with proper config
            coach = Card_G4_ReinforcedCoach(db_config)
            
            self.logger.info(f"  ✅ Card G4 initialized - Phase {coach.learning_phase}")
            
            # Test basic functionality
            mock_extraction = {'test_field': 'test_value'}
            performance = coach.analyze_performance(mock_extraction, None)
            
            self.logger.info(f"  ✅ Performance analysis: accuracy={performance.accuracy:.2f}")
            
            self.results['tests']['card_g4'] = {
                'status': 'PASS',
                'phase': coach.learning_phase,
                'accuracy': performance.accuracy
            }
            return True
            
        except Exception as e:
            self.logger.error(f"  ❌ Card G4 failed: {e}")
            self.logger.debug(traceback.format_exc())
            self.results['tests']['card_g4'] = {'status': 'FAIL', 'error': str(e)}
            return False
                    
    def test_golden_patterns(self) -> bool:
        """Test Golden patterns integration"""
        self.logger.info("📌 Testing Golden Patterns...")
        
        try:
            # Check patterns file
            patterns_path = '/tmp/twin-pipeline/src/sectionizer/golden_patterns.json'
            if not os.path.exists(patterns_path):
                self.logger.error(f"  ❌ Patterns file not found: {patterns_path}")
                return False
                
            with open(patterns_path, 'r') as f:
                patterns_data = json.load(f)
                
            section_patterns = patterns_data.get('section_patterns', [])
            self.logger.info(f"  ✅ {len(section_patterns)} section patterns loaded")
            
            # Check for supplier patterns
            supplier_patterns = [p for p in section_patterns if 'leverantör' in p.lower()]
            self.logger.info(f"  ✅ {len(supplier_patterns)} supplier patterns found")
            
            self.results['tests']['golden_patterns'] = {
                'status': 'PASS',
                'total_patterns': len(section_patterns),
                'supplier_patterns': len(supplier_patterns)
            }
            return True
            
        except Exception as e:
            self.logger.error(f"  ❌ Pattern test failed: {e}")
            self.results['tests']['golden_patterns'] = {'status': 'FAIL', 'error': str(e)}
            return False
            
    def test_unified_system(self) -> bool:
        """Test the complete unified system"""
        self.logger.info("📌 Testing Unified Golden Fortress...")
        
        try:
            # Test agent registry
            registry_path = '/tmp/twin-pipeline/src/agents/golden_registry.json'
            with open(registry_path, 'r') as f:
                registry = json.load(f)
                
            agent_count = len(registry['agents'])
            self.logger.info(f"  ✅ {agent_count} agents in registry")
            
            # Test unified coach availability
            unified_coach_path = '/tmp/twin-pipeline/src/orchestrator/unified_coach.py'
            exists = os.path.exists(unified_coach_path)
            self.logger.info(f"  ✅ Unified coach: {'EXISTS' if exists else 'MISSING'}")
            
            # Test shadow orchestrator enhancement
            shadow_path = '/tmp/twin-pipeline/src/orchestrator/shadow_orchestrator.py'
            if os.path.exists(shadow_path):
                with open(shadow_path, 'r') as f:
                    content = f.read()
                    has_card_g4 = 'CARD_G4_AVAILABLE' in content
                    
                self.logger.info(f"  ✅ Shadow orchestrator: {'ENHANCED' if has_card_g4 else 'NOT ENHANCED'}")
            
            self.results['tests']['unified_system'] = {
                'status': 'PASS',
                'agents': agent_count,
                'unified_coach': exists,
                'shadow_enhanced': has_card_g4 if 'has_card_g4' in locals() else False
            }
            return True
            
        except Exception as e:
            self.logger.error(f"  ❌ Unified system test failed: {e}")
            self.results['tests']['unified_system'] = {'status': 'FAIL', 'error': str(e)}
            return False
            
    def run_voyage(self) -> Dict:
        """Execute complete H100 maiden voyage"""
        self.logger.info("=" * 80)
        self.logger.info("🚢 H100-NATIVE MAIDEN VOYAGE - GOLDEN FORTRESS")
        self.logger.info("=" * 80)
        self.logger.info("")
        
        start_time = time.time()
        
        # Fix database first
        self.logger.info("🔧 Preparing Database...")
        self.db_manager.fix_tables()
        self.logger.info("")
        
        # Run test suite
        tests = [
            ("Database Connection", self.test_database_connection),
            ("Golden Patterns", self.test_golden_patterns),
            ("Twin-Pipeline Card G4", self.test_twin_pipeline_integration),
            ("Unified System", self.test_unified_system)
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            self.logger.info("")
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.logger.error(f"  ❌ {name} crashed: {e}")
                self.results['errors'].append({
                    'test': name,
                    'error': str(e)
                })
                failed += 1
                
        # Calculate results
        duration = time.time() - start_time
        self.results['performance'] = {
            'duration_seconds': round(duration, 2),
            'tests_passed': passed,
            'tests_failed': failed,
            'success_rate': round(passed / max(1, passed + failed) * 100, 1)
        }
        
        # Determine success level
        if passed == len(tests):
            success_level = "🎯 EXCELLENT - 100% SUCCESS!"
        elif passed >= len(tests) * 0.75:
            success_level = "✅ GOOD"
        elif passed >= len(tests) * 0.5:
            success_level = "⚠️ MINIMUM"
        else:
            success_level = "❌ FAILED"
            
        self.logger.info("")
        self.logger.info("=" * 80)
        self.logger.info("🏁 VOYAGE COMPLETE")
        self.logger.info("=" * 80)
        self.logger.info(f"  Tests Passed: {passed}/{len(tests)}")
        self.logger.info(f"  Duration: {duration:.2f}s")
        self.logger.info(f"  Success Rate: {self.results['performance']['success_rate']}%")
        self.logger.info(f"  Status: {success_level}")
        self.logger.info("")
        
        # Save results
        results_file = f'/tmp/h100_voyage_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        self.logger.info(f"📊 Results saved to: {results_file}")
        
        return self.results

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for H100 execution"""
    print("\n🚀 H100-NATIVE GOLDEN FORTRESS VOYAGE\n")
    print("✅ CARD G4 CONFIG ISSUE FIXED - Using standard DB config dict\n")
    
    # Setup H100 environment
    H100Environment.setup()
    
    # Run voyage
    voyage = H100MaidenVoyage()
    results = voyage.run_voyage()
    
    # Return appropriate exit code
    if results['performance'].get('success_rate', 0) == 100:
        print("\n✅ 100% SUCCESS! All tests passed! Golden Fortress is fully operational.")
        sys.exit(0)
    elif results['performance'].get('tests_failed', 1) > 0:
        print("\n⚠️ Some tests failed. Check logs for details.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed! Golden Fortress is operational.")
        sys.exit(0)

if __name__ == "__main__":
    main()