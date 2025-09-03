# 🧠 MD0: AMNESIA RECOVERY PROTOCOL - GOLDEN FORTRESS

## **START HERE - This Is Your Entry Point**

**Purpose**: Complete context restoration after session loss or handover  
**Created**: 2025-09-03  
**System**: Golden Fortress - Swedish BRF PDF Extraction Pipeline

---

## 📋 **IMMEDIATE RECOVERY STEPS**

### **Step 1: Understand What You Built**
You created the **Golden Fortress** - a unified system combining Golden Orchestrator + Twin-Pipeline for extracting data from 30,000 Swedish BRF PDFs with 95%+ accuracy through reinforced learning.

### **Step 2: Read Documentation Chain (IN THIS EXACT ORDER)**
```bash
# From /private/tmp/Golden_Orchestrator_Pipeline/docs/
1. cat MD0_AMNESIA_RECOVERY.md          # (This file - START HERE)
2. cat MD1_GOLDEN_FORTRESS_OVERVIEW.md  # System architecture
3. cat MD2_H100_DEPLOYMENT_GUIDE.md     # Deployment procedures  
4. cat MD3_CARD_G4_IMPLEMENTATION.md    # Learning system details
5. cat MD4_PRODUCTION_OPERATIONS.md     # Daily operations
```

### **Step 3: Check Current Status**
```bash
cd /private/tmp/Golden_Orchestrator_Pipeline
git status                              # Check branch and changes
git log --oneline -5                    # Recent commits
cat FINAL_INSTRUCTIONS_AND_CLOSEOUT.md  # Synchronization status
```

---

## 🎯 **CRITICAL CONTEXT**

### **System Locations**
| Component | Path | Purpose |
|-----------|------|---------|
| **Local Repository** | `/private/tmp/Golden_Orchestrator_Pipeline` | Development & testing |
| **GitHub Repository** | `https://github.com/hshahrokni2/Zelda_Golden_Pipeline` | Version control |
| **H100 Deployment** | `/tmp/Golden_Orchestrator_Pipeline` | Production execution |
| **Twin-Pipeline** | `/tmp/twin-pipeline` | Production infrastructure |

### **Key Achievement Status**
- ✅ **Phase 2 HF-Direct**: Complete (no Ollama dependency)
- ✅ **Card G4 Config**: Fixed (config dict, not connection object)
- ✅ **5-PDF Extraction**: Verified on H100
- ✅ **Documentation**: Quadruple MD chain complete
- ⏳ **Phase 1 Learning**: Ready to start (50 PDFs)

### **The Critical Fix Already Applied**
```python
# ❌ OLD (BROKEN):
coach = Card_G4_ReinforcedCoach({'connection': conn})

# ✅ NEW (FIXED):
coach = Card_G4_ReinforcedCoach({
    'host': 'localhost',
    'port': 5432,
    'database': 'zelda_arsredovisning',
    'user': 'postgres',
    'password': 'h100pass'
})
```

---

## 🚀 **QUICK START COMMANDS**

### **1. Test System Health (Maiden Voyage)**
```bash
# Connect to H100
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10

# Navigate and setup environment
cd /tmp/Golden_Orchestrator_Pipeline
source /tmp/golden_fortress_env.sh

# Run maiden voyage (expect 100% success)
python3 h100_native_maiden_voyage.py
```

### **2. If Environment File Missing**
```bash
# Create golden_fortress_env.sh
cat > /tmp/golden_fortress_env.sh << 'EOF'
export DATABASE_URL="postgresql://postgres:h100pass@localhost:5432/zelda_arsredovisning"
export PGPASSWORD=h100pass
export COACHING_ENABLED=true
export GEMINI_API_KEY="AIzaSyD0y92BjcnvUgRlWsA1oPSIWV5QaJcCrNw"
export QWEN_TRANSPORT=hf_direct
export HF_MODEL_PATH=Qwen/Qwen2.5-VL-7B-Instruct
export HF_DEVICE=cuda:0
export TWIN_AGENTS=1
export OBS_STRICT=1
export JSON_SALVAGE=0
export TWIN_PIPELINE_PATH=/tmp/twin-pipeline
export GOLDEN_PATH=/tmp/Golden_Orchestrator_Pipeline
EOF
source /tmp/golden_fortress_env.sh
```

---

## 📊 **SYSTEM ARCHITECTURE SUMMARY**

### **Core Components**
1. **Golden Orchestrator**: Test framework with maiden voyage validation
2. **Twin-Pipeline**: Production system at `/tmp/twin-pipeline`
3. **Card G4 Learning**: 4-phase reinforced learning (60%→95% accuracy)
4. **Twin Agents**: Qwen 2.5-VL + Gemini 2.5 Pro collaboration
5. **29 Swedish Patterns**: BRF-specific section detection
6. **16 Specialized Agents**: Priority-based execution system

