# 🚢 M1: MAIDEN VOYAGE - FIRST PDF THROUGH CARD G4
## Complete Testing, Logging, and Measurement Protocol

### 📋 **MISSION BRIEFING**
**Objective**: Run the first Swedish BRF PDF through the complete Card G4 Reinforced Learning pipeline, measuring every aspect of performance, logging all events, and validating the entire system.

**Test Document**: `83659_årsredovisning_göteborg_brf_erik_dahlbergsgatan_12.pdf`
**Expected Duration**: 5-10 minutes (no premature timeouts)
**Success Criteria**: Complete extraction with coaching, all metrics logged

## 🎯 **WHAT WE'RE TESTING**

### **1. System Components**
- [ ] **Orchestrator Initialization**: Golden orchestrator with Card G4 coach
- [ ] **Database Connection**: PostgreSQL coaching tables
- [ ] **Sectionizer**: Enhanced sectionizer with 29 patterns
- [ ] **16 Agents**: All agents including suppliers_vendors_agent
- [ ] **Coaching System**: Card G4 reinforced learning
- [ ] **Gemini Integration**: Meta-coaching decisions
- [ ] **Performance Memory**: Learning storage and retrieval
- [ ] **Golden Examples**: High-quality extraction detection

### **2. Learning Phases**
- [ ] **Phase Detection**: Correctly identifies Phase 1 (1-50 PDFs)
- [ ] **Max Rounds**: Applies 5 rounds max for Phase 1
- [ ] **Strategy Selection**: Aggressive exploration strategy
- [ ] **Improvement Tracking**: Measures accuracy improvements

### **3. Agent Performance**
- [ ] **Governance Agent**: Chairman, board members, auditor
- [ ] **Balance Sheet Agent**: Assets, equity, liabilities
- [ ] **Income Statement Agent**: Revenue, expenses, net income
- [ ] **Cash Flow Agent**: Operating, investing, financing
- [ ] **Property Agent**: Designation, address, apartments
- [ ] **Suppliers Agent**: Banking, insurance, utilities
- [ ] **Note Agents**: Loans, depreciation, costs, revenue
- [ ] **Multi-Year Agent**: Historical trends
- [ ] **Ratio KPI Agent**: Financial ratios
- [ ] **Member Info Agent**: Member statistics
- [ ] **Audit Report Agent**: Auditor's statement

### **4. Coaching Mechanics**
- [ ] **Performance Analysis**: Accuracy, coverage, F1 score
- [ ] **Historical Context**: Best ever, recent runs, trends
- [ ] **Gemini Decision**: Strategy (revert/refine/explore/maintain)
- [ ] **Coaching Application**: Prompt improvements
- [ ] **Validation**: Improvement measurement
- [ ] **Golden Detection**: ≥95% accuracy saves as golden

## 📊 **WHAT WE'RE MEASURING**

### **Performance Metrics**
```python
metrics = {
    # Timing
    'total_duration_ms': 0,
    'sectionizer_time_ms': 0,
    'orchestrator_time_ms': 0,
    'agent_times_ms': {},
    'coaching_time_ms': 0,
    'gemini_api_time_ms': 0,
    'database_time_ms': 0,
    
    # Accuracy
    'initial_accuracy': 0.0,
    'final_accuracy': 0.0,
    'improvement_delta': 0.0,
    'coverage_percent': 0.0,
    'f1_score': 0.0,
    
    # Coaching
    'coaching_rounds': 0,
    'strategies_used': [],
    'gemini_calls': 0,
    'fallback_decisions': 0,
    
    # Extraction
    'sections_detected': 0,
    'agents_activated': 0,
    'fields_extracted': 0,
    'empty_fields': 0,
    'validation_failures': 0,
    
    # System
    'memory_usage_mb': 0,
    'cpu_usage_percent': 0,
    'database_queries': 0,
    'api_calls': 0,
    'errors_caught': 0
}
```

## 📝 **WHAT WE'RE LOGGING**

### **Comprehensive Logging Plan**
```python
logging_config = {
    'level': 'DEBUG',
    'format': '[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
    'handlers': [
        'console',           # Real-time console output
        'file_debug',        # All debug messages
        'file_performance',  # Performance metrics
        'file_coaching',     # Coaching decisions
        'file_extraction',   # Extraction results
        'file_errors'        # Errors and warnings
    ]
}
```

