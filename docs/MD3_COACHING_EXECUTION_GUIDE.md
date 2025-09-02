# 📚 MD3: COACHING EXECUTION GUIDE
## Step-by-Step Implementation of Reinforced Learning System

### 📋 **PREREQUISITES CHECK**
- ✅ Read MD1_REINFORCED_LEARNING_OVERVIEW.md
- ✅ Read MD2_CARD_G4_IMPLEMENTATION.md  
- ✅ Golden Orchestrator deployed on H100
- ✅ PostgreSQL with 16 agents loaded
- ✅ Gemini 2.5 Pro API key ready

## 🚀 **PHASE 0: INITIAL SETUP**

### **Step 1: Create Coaching Database Schema**

```bash
# SSH to H100
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10

# Create coaching tables
PGPASSWORD=h100pass psql -U postgres -h localhost -d zelda_arsredovisning << 'SQL'

-- Performance tracking table
CREATE TABLE IF NOT EXISTS coaching_performance (
    session_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    doc_id UUID NOT NULL,
    agent_id VARCHAR(50) NOT NULL,
    round_number INT NOT NULL,
    accuracy FLOAT,
    coverage FLOAT,
    prompt_version VARCHAR(50),
    prompt_text TEXT,
    extraction_json JSONB,
    errors JSONB,
    coaching_applied JSONB,
    improvement_delta FLOAT,
    best_round_number INT,
    reverted_to_round INT,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_agent_performance (agent_id, accuracy DESC),
    INDEX idx_doc_coaching (doc_id, agent_id, round_number)
);

-- Prompt evolution tracking
CREATE TABLE IF NOT EXISTS prompt_evolution (
    evolution_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    agent_id VARCHAR(50) NOT NULL,
    version VARCHAR(50) NOT NULL,
    prompt_text TEXT NOT NULL,
    examples JSONB,
    derived_from_version VARCHAR(50),
    avg_accuracy FLOAT,
    usage_count INT DEFAULT 0,
    success_rate FLOAT,
    phase INT,
    is_golden BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(agent_id, version)
);

-- Golden examples library
CREATE TABLE IF NOT EXISTS golden_examples (
    example_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    agent_id VARCHAR(50) NOT NULL,
    doc_type VARCHAR(50),
    doc_id UUID,
    input_pages INT[],
    expected_output JSONB,
    actual_output JSONB,
    accuracy_score FLOAT,
    validated_by VARCHAR(50) DEFAULT 'gemini-2.5-pro',
    validation_timestamp TIMESTAMP DEFAULT NOW(),
    usage_count INT DEFAULT 0,
    INDEX idx_golden_agent (agent_id, accuracy_score DESC)
);

-- Coaching session tracker
CREATE TABLE IF NOT EXISTS coaching_sessions (
    session_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    doc_id UUID NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    phase INT,
    total_agents INT,
    coached_agents INT,
    avg_improvement FLOAT,
    status VARCHAR(20) DEFAULT 'running'
);

SQL

echo "✅ Coaching database schema created"
```

### **Step 2: Deploy Card G4 Implementation**

```bash
# On local machine
cd /tmp/Golden_Orchestrator_Pipeline

# Create coaching directory structure
mkdir -p coaching
mkdir -p coaching/prompts
mkdir -p coaching/examples

# Create the Card G4 implementation file
cat > coaching/card_g4_reinforced_coach.py << 'PYTHON'
[Copy the implementation from MD2]
PYTHON

# Create integration module
cat > coaching/__init__.py << 'PYTHON'
from .card_g4_reinforced_coach import Card_G4_ReinforcedCoach

__all__ = ['Card_G4_ReinforcedCoach']
PYTHON

# Deploy to H100
scp -P 26983 -i ~/.ssh/BrfGraphRag -r coaching/ root@45.135.56.10:/tmp/Golden_Orchestrator_Pipeline/
```

### **Step 3: Configure Environment**

