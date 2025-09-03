# 📜 MD2: H100 DEPLOYMENT GUIDE - RUNNING THE SYSTEM
## Complete Instructions for H100 Deployment and Testing

**Prerequisites**: You've read [MD1_GOLDEN_FORTRESS_OVERVIEW.md](MD1_GOLDEN_FORTRESS_OVERVIEW.md)  
**Next Document**: [MD3_CARD_G4_IMPLEMENTATION.md](MD3_CARD_G4_IMPLEMENTATION.md)

## 🎯 H100 INFRASTRUCTURE

### The H100 Server
- **IP**: 45.135.56.10
- **SSH Port**: 26983
- **GPU**: NVIDIA H100 80GB HBM3
- **Database**: PostgreSQL with 200+ BRF documents
- **Models**: Qwen 2.5-VL (7B) via HF-Direct

### SSH Access
```bash
# Connect to H100
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10

# With tunnel for local access to database
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10 -N -f -L 15432:localhost:5432
```

## 🚀 DEPLOYMENT STEPS

### Step 1: Check Current Status

```bash
# SSH to H100
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10

# Check what's deployed
ls -la /tmp/Golden_Orchestrator_Pipeline
ls -la /tmp/twin-pipeline
ls -la /root/production_brf_pipeline

# Check database
psql -U postgres -d zelda_arsredovisning -c "SELECT COUNT(*) FROM arsredovisning_documents;"
# Expected: 200+ documents
```

### Step 2: Deploy Golden Orchestrator (if not present)

```bash
# From local machine
cd /private/tmp/Golden_Orchestrator_Pipeline

# Create deployment package
tar czf golden_orchestrator.tar.gz \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  .

# Copy to H100
scp -P 26983 -i ~/.ssh/BrfGraphRag \
  golden_orchestrator.tar.gz \
  root@45.135.56.10:/tmp/

# On H100, extract
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10
cd /tmp
tar xzf golden_orchestrator.tar.gz -C Golden_Orchestrator_Pipeline/
```

### Step 3: Deploy Twin-Pipeline Updates

```bash
# Copy Card G4 to twin-pipeline
cp /tmp/Golden_Orchestrator_Pipeline/coaching/card_g4_reinforced_coach_fixed.py \
   /tmp/twin-pipeline/src/coaching/

# Copy golden patterns
cp /tmp/Golden_Orchestrator_Pipeline/sectionizer/golden_patterns.json \
   /tmp/twin-pipeline/src/sectionizer/

# Copy agent registry
cp /tmp/Golden_Orchestrator_Pipeline/agents/golden_registry.json \
   /tmp/twin-pipeline/src/agents/
```

### Step 4: Environment Setup

```bash
# ON H100 - Set all required environment variables
cat > /tmp/golden_fortress_env.sh << 'EOF'
#!/bin/bash
# Golden Fortress Environment Configuration

# Database (local on H100, no tunnel)
export DATABASE_URL="postgresql://postgres:h100pass@localhost:5432/zelda_arsredovisning"
export PGPASSWORD=h100pass

# HF-Direct Configuration
export QWEN_TRANSPORT=hf_direct
export HF_MODEL_PATH=Qwen/Qwen2.5-VL-7B-Instruct
export HF_DEVICE=cuda:0
export USE_HF_DIRECT=true

# Gemini Configuration
export GEMINI_API_KEY=AIzaSyD0y92BjcnvUgRlWsA1oPSIWV5QaJcCrNw
export GEMINI_MODEL=gemini-2.5-pro

# Twin Agents
export TWIN_AGENTS=1

# Coaching
export COACHING_ENABLED=true

# Strict Mode
export OBS_STRICT=1
export JSON_SALVAGE=0

# Paths
export TWIN_PIPELINE_PATH=/tmp/twin-pipeline
export GOLDEN_PATH=/tmp/Golden_Orchestrator_Pipeline

echo "✅ Golden Fortress environment configured"
EOF

# Source it
source /tmp/golden_fortress_env.sh
```

## 🧪 RUNNING THE MAIDEN VOYAGE

### Option 1: H100-Native Voyage (RECOMMENDED)

```bash
# ON H100
cd /tmp/Golden_Orchestrator_Pipeline
source /tmp/golden_fortress_env.sh
python3 h100_native_maiden_voyage.py
```

Expected Output:
```
🚀 H100-NATIVE GOLDEN FORTRESS VOYAGE

✅ H100 Environment Configured:
  - Database: localhost:5432/zelda_arsredovisning
  - Twin Pipeline: /tmp/twin-pipeline
  - Golden Orchestrator: /tmp/Golden_Orchestrator_Pipeline

✅ Database connection pool created
🔧 Preparing Database...
  - Table arsredovisning_documents: ✅ EXISTS
  - Table agent_registry: ✅ EXISTS
  - Table coaching_sessions: ✅ EXISTS
  - Table prompt_execution_history: ✅ EXISTS

================================================================================
🚢 H100-NATIVE MAIDEN VOYAGE - GOLDEN FORTRESS
================================================================================

📌 Testing Database Connection...
  ✅ Database connected: 200 documents

📌 Testing Golden Patterns...
  ✅ 29 section patterns loaded
  ✅ 3 supplier patterns found

📌 Testing Twin-Pipeline Card G4...
  ✅ Card G4 initialized - Phase 1
  ✅ Performance analysis: accuracy=0.65

📌 Testing Unified Golden Fortress...
  ✅ 16 agents in registry
  ✅ Unified coach: EXISTS
  ✅ Shadow orchestrator: ENHANCED

================================================================================
🏁 VOYAGE COMPLETE
================================================================================
  Tests Passed: 4/4
  Duration: 12.45s
  Success Rate: 100.0%
  Status: 🎯 EXCELLENT - 100% SUCCESS!

📊 Results saved to: /tmp/h100_voyage_results_20250903_123456.json

✅ 100% SUCCESS! All tests passed! Golden Fortress is fully operational.
```