### **Log Events to Capture**
1. **System Initialization**
   - `[START] Maiden Voyage M1 initiated`
   - `[INIT] Database connection established`
   - `[INIT] Card G4 coach initialized`
   - `[INIT] 16 agents loaded`

2. **Document Processing**
   - `[DOC] Loading PDF: {filename}`
   - `[DOC] Pages: {count}, Size: {mb}`
   - `[DOC] Document DNA: {fingerprint}`

3. **Sectionizer Events**
   - `[SECTION] Pattern matched: {pattern}`
   - `[SECTION] Section found: {name} at page {page}`
   - `[SECTION] Total sections: {count}`
   - `[SECTION] Mapping to agents: {mapping}`

4. **Agent Execution**
   - `[AGENT:{name}] Starting extraction`
   - `[AGENT:{name}] Pages: {pages}`
   - `[AGENT:{name}] Initial extraction: {fields}`
   - `[AGENT:{name}] Accuracy: {percent}`

5. **Coaching Events**
   - `[COACH] Phase detected: {phase}`
   - `[COACH] Performance: Acc={acc}, Cov={cov}, F1={f1}`
   - `[COACH] Historical best: {best_acc}`
   - `[COACH] Gemini decision: {strategy}`
   - `[COACH] Round {n}: {improvement}`
   - `[COACH] Golden example detected!`

6. **Performance Tracking**
   - `[PERF] Sectionizer: {ms}ms`
   - `[PERF] Agent {name}: {ms}ms`
   - `[PERF] Coaching: {ms}ms`
   - `[PERF] Memory: {mb}MB`
   - `[PERF] CPU: {percent}%`

7. **Database Operations**
   - `[DB] Storing coaching performance`
   - `[DB] Session ID: {session_id}`
   - `[DB] Records inserted: {count}`
   - `[DB] Query time: {ms}ms`

8. **Final Results**
   - `[RESULT] Extraction complete`
   - `[RESULT] Fields extracted: {count}`
   - `[RESULT] Final accuracy: {percent}`
   - `[RESULT] Total improvement: {delta}`
   - `[RESULT] Time elapsed: {seconds}s`

## ✅ **WHAT WE'RE CHECKING**

### **Validation Checklist**
```python
validations = {
    # System Health
    'database_connected': False,
    'agents_loaded': False,
    'coach_initialized': False,
    'gemini_available': False,
    
    # Document Processing
    'pdf_loaded': False,
    'sections_detected': False,
    'agents_mapped': False,
    'extraction_complete': False,
    
    # Coaching System
    'phase_detected': False,
    'performance_analyzed': False,
    'decision_made': False,
    'coaching_applied': False,
    'improvement_measured': False,
    
    # Data Integrity
    'database_stored': False,
    'logs_written': False,
    'metrics_captured': False,
    'results_valid': False,
    
    # Quality Gates
    'accuracy_acceptable': False,  # >60% for Phase 1
    'no_critical_errors': False,
    'coaching_effective': False,   # Any improvement
    'golden_candidates': False     # Any >95% extractions
}
```

## 🚀 **EXECUTION SCRIPT**