```bash
# On H100
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10

# Set environment variables
cat >> ~/.bashrc << 'ENV'
# Coaching Configuration
export COACHING_ENABLED=true
export COACHING_MODEL="gemini-2.5-pro"
export MAX_COACHING_ROUNDS_SECTIONIZER=2
export MAX_COACHING_ROUNDS_AGENTS=5
export LEARNING_PHASE_AUTO_DETECT=true
export GOLDEN_THRESHOLD=0.95
export COACHING_DB_URL="postgresql://postgres:h100pass@localhost:5432/zelda_arsredovisning"

# Gemini Configuration  
export GEMINI_API_KEY="AIzaSyD0y92BjcnvUgRlWsA1oPSIWV5QaJcCrNw"
export GEMINI_TEMPERATURE=0.1
export GEMINI_MAX_TOKENS=4096
ENV

source ~/.bashrc
```

## 📊 **PHASE 1: EXPLORATION (PDFs 1-50)**

### **Step 4: Initialize First PDF with Aggressive Coaching**

```bash
# Create coaching runner script
cat > /tmp/Golden_Orchestrator_Pipeline/run_coached_extraction.py << 'PYTHON'
#!/usr/bin/env python3

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, '/tmp/Golden_Orchestrator_Pipeline')

from orchestrator.golden_orchestrator import GoldenOrchestrator
from sectionizer.golden_sectionizer import GoldenSectionizer
from agents.agent_loader import AgentRegistry
from coaching.card_g4_reinforced_coach import Card_G4_ReinforcedCoach

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_phase1_coaching(doc_id: str, pdf_path: str):
    """
    Phase 1: Exploration with aggressive coaching (5 rounds max)
    """
    logging.info(f"Starting Phase 1 coaching for document {doc_id}")
    
    # Initialize components
    db_config = {
        'host': 'localhost',
        'database': 'zelda_arsredovisning', 
        'user': 'postgres',
        'password': 'h100pass'
    }
    
    coach = Card_G4_ReinforcedCoach(db_config)
    orchestrator = GoldenOrchestrator()
    sectionizer = GoldenSectionizer()
    registry = AgentRegistry()
    
    # Track coaching session
    session_results = {
        'doc_id': doc_id,
        'phase': 1,
        'started_at': datetime.now().isoformat(),
        'agents': {}
    }
    
    # 1. Run sectionizer with coaching
    logging.info("Running sectionizer...")
    sections = sectionizer.extract_sections(pdf_path)
    
    # Coach sectionizer if needed (max 2 rounds)
    for round in range(2):
        section_performance = coach.analyze_performance(
            {'sections': sections},
            ground_truth=None  # Self-evaluation
        )
        
        if section_performance.coverage < 0.80:
            logging.info(f"Sectionizer coaching round {round+1}")
            sections = coach.coach_extraction(
                doc_id=doc_id,
                agent_id='sectionizer',
                current_extraction={'sections': sections}
            ).get('sections', sections)
        else:
            break
    
    # 2. Map sections to agents
    agent_assignments = orchestrator.map_sections_to_agents(sections)
    
    # 3. Run each agent with aggressive coaching
    for agent_id, assignment in agent_assignments.items():
        logging.info(f"Processing agent: {agent_id}")
        
        # Get agent prompt
        agent = registry.get_agent(agent_id)
        
        # Initial extraction
        extraction = orchestrator.run_agent(
            agent_id=agent_id,
            pages=assignment['pages'],
            prompt=agent['prompt']
        )
        
        # Aggressive coaching (up to 5 rounds)
        best_extraction = extraction
        best_accuracy = 0
        
        for round in range(5):
            performance = coach.analyze_performance(extraction, None)
            
            if performance.accuracy >= 0.95:
                logging.info(f"Agent {agent_id} reached golden accuracy!")
                break
                
            logging.info(f"Coaching {agent_id} round {round+1}")
            coached = coach.coach_extraction(
                doc_id=doc_id,
                agent_id=agent_id,
                current_extraction=extraction
            )
            
            new_performance = coach.analyze_performance(coached, None)
            
            if new_performance.accuracy > best_accuracy:
                best_extraction = coached
                best_accuracy = new_performance.accuracy
            
            extraction = coached
            
            # Stop if no improvement for 2 rounds
            if round > 1 and new_performance.accuracy <= best_accuracy:
                logging.info(f"No improvement, stopping at round {round+1}")
                break
        
        session_results['agents'][agent_id] = {
            'rounds': round + 1,
            'final_accuracy': best_accuracy,
            'extraction': best_extraction
        }
    
    # 4. Save results
    session_results['completed_at'] = datetime.now().isoformat()
    
    output_path = f"/tmp/coaching_results/{doc_id}_phase1.json"
    Path(output_path).parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(session_results, f, indent=2)
    
    logging.info(f"Phase 1 coaching complete. Results saved to {output_path}")
    return session_results

if __name__ == "__main__":
    # Test with first document
    test_doc_id = "83659_årsredovisning_göteborg_brf_erik_dahlbergsgatan_12"
    test_pdf_path = "/path/to/pdf"
    
    results = run_phase1_coaching(test_doc_id, test_pdf_path)
    print(json.dumps(results, indent=2))
PYTHON

chmod +x run_coached_extraction.py
```