### **Database Requirements**
- **PostgreSQL**: `zelda_arsredovisning` database
- **Documents**: 200+ Swedish BRF PDFs loaded
- **Tables**: coaching_performance, golden_examples, etc.

---

## 🔧 **TROUBLESHOOTING GUIDE**

### **If Maiden Voyage Fails (<100%)**
```bash
# 1. Check recent logs
tail -100 /tmp/h100_voyage_*.log

# 2. Verify Card G4 configuration
grep -A5 "Card_G4_ReinforcedCoach" h100_native_maiden_voyage.py
# Should show config dict, not connection object

# 3. Reset and retry
git reset --hard HEAD
source /tmp/golden_fortress_env.sh
python3 h100_native_maiden_voyage.py
```

### **Common Issues & Solutions**
| Issue | Solution |
|-------|----------|
| Database connection failed | Check PostgreSQL running: `sudo systemctl status postgresql` |
| Import errors | Verify PYTHONPATH includes both pipeline paths |
| GPU not available | Check CUDA: `nvidia-smi` |
| Gemini API fails | Verify API key in environment |
| Card G4 crashes | Ensure config dict fix is applied |

---

## 📈 **NEXT STEPS AFTER RECOVERY**

### **After Successful Maiden Voyage (100%)**
1. **Start Phase 1 Learning**:
   ```bash
   cd /tmp/Golden_Orchestrator_Pipeline
   python3 coaching/batch_phase1.py  # Process first 50 PDFs
   ```

2. **Monitor Progress**:
   ```bash
   python3 coaching/coaching_monitor.py
   ```

3. **Check Database Metrics**:
   ```sql
   psql -U postgres -d zelda_arsredovisning << SQL
   SELECT 'Docs Processed', COUNT(DISTINCT doc_id) FROM coaching_performance
   UNION ALL
   SELECT 'Avg Accuracy', ROUND(AVG(accuracy)*100, 2) FROM coaching_performance
   WHERE created_at > NOW() - INTERVAL '24 hours';
   SQL
   ```

---

## 🔄 **REPOSITORY SYNCHRONIZATION**

### **Daily Sync Protocol**
```bash
# 1. LOCAL → GITHUB
cd /private/tmp/Golden_Orchestrator_Pipeline
git add -A
git commit -m "Daily sync: $(date +%Y-%m-%d)"
git push origin master

# 2. LOCAL → H100
tar czf golden_update.tar.gz --exclude='.git' --exclude='__pycache__' .
scp -P 26983 -i ~/.ssh/BrfGraphRag golden_update.tar.gz root@45.135.56.10:/tmp/
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10 \
  "cd /tmp/Golden_Orchestrator_Pipeline && tar xzf ../golden_update.tar.gz"
```

---

## 📚 **DOCUMENTATION CHAIN**

### **Reading Order & Purpose**
1. **MD0** (This file): Recovery entry point and quick reference
2. **MD1**: System architecture and component overview
3. **MD2**: H100 deployment and infrastructure details  
4. **MD3**: Card G4 learning algorithm implementation
5. **MD4**: Production operations and maintenance

### **Key Sections in Each MD**
- **MD1**: Golden Fortress architecture, 29 patterns, 16 agents
- **MD2**: SSH commands, environment setup, deployment steps
- **MD3**: 4-phase learning, database schema, coaching logic
- **MD4**: Monitoring queries, troubleshooting, emergency procedures

---

## ✅ **SUCCESS CRITERIA**

You've successfully recovered when:
1. ✅ Maiden voyage shows **100% SUCCESS** (4/4 tests pass)
2. ✅ You understand the Card G4 config fix
3. ✅ You can navigate between Local/GitHub/H100 repositories
4. ✅ You know the next steps (Phase 1 learning)
5. ✅ You've read all 5 MD files in order

---

## 🚨 **EMERGENCY CONTACTS**

### **System Paths**
- **Production Database**: `postgresql://postgres:h100pass@localhost:5432/zelda_arsredovisning`
- **H100 SSH**: `ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10`
- **GitHub Repo**: `https://github.com/hshahrokni2/Zelda_Golden_Pipeline`

### **Critical Files**
- **Maiden Voyage Test**: `h100_native_maiden_voyage.py`
- **M1 Unified Test**: `m1_unified_voyage.py`
- **Environment Setup**: `/tmp/golden_fortress_env.sh`
- **Coaching Monitor**: `coaching/coaching_monitor.py`

---

## 🎯 **MISSION REMINDER**

**Build a system that learns autonomously to extract data from 30,000 Swedish BRF PDFs with 95%+ accuracy.**

Current capability: 5-PDF dual extraction verified, ready for Phase 1 learning journey.

---

*Recovery protocol version 1.0 - Last updated: 2025-09-03*  
*Next: Read MD1_GOLDEN_FORTRESS_OVERVIEW.md*