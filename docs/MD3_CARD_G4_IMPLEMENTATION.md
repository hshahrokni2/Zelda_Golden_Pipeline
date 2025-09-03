# 📜 MD3: CARD G4 IMPLEMENTATION - THE LEARNING ENGINE
## Complete Guide to the Reinforced Learning System

**Prerequisites**: You've read MD1 and MD2  
**Next Document**: [MD4_PRODUCTION_OPERATIONS.md](MD4_PRODUCTION_OPERATIONS.md)

## 🎯 WHAT IS CARD G4?

Card G4 is a **Reinforced Learning System** that autonomously improves extraction accuracy from 60% to 95%+ over 200 PDFs.

### Core Concepts:
- **4-Phase Learning Journey**: Exploration → Optimization → Convergence → Golden State
- **Performance Memory**: Tracks best-ever and recent performance per agent
- **Gemini Meta-Coach**: Makes strategic decisions about when and how to coach
- **Golden Examples**: Collects 95%+ accuracy extractions as templates

## 🏗️ ARCHITECTURE

### The Complete System
```
Card_G4_ReinforcedCoach
├── Learning Phases (4)
│   ├── Phase 1: Exploration (PDFs 1-50)
│   ├── Phase 2: Optimization (PDFs 51-150)
│   ├── Phase 3: Convergence (PDFs 151-200)
│   └── Phase 4: Golden State (PDFs 201+)
├── Performance Memory
│   ├── Best Ever (per agent)
│   ├── Recent Runs (last 10)
│   └── Trend Analysis
├── Coaching Strategies
│   ├── Revert (go back to best)
│   ├── Refine (small improvements)
│   ├── Explore (try new approaches)
│   └── Maintain (keep current)
└── Database Integration
    ├── coaching_sessions
    ├── coaching_performance
    ├── golden_examples
    └── prompt_execution_history
```

## 📊 THE 4-PHASE JOURNEY

### Phase 1: EXPLORATION (PDFs 1-50)
```python
{
    'learning_phase': 1,
    'accuracy_range': '60% → 80%',
    'max_coaching_rounds': 5,
    'strategy_preference': 'explore',
    'goals': [
        'Discover what works',
        'Build initial patterns',
        'Learn Swedish terminology',
        'Identify document structures'
    ]
}
```

**What Happens**:
- Aggressive experimentation with different prompts
- 5 coaching rounds maximum per agent
- Gemini explores various approaches
- Wide variation in results expected

### Phase 2: OPTIMIZATION (PDFs 51-150)
```python
{
    'learning_phase': 2,
    'accuracy_range': '80% → 90%',
    'max_coaching_rounds': 3,
    'strategy_preference': 'refine',
    'goals': [
        'Solidify successful patterns',
        'Reduce extraction errors',
        'Optimize prompt efficiency',
        'Build consistency'
    ]
}
```

**What Happens**:
- Focus on refining what works
- 3 coaching rounds maximum
- Less exploration, more refinement
- Consistency improves significantly

### Phase 3: CONVERGENCE (PDFs 151-200)
```python
{
    'learning_phase': 3,
    'accuracy_range': '90% → 95%',
    'max_coaching_rounds': 2,
    'strategy_preference': 'maintain',
    'goals': [
        'Handle edge cases',
        'Perfect accuracy',
        'Minimize coaching needs',
        'Prepare for production'
    ]
}
```

**What Happens**:
- Fine-tuning for edge cases
- 2 coaching rounds maximum
- Focus on maintaining high accuracy
- Collecting golden examples

### Phase 4: GOLDEN STATE (PDFs 201+)
```python
{
    'learning_phase': 4,
    'accuracy_range': '95%+',
    'max_coaching_rounds': 1,
    'strategy_preference': 'golden',
    'goals': [
        'Maintain excellence',
        'Use golden examples',
        'Minimal intervention',
        'Production ready'
    ]
}
```

**What Happens**:
- System runs autonomously
- 1 coaching round only for anomalies
- Uses golden examples as templates
- Ready for production deployment