### **Step 5: Batch Process First 50 PDFs**

```python
# Create batch processor for Phase 1
cat > /tmp/Golden_Orchestrator_Pipeline/batch_phase1.py << 'PYTHON'
#!/usr/bin/env python3

import os
import sys
import json
import time
import psycopg2
from pathlib import Path

sys.path.insert(0, '/tmp/Golden_Orchestrator_Pipeline')
from run_coached_extraction import run_phase1_coaching

def get_first_50_pdfs():
    """Get first 50 PDFs from database"""
    conn = psycopg2.connect(
        host='localhost',
        database='zelda_arsredovisning',
        user='postgres', 
        password='h100pass'
    )
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT doc_id, file_path 
            FROM arsredovisning_documents
            WHERE status = 'ready'
            LIMIT 50
        """)
        return cur.fetchall()

def batch_process_phase1():
    """Process first 50 PDFs with aggressive coaching"""
    pdfs = get_first_50_pdfs()
    
    results = []
    for i, (doc_id, pdf_path) in enumerate(pdfs, 1):
        print(f"\n{'='*60}")
        print(f"Processing PDF {i}/50: {doc_id}")
        print(f"{'='*60}")
        
        try:
            result = run_phase1_coaching(doc_id, pdf_path)
            results.append(result)
            
            # Show progress
            avg_accuracy = sum(
                agent['final_accuracy'] 
                for agent in result['agents'].values()
            ) / len(result['agents'])
            
            print(f"✅ Completed with avg accuracy: {avg_accuracy:.2%}")
            
        except Exception as e:
            print(f"❌ Error processing {doc_id}: {e}")
            results.append({'doc_id': doc_id, 'error': str(e)})
        
        # Rate limiting
        time.sleep(2)
    
    # Save batch results
    with open('/tmp/phase1_batch_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"PHASE 1 COMPLETE")
    print(f"Processed: {len(results)} PDFs")
    print(f"Results saved to /tmp/phase1_batch_results.json")

if __name__ == "__main__":
    batch_process_phase1()
PYTHON

chmod +x batch_phase1.py
```

## 🔄 **PHASE 2: OPTIMIZATION (PDFs 51-150)**

### **Step 6: Transition to Selective Coaching**

```python
# Phase 2 runner with selective coaching
cat > /tmp/Golden_Orchestrator_Pipeline/run_phase2_coaching.py << 'PYTHON'
def run_phase2_coaching(doc_id: str, pdf_path: str):
    """
    Phase 2: Optimization with selective coaching (3 rounds max)
    Focus on underperforming agents only
    """
    # Load performance thresholds from Phase 1
    with open('/tmp/phase1_metrics.json') as f:
        phase1_metrics = json.load(f)
    
    avg_accuracies = phase1_metrics['avg_accuracies_by_agent']
    
    # Only coach agents below their Phase 1 average
    coaching_targets = {}
    for agent_id, assignment in agent_assignments.items():
        extraction = run_agent(agent_id, assignment)
        performance = analyze_performance(extraction)
        
        # Selective coaching based on Phase 1 baseline
        if performance.accuracy < avg_accuracies.get(agent_id, 0.75):
            coaching_targets[agent_id] = extraction
    
    # Coach only underperformers (max 3 rounds)
    for agent_id, extraction in coaching_targets.items():
        for round in range(3):
            coached = coach.coach_extraction(
                doc_id=doc_id,
                agent_id=agent_id,
                current_extraction=extraction
            )
            
            if coached['accuracy'] >= avg_accuracies[agent_id] + 0.05:
                break  # Good enough improvement
PYTHON
```