### Option 2: Unified Voyage (Alternative)

```bash
# ON H100
cd /tmp/Golden_Orchestrator_Pipeline
source /tmp/golden_fortress_env.sh
python3 m1_unified_voyage.py
```

### Option 3: Production Run

```bash
# ON H100
cd /tmp/twin-pipeline
source /tmp/golden_fortress_env.sh

# Run with one PDF
RUN_ID="RUN_$(date +%s)"
python scripts/run_prod.py --run-id "$RUN_ID" --limit 1

# Check results
tail -n 50 artifacts/calls_log.ndjson | grep "$RUN_ID"
```

## 🔍 VERIFICATION CHECKLIST

Run these checks to ensure everything is working:

### Database Health
```sql
-- Connect to database
psql -U postgres -d zelda_arsredovisning

-- Check document count
SELECT COUNT(*) FROM arsredovisning_documents;
-- Expected: 200+

-- Check coaching tables
SELECT COUNT(*) FROM coaching_sessions;
SELECT COUNT(*) FROM prompt_execution_history;

-- Check recent extractions
SELECT run_id, created_at, model, success 
FROM extraction_results 
ORDER BY created_at DESC 
LIMIT 5;
```

### File System
```bash
# Check golden patterns
cat /tmp/twin-pipeline/src/sectionizer/golden_patterns.json | jq '.section_patterns | length'
# Expected: 29

# Check agent registry
cat /tmp/twin-pipeline/src/agents/golden_registry.json | jq '.agents | keys | length'
# Expected: 16

# Check Card G4
ls -la /tmp/twin-pipeline/src/coaching/card_g4_reinforced_coach_fixed.py
# Should exist
```

### Model Loading
```python
# Test HF-Direct model loading
python3 << 'EOF'
import os
os.environ['HF_MODEL_PATH'] = 'Qwen/Qwen2.5-VL-7B-Instruct'
os.environ['HF_DEVICE'] = 'cuda:0'

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2.5-VL-7B-Instruct",
    device_map="cuda:0"
)
print("✅ Model loaded successfully")
EOF
```

## 🚨 TROUBLESHOOTING

### Problem: Database Connection Failed
```bash
# Check PostgreSQL is running
systemctl status postgresql

# Check can connect locally
psql -U postgres -d zelda_arsredovisning -c "SELECT 1;"

# Check environment
echo $DATABASE_URL
```

### Problem: Card G4 Import Error
```python
# The old bug (now fixed):
# Error: "invalid dsn: invalid connection option 'connection'"

# Solution: Use config dict, not connection object
db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'zelda_arsredovisning',
    'user': 'postgres',
    'password': 'h100pass'
}
coach = Card_G4_ReinforcedCoach(db_config)
```

### Problem: Model Loading Issues
```bash
# Check CUDA
nvidia-smi

# Check PyTorch CUDA
python3 -c "import torch; print(torch.cuda.is_available())"

# Check transformers
python3 -c "import transformers; print(transformers.__version__)"
```

### Problem: SSH Connection Issues
```bash
# Check SSH key permissions
chmod 600 ~/.ssh/BrfGraphRag

# Test connection
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10 "echo 'Connected'"

# Kill old tunnels
ps aux | grep "ssh.*15432" | grep -v grep | awk '{print $2}' | xargs kill
```

## 📊 MONITORING

### Real-time Logs
```bash
# Watch coaching progress
tail -f /tmp/Golden_Orchestrator_Pipeline/logs/coaching_*.log

# Watch errors
tail -f /tmp/Golden_Orchestrator_Pipeline/logs/errors_*.log

# Watch performance
tail -f /tmp/Golden_Orchestrator_Pipeline/logs/performance_*.log
```

### Database Monitoring
```sql
-- Coaching effectiveness
SELECT 
    agent_id,
    AVG(accuracy) as avg_accuracy,
    COUNT(*) as coaching_rounds,
    MAX(accuracy) as best_accuracy
FROM coaching_performance
GROUP BY agent_id
ORDER BY avg_accuracy DESC;

-- Recent golden examples
SELECT agent_id, accuracy, created_at
FROM golden_examples
WHERE accuracy >= 0.95
ORDER BY created_at DESC
LIMIT 10;
```

## ✅ SUCCESS CRITERIA

You know deployment is successful when:

1. **All 4 tests pass** in maiden voyage (100% success rate)
2. **Database shows 200+ documents**
3. **29 patterns load** including suppliers
4. **16 agents** are in registry
5. **Card G4 initializes** without config errors
6. **Twin agents** both respond (Qwen + Gemini)
7. **Logs show** no critical errors

## 🔗 NEXT STEPS

Once deployment is verified:

1. **Run Phase 1 Learning** (first 50 PDFs)
   ```bash
   cd /tmp/Golden_Orchestrator_Pipeline
   python3 coaching/batch_phase1.py
   ```

2. **Monitor Progress**
   ```bash
   python3 coaching/coaching_monitor.py
   ```

3. **Continue to** → [MD3_CARD_G4_IMPLEMENTATION.md](MD3_CARD_G4_IMPLEMENTATION.md)
   - Understand the 4-phase learning system
   - Learn coaching strategies
   - Configure for your use case

---

*Remember: Always run tests ON H100, not FROM local. The database is at localhost:5432 when on H100.*