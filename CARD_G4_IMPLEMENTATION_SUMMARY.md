# 🎯 CARD G4 REINFORCED LEARNING - IMPLEMENTATION SUMMARY
## Complete Guide for Clean Context Implementation

### 📋 **CRITICAL: READ ORDER**
1. **MD1_REINFORCED_LEARNING_OVERVIEW.md** - Vision & architecture
2. **MD2_CARD_G4_IMPLEMENTATION.md** - Technical implementation  
3. **MD3_COACHING_EXECUTION_GUIDE.md** - Step-by-step execution
4. **MD4_PRODUCTION_GOLDEN_STATE.md** - Final deployment

## 🧠 **THE VISION**

Transform the Golden Orchestrator Pipeline into an intelligent, self-improving system that learns from every PDF extraction to achieve 95%+ accuracy after processing 200 documents.

### **Key Innovation: Reinforced Learning with Memory**
- System remembers what worked best for each document type
- Gemini 2.5 Pro acts as meta-coach with full performance history
- Each agent evolves its own specialized expertise
- Golden prompts emerge naturally from successful extractions

## 🏗️ **ARCHITECTURE OVERVIEW**

```
┌─────────────────────────────────────────────────────────┐
│                    REINFORCED LEARNING SYSTEM           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Document → Sectionizer → Orchestrator → Agents        │
│      ↓           ↓            ↓            ↓            │
│  Coaching    Coaching     Coaching    Coaching          │
│      ↓           ↓            ↓            ↓            │
│  Gemini 2.5 Pro (Sees all history, makes decisions)     │
│      ↓                                                   │
│  Performance → Memory → Learning → Golden Prompts       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 **QUICK IMPLEMENTATION STEPS**

### **Phase 0: Setup (Day 1)**
```bash
# 1. SSH to H100
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10

# 2. Create database schema
PGPASSWORD=h100pass psql -U postgres -h localhost -d zelda_arsredovisning < create_coaching_schema.sql

# 3. Deploy Card G4
scp -r coaching/ root@45.135.56.10:/tmp/Golden_Orchestrator_Pipeline/

# 4. Set environment
export COACHING_ENABLED=true
export GEMINI_API_KEY="AIzaSyD0y92BjcnvUgRlWsA1oPSIWV5QaJcCrNw"
```

### **Phase 1: Exploration (PDFs 1-50)**
```python
# Aggressive coaching, try everything
python3 batch_phase1.py  # 5 rounds max per agent
# Expected: 60% → 80% accuracy
```

### **Phase 2: Optimization (PDFs 51-150)**
```python
# Selective coaching, refine what works
python3 batch_phase2.py  # 3 rounds max
# Expected: 80% → 90% accuracy
```

### **Phase 3: Convergence (PDFs 151-200)**
```python
# Minimal coaching, lock in golden prompts
python3 batch_phase3.py  # 2 rounds max
# Expected: 90% → 95% accuracy
```

### **Phase 4: Golden State (PDFs 201+)**
```python
# Extract golden prompts and deploy
python3 extract_golden_prompts.py
python3 deploy_golden_production.py
# Expected: 95%+ sustained accuracy
```

## 💡 **KEY CONCEPTS**

### **1. Performance Memory**
Every coaching session is remembered:
```python
performance_memory = {
    'agent_id': 'balance_sheet_agent',
    'doc_type': 'stockholm_brf_2024',
    'round_2_accuracy': 0.92,  # Best performance
    'round_4_accuracy': 0.88,  # Got worse!
    'decision': 'revert_to_round_2'
}
```

### **2. Gemini Meta-Coaching**
Gemini sees everything and decides strategy:
```python
gemini_context = {
    'current_performance': 0.85,
    'best_ever': 0.92,
    'recent_5_runs': [...],
    'golden_examples': [...],
    'learning_phase': 2,
    'strategy': 'revert|refine|explore|maintain'
}
```

### **3. Coaching Constraints**
- **Sectionizer**: Max 2 rounds (structure is simpler)
- **Agents**: Max 5 rounds (complex extraction logic)
- **Phase-based**: Aggressive → Selective → Minimal → None

### **4. Golden Examples**
High-quality extractions become training examples:
```python
if accuracy >= 0.95:
    save_as_golden_example(extraction)
    # Future prompts include these examples
```

## 📊 **MONITORING COMMANDS**

```bash
# Real-time progress
watch -n 10 python3 coaching_monitor.py

# Check specific agent
psql -c "SELECT * FROM coaching_performance WHERE agent_id='suppliers_vendors_agent'"

