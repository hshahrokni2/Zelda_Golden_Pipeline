# 📜 MD4: PRODUCTION OPERATIONS - DAILY WORKFLOWS
## Running, Monitoring, and Maintaining the Golden Fortress

**Prerequisites**: You've read MD1, MD2, and MD3  
**Purpose**: Daily operations, monitoring, troubleshooting, and optimization

## 🎯 PRODUCTION OVERVIEW

### System Status Dashboard
```bash
# Quick health check
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10 << 'EOF'
echo "=== GOLDEN FORTRESS STATUS ==="
echo -n "Database Documents: "
psql -U postgres -d zelda_arsredovisning -t -c "SELECT COUNT(*) FROM arsredovisning_documents;"
echo -n "Coaching Sessions: "
psql -U postgres -d zelda_arsredovisning -t -c "SELECT COUNT(*) FROM coaching_sessions;"
echo -n "Golden Examples: "
psql -U postgres -d zelda_arsredovisning -t -c "SELECT COUNT(*) FROM golden_examples WHERE accuracy >= 0.95;"
echo -n "Current Phase: "
psql -U postgres -d zelda_arsredovisning -t -c "SELECT MAX(phase) FROM coaching_performance;"
echo -n "Average Accuracy: "
psql -U postgres -d zelda_arsredovisning -t -c "SELECT ROUND(AVG(accuracy)*100, 2) || '%' FROM coaching_performance WHERE created_at > NOW() - INTERVAL '24 hours';"
EOF
```

### Key Metrics
- **Documents Processed**: Target 200 for full learning
- **Current Learning Phase**: 1-4 (see Card G4 phases)
- **Average Accuracy**: Should improve 15% per phase
- **Golden Examples**: Collection starts at 95%+ accuracy
- **System Load**: GPU memory, CPU usage, DB connections

## 🚀 DAILY OPERATIONS

### Morning Startup Routine
```bash
# 1. SSH to H100
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10

# 2. Source environment
source /tmp/golden_fortress_env.sh

# 3. Check system health
nvidia-smi  # GPU status
df -h       # Disk space
free -h     # Memory

# 4. Verify database
psql -U postgres -d zelda_arsredovisning -c "SELECT 1;"

# 5. Run verification voyage
cd /tmp/Golden_Orchestrator_Pipeline
python3 h100_native_maiden_voyage.py
```

### Processing New Documents
```bash
# Single document by ID
RUN_ID="RUN_$(date +%s)"
python scripts/run_prod.py \
  --run-id "$RUN_ID" \
  --doc-id "SPECIFIC_UUID" \
  --enable-coaching

# Batch processing (next 10 documents)
python scripts/run_prod.py \
  --run-id "$RUN_ID" \
  --limit 10 \
  --enable-coaching \
  --max-rounds 3

# Phase-specific batch
python coaching/run_phase.py \
  --phase 1 \
  --start-doc 51 \
  --end-doc 100
```

### Monitoring Coaching Progress
```sql
-- Real-time coaching dashboard
psql -U postgres -d zelda_arsredovisning << 'SQL'
-- Current session progress
SELECT 
    run_id,
    agent_id,
    COUNT(*) as rounds,
    AVG(accuracy) as avg_accuracy,
    MAX(accuracy) as best_accuracy,
    STRING_AGG(strategy, ' → ' ORDER BY round) as strategy_sequence
FROM (
    SELECT * FROM coaching_sessions 
    WHERE created_at > NOW() - INTERVAL '1 hour'
    ORDER BY created_at DESC
) recent
GROUP BY run_id, agent_id
ORDER BY run_id DESC, avg_accuracy DESC;

-- Agent performance trends
SELECT 
    agent_id,
    DATE(created_at) as date,
    COUNT(*) as docs_processed,
    AVG(accuracy) as daily_avg,
    MAX(accuracy) as daily_best
FROM coaching_performance
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY agent_id, DATE(created_at)
ORDER BY date DESC, daily_avg DESC;
SQL
```

### Receipt Validation
```bash
# Check recent model calls
tail -n 100 artifacts/calls_log.ndjson | \
  jq 'select(.run_id | startswith("RUN_")) | 
      {run_id, model, http_status, latency_ms, accuracy}'

# Verify twin agent consensus
tail -n 100 artifacts/calls_log.ndjson | \
  jq 'select(.model == "qwen2.5vl:7b" or .model == "gemini-2.5-pro") | 
      {model, success: .http_status == 200}' | \
  jq -s 'group_by(.model) | 
         map({model: .[0].model, success_rate: (map(select(.success)) | length) / length})'

# Check for errors
tail -n 1000 artifacts/calls_log.ndjson | \
  jq 'select(.http_status != 200) | 
      {timestamp, model, error: .error_message, doc_id}'
```