## 📈 **MONITORING & VALIDATION**

### **Step 7: Create Monitoring Dashboard**

```python
cat > /tmp/Golden_Orchestrator_Pipeline/coaching_monitor.py << 'PYTHON'
#!/usr/bin/env python3

import psycopg2
import json
from datetime import datetime, timedelta
from tabulate import tabulate

def get_coaching_metrics():
    """Real-time coaching metrics dashboard"""
    conn = psycopg2.connect(
        host='localhost',
        database='zelda_arsredovisning',
        user='postgres',
        password='h100pass'
    )
    
    metrics = {}
    
    with conn.cursor() as cur:
        # Overall progress
        cur.execute("""
            SELECT 
                COUNT(DISTINCT doc_id) as pdfs_processed,
                AVG(accuracy) as avg_accuracy,
                MAX(accuracy) as best_accuracy,
                AVG(improvement_delta) as avg_improvement
            FROM coaching_performance
        """)
        metrics['overall'] = cur.fetchone()
        
        # Agent performance
        cur.execute("""
            SELECT 
                agent_id,
                AVG(accuracy) as avg_acc,
                MAX(accuracy) as max_acc,
                COUNT(*) as sessions,
                AVG(improvement_delta) as avg_imp
            FROM coaching_performance
            GROUP BY agent_id
            ORDER BY avg_acc DESC
        """)
        metrics['agents'] = cur.fetchall()
        
        # Learning phase
        cur.execute("""
            SELECT COUNT(DISTINCT doc_id) FROM coaching_performance
        """)
        pdf_count = cur.fetchone()[0]
        
        if pdf_count <= 50:
            phase = "Phase 1: Exploration"
        elif pdf_count <= 150:
            phase = "Phase 2: Optimization"
        elif pdf_count <= 200:
            phase = "Phase 3: Convergence"
        else:
            phase = "Phase 4: Golden State"
        
        metrics['phase'] = phase
        metrics['pdf_count'] = pdf_count
    
    return metrics

def display_dashboard():
    """Display coaching metrics dashboard"""
    metrics = get_coaching_metrics()
    
    print("\n" + "="*80)
    print("REINFORCED COACHING DASHBOARD")
    print("="*80)
    
    print(f"\n📊 LEARNING PHASE: {metrics['phase']}")
    print(f"📚 PDFs Processed: {metrics['pdf_count']}/200")
    
    print(f"\n🎯 OVERALL METRICS:")
    print(f"  Average Accuracy: {metrics['overall'][1]:.2%}")
    print(f"  Best Accuracy: {metrics['overall'][2]:.2%}") 
    print(f"  Avg Improvement: {metrics['overall'][3]:.2%}")
    
    print(f"\n📈 AGENT PERFORMANCE:")
    headers = ["Agent", "Avg Acc", "Max Acc", "Sessions", "Avg Improvement"]
    table_data = [
        [row[0][:20], f"{row[1]:.2%}", f"{row[2]:.2%}", row[3], f"{row[4]:.2%}"]
        for row in metrics['agents']
    ]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Progress bar
    progress = min(metrics['pdf_count'] / 200, 1.0)
    bar_length = 50
    filled = int(bar_length * progress)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    print(f"\n📊 Progress to Golden State:")
    print(f"[{bar}] {progress:.1%}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    display_dashboard()
PYTHON

chmod +x coaching_monitor.py
```

### **Step 8: Validate Coaching Effectiveness**