## 🧠 THE COACHING ALGORITHM

### Core Implementation
```python
class Card_G4_ReinforcedCoach:
    def __init__(self, db_config):
        """
        IMPORTANT: db_config must be a dict with connection params,
        NOT a psycopg2 connection object!
        """
        self.db_config = db_config  # {'host': ..., 'port': ..., etc}
        self.learning_phase = self.detect_learning_phase()
        self.performance_memory = self.load_performance_memory()
        self.gemini_client = self.init_gemini()
        
    def coach_extraction(self, agent_id, extraction, ground_truth=None):
        """Main coaching pipeline"""
        
        # 1. Analyze current performance
        performance = self.analyze_performance(extraction, ground_truth)
        
        # 2. Get historical context
        history = self.get_agent_history(agent_id)
        
        # 3. Ask Gemini for coaching decision
        strategy = self.make_coaching_decision(
            agent_id, performance, history
        )
        
        # 4. Apply coaching strategy
        improved_prompt = self.apply_coaching_strategy(
            agent_id, strategy, extraction
        )
        
        # 5. Store learning outcome
        self.store_learning_outcome(
            agent_id, performance, strategy, improved_prompt
        )
        
        # 6. Check for golden example
        if performance.accuracy >= 0.95:
            self.save_golden_example(agent_id, extraction)
            
        return improved_prompt
```

### Performance Analysis
```python
def analyze_performance(self, extraction, ground_truth):
    """Calculate accuracy, coverage, and F1 score"""
    
    if ground_truth:
        # Direct comparison
        accuracy = self.calculate_accuracy(extraction, ground_truth)
        coverage = self.calculate_coverage(extraction, ground_truth)
        f1_score = self.calculate_f1(accuracy, coverage)
    else:
        # Heuristic evaluation
        accuracy = self.estimate_accuracy(extraction)
        coverage = self.estimate_coverage(extraction)
        f1_score = (2 * accuracy * coverage) / (accuracy + coverage)
        
    return Performance(
        accuracy=accuracy,
        coverage=coverage,
        f1_score=f1_score,
        empty_fields=self.count_empty_fields(extraction),
        extraction_time_ms=extraction.get('time_ms', 0)
    )
```

### Coaching Decision with Gemini
```python
def make_coaching_decision(self, agent_id, performance, history):
    """Ask Gemini 2.5 Pro for strategic coaching decision"""
    
    prompt = f"""
    You are coaching {agent_id} in Phase {self.learning_phase}.
    
    Current Performance:
    - Accuracy: {performance.accuracy:.2%}
    - Coverage: {performance.coverage:.2%}
    - F1 Score: {performance.f1_score:.2%}
    
    Historical Context:
    - Best Ever: {history.best_accuracy:.2%}
    - Recent Average: {history.recent_average:.2%}
    - Trend: {history.trend}
    - Total Runs: {history.total_runs}
    
    Phase {self.learning_phase} Guidelines:
    - Max Rounds: {self.get_max_rounds()}
    - Target Accuracy: {self.get_target_accuracy():.2%}
    - Preferred Strategy: {self.get_preferred_strategy()}
    
    Choose coaching strategy:
    1. REVERT - Go back to best-ever prompt (accuracy dropped >10%)
    2. REFINE - Make small improvements (accuracy 70-90%)
    3. EXPLORE - Try new approach (accuracy <70% or stuck)
    4. MAINTAIN - Keep current (accuracy >90% and stable)
    
    Return: REVERT|REFINE|EXPLORE|MAINTAIN
    """
    
    response = self.gemini_client.generate(prompt)
    return response.strip()
```