## 📊 PERFORMANCE OPTIMIZATION

### GPU Memory Management
```python
# Monitor GPU usage during extraction
import subprocess
import json

def monitor_gpu():
    result = subprocess.run(
        ['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits'],
        capture_output=True, text=True
    )
    used, total = map(int, result.stdout.strip().split(', '))
    usage_percent = (used / total) * 100
    
    if usage_percent > 90:
        print(f"⚠️ GPU memory critical: {usage_percent:.1f}%")
        # Trigger cleanup
        cleanup_gpu_memory()
    elif usage_percent > 75:
        print(f"📊 GPU memory high: {usage_percent:.1f}%")
    else:
        print(f"✅ GPU memory OK: {usage_percent:.1f}%")
```

### Database Query Optimization
```sql
-- Add missing indexes if queries are slow
CREATE INDEX IF NOT EXISTS idx_extraction_created 
ON extraction_results(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_coaching_run_agent 
ON coaching_sessions(run_id, agent_id);

-- Vacuum and analyze tables
VACUUM ANALYZE coaching_performance;
VACUUM ANALYZE extraction_results;

-- Check slow queries
SELECT 
    query,
    calls,
    mean_exec_time as avg_ms,
    max_exec_time as max_ms
FROM pg_stat_statements
WHERE mean_exec_time > 1000  -- Queries averaging >1 second
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Caching Optimization
```python
# Implement section caching to avoid re-processing
class SectionCache:
    def __init__(self, ttl_hours=24):
        self.cache = {}
        self.ttl = ttl_hours * 3600
        
    def get_or_compute(self, pdf_hash, compute_func):
        if pdf_hash in self.cache:
            entry = self.cache[pdf_hash]
            if time.time() - entry['timestamp'] < self.ttl:
                print(f"✅ Cache hit for {pdf_hash[:8]}")
                return entry['sections']
        
        # Compute and cache
        sections = compute_func()
        self.cache[pdf_hash] = {
            'sections': sections,
            'timestamp': time.time()
        }
        return sections
```

## 🔧 TROUBLESHOOTING GUIDE

### Issue: Extraction Accuracy Dropping
```bash
# 1. Check recent coaching strategies
psql -U postgres -d zelda_arsredovisning -c "
SELECT strategy, COUNT(*), AVG(improvement) 
FROM coaching_sessions 
WHERE created_at > NOW() - INTERVAL '1 day'
GROUP BY strategy;"

# 2. Identify problematic agents
psql -U postgres -d zelda_arsredovisning -c "
SELECT agent_id, AVG(accuracy) as recent_avg
FROM coaching_performance
WHERE created_at > NOW() - INTERVAL '1 day'
GROUP BY agent_id
HAVING AVG(accuracy) < 0.7
ORDER BY recent_avg;"

# 3. Force exploration strategy for stuck agents
python << 'EOF'
from coaching.card_g4_reinforced_coach_fixed import Card_G4_ReinforcedCoach