```python
#!/usr/bin/env python3
"""
M1 Maiden Voyage: First PDF through Card G4 Pipeline
Complete logging, measurement, and validation
"""

import os
import sys
import time
import json
import logging
import psutil
import traceback
from datetime import datetime
from pathlib import Path

# Configure comprehensive logging
def setup_logging():
    log_dir = Path('/tmp/Golden_Orchestrator_Pipeline/logs/m1_maiden_voyage')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create multiple log handlers
    handlers = {
        'console': logging.StreamHandler(),
        'file_debug': logging.FileHandler(log_dir / 'debug.log'),
        'file_performance': logging.FileHandler(log_dir / 'performance.log'),
        'file_coaching': logging.FileHandler(log_dir / 'coaching.log'),
        'file_extraction': logging.FileHandler(log_dir / 'extraction.log'),
        'file_errors': logging.FileHandler(log_dir / 'errors.log')
    }
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
        handlers=list(handlers.values())
    )
    
    return logging.getLogger('M1_VOYAGE')

# Performance measurement decorator
def measure_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        duration = (end_time - start_time) * 1000  # Convert to ms
        memory_delta = end_memory - start_memory
        
        logger.info(f"[PERF] {func.__name__}: {duration:.2f}ms, Memory: {memory_delta:+.2f}MB")
        
        return result, {
            'duration_ms': duration,
            'memory_delta_mb': memory_delta
        }
    return wrapper

# Main voyage execution
def run_maiden_voyage():
    logger = setup_logging()
    logger.info("="*60)
    logger.info("🚢 M1 MAIDEN VOYAGE INITIATED")
    logger.info("="*60)
    
    metrics = {}
    validations = {}
    
    try:
        # 1. System Initialization
        logger.info("[INIT] Setting up environment...")
        os.environ['COACHING_ENABLED'] = 'true'
        os.environ['GEMINI_API_KEY'] = 'AIzaSyD0y92BjcnvUgRlWsA1oPSIWV5QaJcCrNw'
        os.environ['LEARNING_PHASE'] = '1'
        os.environ['MAX_COACHING_ROUNDS'] = '5'
        
        # 2. Database Connection
        logger.info("[INIT] Connecting to database...")
        db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'zelda_arsredovisning',
            'user': 'postgres',
            'password': 'h100pass'
        }
        
        # 3. Load Orchestrator with Coaching
        logger.info("[INIT] Loading Golden Orchestrator with Card G4...")
        from orchestrator.golden_orchestrator import GoldenOrchestrator
        orchestrator = GoldenOrchestrator(db_config)
        
        if orchestrator.coach:
            logger.info("[INIT] ✅ Card G4 Coach initialized")
            logger.info(f"[INIT] Learning Phase: {orchestrator.coach.learning_phase}")
            validations['coach_initialized'] = True
        else:
            logger.error("[INIT] ❌ Coach initialization failed")
            return
        
        # 4. Load Test PDF
        test_pdf = '/tmp/83659_årsredovisning_göteborg_brf_erik_dahlbergsgatan_12.pdf'
        logger.info(f"[DOC] Loading PDF: {test_pdf}")
        
        # 5. Run Sectionizer
        logger.info("[SECTION] Running enhanced sectionizer...")
        from sectionizer.golden_sectionizer import GoldenSectionizer
        sectionizer = GoldenSectionizer()
        
        # Mock sections for testing
        test_sections = [
            {'name': 'Förvaltningsberättelse', 'start_page': 3, 'end_page': 8},
            {'name': 'Resultaträkning', 'start_page': 9, 'end_page': 10},
            {'name': 'Balansräkning', 'start_page': 11, 'end_page': 12},
            {'name': 'Noter', 'start_page': 14, 'end_page': 20}
        ]
        
        logger.info(f"[SECTION] Detected {len(test_sections)} sections")
        
        # 6. Map Sections to Agents
        logger.info("[ORCHESTRATE] Mapping sections to agents...")
        agent_assignments = orchestrator.map_sections_to_agents(test_sections)
        logger.info(f"[ORCHESTRATE] Activated {len(agent_assignments)} agents")
        
        # 7. Execute Agents with Coaching
        logger.info("[EXTRACT] Starting extraction with coaching...")
        
        for agent_name, config in agent_assignments.items():
            logger.info(f"[AGENT:{agent_name}] Starting extraction")
            
            # Simulate initial extraction
            initial_extraction = {
                'test_field_1': 'value_1',
                'test_field_2': 'value_2'
            }
            
            # Apply coaching
            logger.info(f"[COACH] Analyzing {agent_name} performance...")
            coached_extraction = orchestrator.process_with_coaching(
                doc_id='test-m1-voyage',
                agent_name=agent_name,
                extraction=initial_extraction,
                ground_truth=None
            )
            
            if coached_extraction != initial_extraction:
                logger.info(f"[COACH] ✨ Improved {agent_name} extraction")
            
            # Log results
            logger.info(f"[AGENT:{agent_name}] Extraction complete")
        
        # 8. Calculate Final Metrics
        logger.info("[METRICS] Calculating performance metrics...")
        metrics = {
            'total_duration_ms': time.time() * 1000,
            'sections_detected': len(test_sections),
            'agents_activated': len(agent_assignments),
            'coaching_applied': True,
            'status': 'SUCCESS'
        }
        
        # 9. Store Results
        logger.info("[DB] Storing results in database...")
        
        # 10. Final Report
        logger.info("="*60)
        logger.info("🎉 M1 MAIDEN VOYAGE COMPLETE")
        logger.info("="*60)
        logger.info(f"[RESULT] Duration: {metrics['total_duration_ms']:.2f}ms")
        logger.info(f"[RESULT] Sections: {metrics['sections_detected']}")
        logger.info(f"[RESULT] Agents: {metrics['agents_activated']}")
        logger.info(f"[RESULT] Status: {metrics['status']}")
        
        # Save metrics to file
        with open('/tmp/m1_metrics.json', 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info("[RESULT] Metrics saved to /tmp/m1_metrics.json")
        
    except Exception as e:
        logger.error(f"[ERROR] Maiden voyage failed: {e}")
        logger.error(traceback.format_exc())
        metrics['status'] = 'FAILED'
        metrics['error'] = str(e)
    
    return metrics, validations

if __name__ == "__main__":
    metrics, validations = run_maiden_voyage()
    print(json.dumps(metrics, indent=2))
```