### Coaching Strategies
```python
def apply_coaching_strategy(self, agent_id, strategy, extraction):
    """Apply the chosen coaching strategy"""
    
    if strategy == 'REVERT':
        # Go back to best-ever prompt
        return self.get_best_prompt(agent_id)
        
    elif strategy == 'REFINE':
        # Small improvements to current prompt
        return self.refine_prompt(agent_id, extraction)
        
    elif strategy == 'EXPLORE':
        # Try completely new approach
        return self.explore_new_prompt(agent_id, extraction)
        
    elif strategy == 'MAINTAIN':
        # Keep current prompt
        return self.get_current_prompt(agent_id)
        
    else:
        # Fallback to refinement
        return self.refine_prompt(agent_id, extraction)
```

## 💾 DATABASE SCHEMA

### Core Tables
```sql
-- Performance tracking per agent
CREATE TABLE coaching_performance (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100),
    doc_id VARCHAR(100),
    accuracy FLOAT,
    coverage FLOAT,
    f1_score FLOAT,
    strategy VARCHAR(20),
    phase INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Golden examples (95%+ accuracy)
CREATE TABLE golden_examples (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100),
    doc_id VARCHAR(100),
    extraction JSONB,
    prompt TEXT,
    accuracy FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Coaching session tracking
CREATE TABLE coaching_sessions (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100),
    agent_id VARCHAR(100),
    round INTEGER,
    strategy VARCHAR(20),
    improvement FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prompt evolution history
CREATE TABLE prompt_execution_history (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100),
    prompt_version INTEGER,
    prompt_text TEXT,
    accuracy FLOAT,
    usage_count INTEGER,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes for Performance
```sql
CREATE INDEX idx_coaching_performance_agent ON coaching_performance(agent_id);
CREATE INDEX idx_golden_examples_agent ON golden_examples(agent_id);
CREATE INDEX idx_golden_examples_accuracy ON golden_examples(accuracy DESC);
CREATE INDEX idx_coaching_sessions_run ON coaching_sessions(run_id);
CREATE INDEX idx_prompt_history_agent ON prompt_execution_history(agent_id);
```

## 🚀 RUNNING CARD G4

### Single Document Coaching
```python
# Initialize Card G4 with correct config
from coaching.card_g4_reinforced_coach_fixed import Card_G4_ReinforcedCoach

db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'zelda_arsredovisning',
    'user': 'postgres',
    'password': 'h100pass'
}

coach = Card_G4_ReinforcedCoach(db_config)

# Coach an extraction
extraction = agent.extract(document)
improved_prompt = coach.coach_extraction(
    agent_id='governance_agent',
    extraction=extraction,
    ground_truth=None  # Or provide if available
)

# Use improved prompt
better_extraction = agent.extract_with_prompt(document, improved_prompt)
```

### Batch Processing (Phase 1)
```python
# Process first 50 PDFs with aggressive coaching
def run_phase1_batch():
    """Process PDFs 1-50 with Card G4 learning"""
    
    coach = Card_G4_ReinforcedCoach(db_config)
    documents = load_documents(1, 50)
    
    for doc in documents:
        print(f"\n📄 Processing: {doc.id}")
        
        # Run all agents with coaching
        for agent_id in AGENT_REGISTRY:
            print(f"  🤖 Agent: {agent_id}")
            
            # Initial extraction
            extraction = run_agent(agent_id, doc)
            
            # Coach up to 5 rounds (Phase 1)
            for round in range(coach.get_max_rounds()):
                improved = coach.coach_extraction(
                    agent_id, extraction
                )
                
                # Re-extract with improved prompt
                extraction = run_agent_with_prompt(
                    agent_id, doc, improved
                )
                
                # Check if good enough
                if extraction['accuracy'] >= 0.80:
                    print(f"    ✅ Target reached: {extraction['accuracy']:.2%}")
                    break
                    
            # Save results
            save_extraction(doc.id, agent_id, extraction)