coach = Card_G4_ReinforcedCoach(db_config)
coach.force_strategy('stuck_agent', 'EXPLORE')
EOF
```

### Issue: Twin Agents Disagreeing
```python
# Compare twin agent outputs
def compare_twin_outputs(doc_id, run_id):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT model, json_data, success
        FROM extraction_results
        WHERE doc_id = %s AND run_id = %s
        ORDER BY model
    """, (doc_id, run_id))
    
    results = cur.fetchall()
    if len(results) == 2:
        qwen_data = json.loads(results[0][1])
        gemini_data = json.loads(results[1][1])
        
        # Find disagreements
        disagreements = {}
        for key in set(qwen_data.keys()) | set(gemini_data.keys()):
            if qwen_data.get(key) != gemini_data.get(key):
                disagreements[key] = {
                    'qwen': qwen_data.get(key),
                    'gemini': gemini_data.get(key)
                }
        
        return disagreements
```

### Issue: Database Connection Pool Exhausted
```sql
-- Check active connections
SELECT pid, usename, application_name, state, query_start
FROM pg_stat_activity
WHERE datname = 'zelda_arsredovisning'
ORDER BY query_start;

-- Kill idle connections older than 1 hour
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'zelda_arsredovisning'
  AND state = 'idle'
  AND state_change < NOW() - INTERVAL '1 hour';

-- Increase connection pool if needed
ALTER SYSTEM SET max_connections = 200;
-- Then restart PostgreSQL
```

### Issue: Model Loading Failures
```bash
# Clear model cache
rm -rf ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-VL-7B-Instruct

# Re-download model
python -c "
from transformers import Qwen2VLForConditionalGeneration
model = Qwen2VLForConditionalGeneration.from_pretrained(
    'Qwen/Qwen2.5-VL-7B-Instruct',
    cache_dir='/tmp/models',
    force_download=True
)
print('✅ Model re-downloaded')
"

# Verify CUDA
python -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA devices: {torch.cuda.device_count()}')
print(f'Current device: {torch.cuda.current_device()}')
"
```

## 📈 PRODUCTION MONITORING

### Grafana Dashboard Queries
```sql
-- For accuracy tracking
SELECT 
    date_trunc('hour', created_at) as time,
    AVG(accuracy) as avg_accuracy,
    AVG(f1_score) as avg_f1,
    COUNT(*) as extractions
FROM coaching_performance
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY 1
ORDER BY 1;

-- For agent performance
SELECT 
    agent_id,
    AVG(accuracy) as accuracy,
    COUNT(*) as volume
FROM coaching_performance
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY agent_id;

-- For system health
SELECT 
    date_trunc('minute', created_at) as time,
    AVG(processing_time_ms) as avg_latency,
    MAX(processing_time_ms) as max_latency,
    COUNT(*) as requests
FROM extraction_results
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY 1
ORDER BY 1;
```

### Alert Conditions
```python
# Set up alerts for critical conditions
ALERT_CONDITIONS = {
    'accuracy_drop': {
        'query': "SELECT AVG(accuracy) FROM coaching_performance WHERE created_at > NOW() - INTERVAL '1 hour'",
        'threshold': 0.70,
        'operator': '<',
        'message': "⚠️ Accuracy dropped below 70%"
    },
    'no_golden_examples': {
        'query': "SELECT COUNT(*) FROM golden_examples WHERE created_at > NOW() - INTERVAL '24 hours'",
        'threshold': 0,
        'operator': '==',
        'message': "📊 No golden examples in 24 hours"
    },
    'high_error_rate': {
        'query': "SELECT COUNT(*) FROM extraction_results WHERE success = false AND created_at > NOW() - INTERVAL '1 hour'",
        'threshold': 10,
        'operator': '>',
        'message': "❌ High error rate detected"
    }
}

def check_alerts():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    for name, condition in ALERT_CONDITIONS.items():
        cur.execute(condition['query'])
        value = cur.fetchone()[0]
        
        if eval(f"{value} {condition['operator']} {condition['threshold']}"):
            send_alert(condition['message'])
```

## 🎯 PRODUCTION CHECKLIST

### Daily Tasks
- [ ] Check system health dashboard
- [ ] Review overnight coaching progress
- [ ] Verify twin agent consensus rate
- [ ] Check for new golden examples
- [ ] Monitor GPU/memory usage
- [ ] Review error logs
- [ ] Backup coaching database

### Weekly Tasks
- [ ] Analyze phase progression
- [ ] Extract top-performing prompts
- [ ] Review agent accuracy trends
- [ ] Optimize slow database queries
- [ ] Clean up old logs and caches
- [ ] Update golden examples library
- [ ] Plan next batch processing

### Phase Transitions
- [ ] Verify phase completion metrics
- [ ] Extract learnings from current phase
- [ ] Update coaching parameters
- [ ] Archive phase-specific data
- [ ] Prepare for next phase goals
- [ ] Update monitoring thresholds
- [ ] Document lessons learned

## 🚨 EMERGENCY PROCEDURES

### Rollback to Previous State
```bash
# 1. Stop current processing
pkill -f "python.*run_prod"

# 2. Restore previous prompts
psql -U postgres -d zelda_arsredovisning << 'SQL'
-- Revert to best-known prompts
UPDATE prompt_execution_history
SET prompt_text = (
    SELECT prompt_text 
    FROM prompt_execution_history p2
    WHERE p2.agent_id = prompt_execution_history.agent_id
    AND p2.accuracy = (
        SELECT MAX(accuracy) 
        FROM prompt_execution_history p3
        WHERE p3.agent_id = prompt_execution_history.agent_id
    )
    LIMIT 1
)
WHERE prompt_version = (
    SELECT MAX(prompt_version)
    FROM prompt_execution_history p4
    WHERE p4.agent_id = prompt_execution_history.agent_id
);
SQL

# 3. Clear bad coaching sessions
psql -U postgres -d zelda_arsredovisning -c "
DELETE FROM coaching_sessions 
WHERE created_at > NOW() - INTERVAL '1 hour'
AND run_id IN (
    SELECT DISTINCT run_id 
    FROM extraction_results 
    WHERE success = false
);"

# 4. Restart with safe parameters
python scripts/run_prod.py \
  --run-id "RECOVERY_$(date +%s)" \
  --limit 1 \
  --disable-coaching  # Run without coaching first
```

### Complete System Reset
```bash
# Only in extreme cases!
read -p "⚠️ This will reset ALL learning. Continue? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    psql -U postgres -d zelda_arsredovisning << 'SQL'
    TRUNCATE coaching_sessions, coaching_performance, golden_examples CASCADE;
    UPDATE prompt_execution_history SET usage_count = 0;
    SQL
    echo "✅ System reset complete. Starting from Phase 1."
fi
```

## 📋 PRODUCTION GUARDRAILS

From CLAUDE.md (NEVER VIOLATE):

### Required Checks
```python
# Pre-flight validation
def validate_production_ready():
    checks = []
    
    # 1. Database has enough documents
    doc_count = get_document_count()
    checks.append(('doc_count', doc_count >= 100, f"Docs: {doc_count}"))
    
    # 2. Strict observability enabled
    checks.append(('obs_strict', os.environ.get('OBS_STRICT') == '1', "OBS_STRICT"))
    checks.append(('json_salvage', os.environ.get('JSON_SALVAGE') == '0', "JSON_SALVAGE"))
    
    # 3. No simulation
    checks.append(('no_sleep', not has_sleep_in_code(), "No time.sleep"))
    
    # 4. Model versions correct
    checks.append(('qwen_model', verify_qwen_model(), "Qwen model"))
    checks.append(('gemini_model', verify_gemini_model(), "Gemini model"))
    
    # 5. Canaries pass
    checks.append(('canaries', verify_sjoestaden_canaries(), "Sjöstaden canaries"))
    
    failed = [name for name, passed, msg in checks if not passed]
    if failed:
        raise ValueError(f"Production checks failed: {failed}")
    
    print("✅ All production checks passed")
    return True
```

### Sjöstaden 2 Canaries
```python
SJOESTADEN_CANARIES = {
    'assets': 301_339_818,
    'total_debt': 99_538_124,
    'cash': 7_335_586,
    'org_no': '769606-2533',
    'chairman': 'Rolf Johansson',
    'auditor': 'Katarina Nyberg'
}

def verify_canary_extraction(extraction):
    """Verify extraction against known ground truth"""
    
    tolerance = 0.01  # 1% tolerance for amounts
    
    checks = []
    for field, expected in SJOESTADEN_CANARIES.items():
        if isinstance(expected, int):
            actual = extraction.get(field, 0)
            passed = abs(actual - expected) / expected < tolerance
        else:
            actual = extraction.get(field, '')
            passed = actual.lower() == expected.lower()
        
        checks.append((field, passed, actual, expected))
    
    failed = [(f, actual, expected) for f, passed, actual, expected in checks if not passed]
    if failed:
        print(f"❌ Canary failed: {failed}")
        return False
    
    return True
```

## 🎉 SUCCESS METRICS

### You're succeeding when:
- ✅ Daily accuracy improves consistently
- ✅ Golden examples accumulate (2-3 per day minimum)
- ✅ Coaching rounds decrease over time
- ✅ Twin agents agree 80%+ of the time
- ✅ Processing time stays under 2s/page
- ✅ No critical errors in 24 hours
- ✅ Phase transitions happen on schedule

### You need intervention when:
- ❌ Accuracy plateaus for 3+ days
- ❌ No golden examples in 48 hours
- ❌ Coaching rounds increasing
- ❌ Twin agents disagree >40%
- ❌ Processing time exceeds 5s/page
- ❌ Critical errors repeating
- ❌ Behind phase schedule by 20%+ documents

## 📚 COMPLETE DOCUMENTATION CHAIN

You've now read the complete quadruple MD chain:

1. ✅ **[MD1_GOLDEN_FORTRESS_OVERVIEW.md](MD1_GOLDEN_FORTRESS_OVERVIEW.md)** - System architecture
2. ✅ **[MD2_H100_DEPLOYMENT_GUIDE.md](MD2_H100_DEPLOYMENT_GUIDE.md)** - Deployment instructions
3. ✅ **[MD3_CARD_G4_IMPLEMENTATION.md](MD3_CARD_G4_IMPLEMENTATION.md)** - Learning system
4. ✅ **[MD4_PRODUCTION_OPERATIONS.md](MD4_PRODUCTION_OPERATIONS.md)** - Daily operations

With this documentation, you have everything needed to:
- Understand the complete system
- Deploy to H100 successfully
- Run the maiden voyage with 100% success
- Operate in production
- Troubleshoot any issues
- Achieve 95%+ accuracy goal

---

*The Golden Fortress is now fully documented and operational. May your extractions be accurate and your learning continuous!* 🏰