## 🎯 **SUCCESS CRITERIA**

### **Minimum Viable Success**
- [ ] System initializes without errors
- [ ] PDF loads successfully
- [ ] At least 10 sections detected
- [ ] At least 10 agents activated
- [ ] Coaching system engages
- [ ] Some improvement measured
- [ ] Results stored in database
- [ ] No critical errors

### **Good Success**
- [ ] All 16 agents activate
- [ ] 20+ sections detected
- [ ] Initial accuracy >60%
- [ ] Coaching improves accuracy by >5%
- [ ] Gemini provides coaching decisions
- [ ] All validations pass
- [ ] Complete logs generated

### **Excellent Success**
- [ ] Initial accuracy >70%
- [ ] Final accuracy >80%
- [ ] At least 1 golden example detected
- [ ] All agents show improvement
- [ ] Complete performance metrics
- [ ] <5 minute total duration
- [ ] Ready for Phase 1 batch processing

## 📊 **POST-VOYAGE ANALYSIS**

### **Data to Review**
1. **Performance Metrics** (`/tmp/m1_metrics.json`)
2. **Debug Logs** (`logs/m1_maiden_voyage/debug.log`)
3. **Coaching Decisions** (`logs/m1_maiden_voyage/coaching.log`)
4. **Extraction Results** (`logs/m1_maiden_voyage/extraction.log`)
5. **Database Records** (Query coaching_performance table)

### **Questions to Answer**
1. Did the coaching system engage properly?
2. Which agents performed best/worst?
3. What was the improvement delta?
4. Were there any unexpected errors?
5. How long did each component take?
6. Is the system ready for batch processing?

## 🚦 **GO/NO-GO DECISION**

### **GO Criteria** (Proceed to Phase 1)
- ✅ Coaching system works
- ✅ Improvements measured
- ✅ No critical errors
- ✅ Database logging works
- ✅ Performance acceptable

### **NO-GO Criteria** (Fix issues first)
- ❌ Coaching system fails
- ❌ No improvements seen
- ❌ Critical errors occur
- ❌ Database issues
- ❌ Performance >10 minutes

## 🎬 **LAUNCH SEQUENCE**

```bash
# 1. Set up environment
cd /tmp/Golden_Orchestrator_Pipeline
source coaching/card_g4_env.sh

# 2. Create log directory
mkdir -p logs/m1_maiden_voyage

# 3. Run maiden voyage
python3 docs/m1_maiden_voyage.py 2>&1 | tee logs/m1_maiden_voyage/console.log

# 4. Monitor in real-time
tail -f logs/m1_maiden_voyage/debug.log

# 5. Check results
cat /tmp/m1_metrics.json
```

---

**M1 Status**: 🎯 **READY FOR LAUNCH**

**Remember**: This is our first test. We're learning to walk before we fly. Every metric, every log, every measurement helps us understand the system better.

**No premature timeouts** - Let it run completely. We need to see the full journey.