# View learning curve
python3 plot_learning_curve.py

# Validate effectiveness
python3 validate_coaching.py
```

## 🎯 **SUCCESS CRITERIA**

### **By PDF 50 (Phase 1 Complete)**
- ✅ 75%+ average accuracy
- ✅ All agents have baseline metrics
- ✅ 10+ golden examples collected

### **By PDF 150 (Phase 2 Complete)**
- ✅ 85%+ average accuracy  
- ✅ Coaching success rate >60%
- ✅ 30+ golden examples per agent

### **By PDF 200 (Phase 3 Complete)**
- ✅ 95%+ average accuracy
- ✅ Prompt stability <5% change
- ✅ Ready for production

## 🔧 **CRITICAL INTEGRATION POINTS**

### **1. With Orchestrator**
```python
# In golden_orchestrator.py, add:
if os.getenv('COACHING_ENABLED') == 'true':
    from coaching.card_g4_reinforced_coach import Card_G4_ReinforcedCoach
    self.coach = Card_G4_ReinforcedCoach(db_config)
```

### **2. With Agent Registry**
```python
# Agents update dynamically:
registry.update_agent_prompt(agent_id, new_prompt, version)
```

### **3. With Sectionizer**
```python
# Sectionizer gets coached too:
if section_coverage < 0.80:
    coach.coach_extraction('sectionizer', sections)
```

## ⚠️ **COMMON PITFALLS & SOLUTIONS**

### **Problem 1: Coaching Makes Things Worse**
```python
# Solution: Revert to best known version
if new_accuracy < best_historical - 0.10:
    revert_to_best_prompt()
```

### **Problem 2: Stuck at Local Maximum**
```python
# Solution: Exploration strategy
if no_improvement_for_5_rounds:
    strategy = "explore"  # Try radically different approach
```

### **Problem 3: Gemini Rate Limits**
```python
# Solution: Exponential backoff
for attempt in range(5):
    try:
        response = gemini.generate_content(prompt)
        break
    except RateLimitError:
        time.sleep(2 ** attempt)
```

## 📝 **IMPLEMENTATION CHECKLIST**

### **Before Starting**
- [ ] Golden Orchestrator tests passing (6/6)
- [ ] PostgreSQL has 16 agents loaded
- [ ] Gemini API key configured
- [ ] H100 SSH tunnel established

### **Card G4 Setup**
- [ ] Coaching database tables created
- [ ] Card G4 implementation deployed
- [ ] Environment variables set
- [ ] Integration with orchestrator verified

### **Phase 1 Execution**
- [ ] First PDF processed with coaching
- [ ] Batch processor for 50 PDFs ready
- [ ] Monitoring dashboard working
- [ ] Results being stored in database

### **Phase 2-3 Execution**
- [ ] Selective coaching implemented
- [ ] Golden examples accumulating
- [ ] Performance trending upward
- [ ] Prompt convergence visible

### **Phase 4 Deployment**
- [ ] Golden prompts extracted
- [ ] Production config deployed
- [ ] Coaching disabled
- [ ] Monitoring active

## 🚨 **EMERGENCY COMMANDS**

```bash
# If something goes wrong:

# 1. Check current status
python3 coaching_monitor.py

# 2. View recent errors
psql -c "SELECT * FROM coaching_performance WHERE errors IS NOT NULL ORDER BY created_at DESC LIMIT 5"

# 3. Rollback if needed
./emergency_rollback.sh

# 4. Re-enable coaching
export COACHING_ENABLED=true
export USE_GOLDEN_PROMPTS=false
```

## 🎉 **EXPECTED OUTCOME**

After implementing Card G4 and processing 200 PDFs:

1. **Sectionizer**: 98% accurate section detection with all Swedish patterns
2. **Agents**: 95%+ extraction accuracy with specialized expertise
3. **Suppliers**: Reliably finds leverantörer in the 10% that have them
4. **Speed**: <30 seconds per document (no coaching needed)
5. **Autonomy**: System self-corrects without intervention

## 🔄 **NEXT STEPS AFTER CLEAN CONTEXT**

When you return with clean context:

1. **Read the 4 MDs in order**
2. **Check current state**: `python3 coaching_monitor.py`
3. **Continue from current phase**
4. **Monitor progress**: `watch -n 10 python3 coaching_monitor.py`
5. **Extract golden prompts when ready**

---

**Remember**: The goal is to create a system that learns autonomously, improving with every document until it achieves near-perfect extraction quality. Card G4 makes this possible through reinforced learning with memory.

**Status**: Ready for implementation. All documentation complete. 🚀