```python
cat > /tmp/Golden_Orchestrator_Pipeline/validate_coaching.py << 'PYTHON'
#!/usr/bin/env python3

def validate_coaching_effectiveness():
    """
    Validate that coaching is actually improving performance
    """
    conn = psycopg2.connect(...)
    
    with conn.cursor() as cur:
        # Check improvement rates
        cur.execute("""
            SELECT 
                agent_id,
                COUNT(CASE WHEN improvement_delta > 0 THEN 1 END) as improvements,
                COUNT(CASE WHEN improvement_delta < 0 THEN 1 END) as regressions,
                COUNT(*) as total
            FROM coaching_performance
            GROUP BY agent_id
        """)
        
        results = cur.fetchall()
        
        for agent_id, improvements, regressions, total in results:
            success_rate = improvements / total if total > 0 else 0
            
            if success_rate < 0.5:
                print(f"⚠️ WARNING: {agent_id} coaching success rate only {success_rate:.1%}")
                print(f"   Consider adjusting coaching strategy")
            else:
                print(f"✅ {agent_id}: {success_rate:.1%} improvement rate")
    
    # Check for golden examples
    cur.execute("""
        SELECT agent_id, COUNT(*) as golden_count
        FROM golden_examples
        GROUP BY agent_id
    """)
    
    golden_counts = cur.fetchall()
    for agent_id, count in golden_counts:
        print(f"🏆 {agent_id}: {count} golden examples collected")

if __name__ == "__main__":
    validate_coaching_effectiveness()
PYTHON
```

## 🚀 **EXECUTION COMMANDS**

### **Complete Execution Sequence**

```bash
# 1. SSH to H100
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10

# 2. Navigate to project
cd /tmp/Golden_Orchestrator_Pipeline

# 3. Run Phase 1 (PDFs 1-50)
python3 batch_phase1.py

# 4. Monitor progress
watch -n 10 python3 coaching_monitor.py

# 5. Validate effectiveness
python3 validate_coaching.py

# 6. When Phase 1 complete, run Phase 2 (PDFs 51-150)
python3 batch_phase2.py

# 7. Continue monitoring
python3 coaching_monitor.py

# 8. After 200 PDFs, extract golden prompts
python3 extract_golden_prompts.py > golden_prompts.json
```

## ✅ **QUALITY GATES**

### **Phase Transition Criteria**

**Phase 1 → Phase 2:**
- ✅ 50 PDFs processed
- ✅ Average accuracy ≥ 75%
- ✅ All agents have baseline metrics
- ✅ At least 10 golden examples collected

**Phase 2 → Phase 3:**
- ✅ 150 PDFs processed
- ✅ Average accuracy ≥ 85%
- ✅ Coaching success rate ≥ 60%
- ✅ 30+ golden examples per agent

**Phase 3 → Phase 4:**
- ✅ 200 PDFs processed
- ✅ Average accuracy ≥ 95%
- ✅ Prompt stability (< 5% change)
- ✅ Gemini validation passed

## 🔍 **TROUBLESHOOTING**

### **Common Issues and Solutions**

**1. Coaching Not Improving Performance**
```python
# Check coaching history
SELECT agent_id, round_number, accuracy, improvement_delta
FROM coaching_performance
WHERE agent_id = 'problematic_agent'
ORDER BY created_at DESC
LIMIT 10;

# Solution: Adjust strategy in Card G4
if improvement_delta < 0 for 3 consecutive rounds:
    strategy = "explore"  # Try different approach
```

**2. Gemini API Rate Limits**
```python
# Add exponential backoff
import time
for attempt in range(5):
    try:
        response = gemini.generate_content(prompt)
        break
    except RateLimitError:
        time.sleep(2 ** attempt)
```

**3. Memory Issues with Large Batches**
```python
# Process in smaller chunks
for chunk in chunks(pdfs, size=10):
    process_chunk(chunk)
    gc.collect()  # Force garbage collection
```

## 📊 **SUCCESS METRICS**

Track these metrics to ensure system is learning effectively:

1. **Accuracy Trend**: Should increase monotonically
2. **Coaching Rounds**: Should decrease over time
3. **Golden Examples**: Should accumulate steadily
4. **Prompt Stability**: Should converge by Phase 3
5. **Cross-Agent Consistency**: Related agents should align

---

**Next: Read MD4_PRODUCTION_GOLDEN_STATE.md for final deployment**