```

### Monitoring Progress
```python
def monitor_card_g4_progress():
    """Monitor Card G4 learning progress"""
    
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    # Overall progress
    cur.execute("""
        SELECT 
            COUNT(DISTINCT doc_id) as docs_processed,
            AVG(accuracy) as avg_accuracy,
            MAX(accuracy) as best_accuracy,
            COUNT(DISTINCT agent_id) as agents_active
        FROM coaching_performance
        WHERE phase = %s
    """, (1,))
    
    progress = cur.fetchone()
    print(f"""
    📊 CARD G4 PROGRESS - PHASE 1
    ================================
    Documents: {progress[0]}/50
    Average Accuracy: {progress[1]:.2%}
    Best Accuracy: {progress[2]:.2%}
    Active Agents: {progress[3]}/16
    """)
    
    # Per-agent progress
    cur.execute("""
        SELECT 
            agent_id,
            COUNT(*) as coaching_rounds,
            AVG(accuracy) as avg_accuracy,
            MAX(accuracy) as best_accuracy
        FROM coaching_performance
        WHERE phase = 1
        GROUP BY agent_id
        ORDER BY avg_accuracy DESC
    """)
    
    print("\n🤖 AGENT PERFORMANCE:")
    for row in cur.fetchall():
        print(f"  {row[0]:30s} Rounds: {row[1]:3d} Avg: {row[2]:.2%} Best: {row[3]:.2%}")
```

## 🎯 BEST PRACTICES

### Do's:
✅ **Always use config dict** for Card G4 initialization  
✅ **Let it run complete rounds** - don't interrupt coaching  
✅ **Monitor progress regularly** but don't micromanage  
✅ **Save golden examples** when accuracy >= 95%  
✅ **Follow phase guidelines** - don't skip phases

### Don'ts:
❌ **Don't pass connection objects** to Card G4  
❌ **Don't override phase settings** unless necessary  
❌ **Don't clear coaching history** - it's valuable  
❌ **Don't skip to Phase 4** without completing 1-3  
❌ **Don't ignore failing agents** - they need more coaching

## 📈 EXPECTED OUTCOMES

### After Phase 1 (50 PDFs):
- Average accuracy: 75-80%
- Best agents: 85%+
- Worst agents: 65%+
- Swedish terms learned
- Document patterns identified

### After Phase 2 (150 PDFs):
- Average accuracy: 85-90%
- Best agents: 92%+
- Worst agents: 80%+
- Consistent performance
- Fewer coaching rounds needed

### After Phase 3 (200 PDFs):
- Average accuracy: 92-95%
- Best agents: 97%+
- Worst agents: 88%+
- Golden examples collected
- Production ready

### Phase 4 (Production):
- Average accuracy: 95%+
- Minimal coaching needed
- Autonomous operation
- Golden examples used
- New documents handled well

## 🔧 TROUBLESHOOTING CARD G4

### Issue: "invalid dsn: invalid connection option"
```python
# Wrong
coach = Card_G4_ReinforcedCoach({'connection': conn})

# Right
coach = Card_G4_ReinforcedCoach({
    'host': 'localhost',
    'port': 5432,
    'database': 'zelda_arsredovisning',
    'user': 'postgres',
    'password': 'h100pass'
})
```

### Issue: Coaching not improving accuracy
```sql
-- Check if strategies are varied
SELECT strategy, COUNT(*) 
FROM coaching_sessions 
GROUP BY strategy;

-- If stuck on one strategy, manually trigger exploration
UPDATE coaching_performance 
SET strategy = 'EXPLORE' 
WHERE agent_id = 'stuck_agent' 
AND accuracy < 0.7;
```

### Issue: Gemini API errors
```python
# Add retry logic
def make_coaching_decision_with_retry(self, *args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return self.make_coaching_decision(*args)
        except Exception as e:
            if attempt == max_retries - 1:
                # Fallback to phase default
                return self.get_preferred_strategy()
            time.sleep(2 ** attempt)  # Exponential backoff
```

## 🔗 NEXT STEPS

After understanding Card G4:

1. **Start Phase 1** with first 50 PDFs
2. **Monitor progress** daily
3. **Collect golden examples** at 95%+
4. **Continue to** → [MD4_PRODUCTION_OPERATIONS.md](MD4_PRODUCTION_OPERATIONS.md)

---

*Remember: Card G4 is a marathon, not a sprint. Let it learn at its own pace through all 4 phases.*