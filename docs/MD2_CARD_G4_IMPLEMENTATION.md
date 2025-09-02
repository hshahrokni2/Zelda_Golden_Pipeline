# 🎮 MD2: CARD G4 IMPLEMENTATION
## Complete Reinforced Coaching System with Gemini 2.5 Pro

### 📋 **PREREQUISITES**
- Must have read MD1_REINFORCED_LEARNING_OVERVIEW.md
- PostgreSQL with coaching tables created
- Gemini 2.5 Pro API access
- Golden Orchestrator Pipeline deployed

## 🏗️ **CARD G4 ARCHITECTURE**

### **Core Implementation**

```python
# /tmp/Golden_Orchestrator_Pipeline/coaching/card_g4_reinforced_coach.py

import json
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass
import psycopg2
from psycopg2.extras import RealDictCursor
import google.generativeai as genai

@dataclass
class ExtractionPerformance:
    accuracy: float
    coverage: float
    precision: float
    recall: float
    f1_score: float
    errors: List[str]
    missing_fields: List[str]
    
@dataclass
class CoachingDecision:
    strategy: str  # 'revert', 'refine', 'maintain', 'explore'
    target_round: Optional[int]
    new_prompt: Optional[str]
    examples_to_add: List[Dict]
    reasoning: str
    confidence: float

class Card_G4_ReinforcedCoach:
    """
    Implements reinforced learning coaching system that learns
    from 200 PDFs to achieve golden prompt state.
    """
    
    def __init__(self, db_config: Dict):
        self.db = psycopg2.connect(**db_config)
        self.gemini = genai.GenerativeModel('gemini-2.5-pro')
        
        # Coaching constraints
        self.max_rounds = {
            'sectionizer': 2,
            'governance_agent': 5,
            'balance_sheet_agent': 5,
            'income_statement_agent': 5,
            'suppliers_vendors_agent': 5,
            # ... other agents
        }
        
        # Learning phase detection
        self.learning_phase = self._detect_learning_phase()
        
        # Performance memory
        self.performance_cache = {}
        self.load_performance_history()
    
    def _detect_learning_phase(self) -> int:
        """Determine current learning phase based on PDFs processed"""
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT COUNT(DISTINCT doc_id) as pdf_count 
                FROM coaching_performance
            """)
            pdf_count = cur.fetchone()[0]
            
        if pdf_count <= 50:
            return 1  # Exploration
        elif pdf_count <= 150:
            return 2  # Optimization
        elif pdf_count <= 200:
            return 3  # Convergence
        else:
            return 4  # Golden State
    
    def coach_extraction(self, 
                        doc_id: str,
                        agent_id: str, 
                        current_extraction: Dict,
                        ground_truth: Optional[Dict] = None) -> Dict:
        """
        Main coaching entry point with reinforced learning
        """
        # 1. Analyze current performance
        performance = self.analyze_performance(
            current_extraction, 
            ground_truth
        )
        
        # 2. Get historical context
        historical_context = self.get_historical_context(
            agent_id, 
            doc_id
        )
        
        # 3. Make coaching decision
        decision = self.make_coaching_decision(
            agent_id,
            performance,
            historical_context
        )
        
        # 4. Apply coaching if needed
        if decision.strategy != 'maintain':
            coached_result = self.apply_coaching(
                agent_id,
                doc_id,
                decision
            )
            
            # 5. Validate improvement
            new_performance = self.analyze_performance(
                coached_result,
                ground_truth
            )
            
            # 6. Store learning outcome
            self.store_learning_outcome(
                doc_id,
                agent_id,
                original=current_extraction,
                coached=coached_result,
                decision=decision,
                improvement=new_performance.accuracy - performance.accuracy
            )
            
            # 7. Update golden examples if excellent
            if new_performance.accuracy >= 0.95:
                self.add_golden_example(
                    agent_id,
                    doc_id,
                    coached_result
                )
            
            return coached_result
        
        return current_extraction
    
    def analyze_performance(self, 
                           extraction: Dict, 
                           ground_truth: Optional[Dict]) -> ExtractionPerformance:
        """
        Comprehensive performance analysis
        """
        if not ground_truth:
            # Self-evaluation based on completeness and format
            return self._self_evaluate(extraction)
        
        # Calculate detailed metrics
        accuracy = self._calculate_accuracy(extraction, ground_truth)
        coverage = self._calculate_coverage(extraction, ground_truth)
        precision = self._calculate_precision(extraction, ground_truth)
        recall = self._calculate_recall(extraction, ground_truth)
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        errors = self._identify_errors(extraction, ground_truth)
        missing_fields = self._find_missing_fields(extraction, ground_truth)
        
        return ExtractionPerformance(
            accuracy=accuracy,
            coverage=coverage,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            errors=errors,
            missing_fields=missing_fields
        )
    
    def get_historical_context(self, agent_id: str, doc_id: str) -> Dict:
        """
        Retrieve comprehensive historical performance data
        """
        with self.db.cursor(cursor_factory=RealDictCursor) as cur:
            # Get best ever performance for this agent
            cur.execute("""
                SELECT * FROM coaching_performance
                WHERE agent_id = %s
                ORDER BY accuracy DESC
                LIMIT 1
            """, (agent_id,))
            best_ever = cur.fetchone()
            
            # Get recent 5 runs for this agent
            cur.execute("""
                SELECT * FROM coaching_performance
                WHERE agent_id = %s
                ORDER BY created_at DESC
                LIMIT 5
            """, (agent_id,))
            recent_runs = cur.fetchall()
            
            # Get performance trend
            cur.execute("""
                SELECT 
                    AVG(accuracy) as avg_accuracy,
                    STDDEV(accuracy) as std_accuracy,
                    COUNT(*) as run_count
                FROM coaching_performance
                WHERE agent_id = %s
                AND created_at > NOW() - INTERVAL '7 days'
            """, (agent_id,))
            trend = cur.fetchone()
            
            # Get golden examples for this agent
            cur.execute("""
                SELECT * FROM golden_examples
                WHERE agent_id = %s
                ORDER BY accuracy_score DESC
                LIMIT 3
            """, (agent_id,))
            golden_examples = cur.fetchall()
            
        return {
            'best_ever': best_ever,
            'recent_runs': recent_runs,
            'trend': trend,
            'golden_examples': golden_examples,
            'learning_phase': self.learning_phase
        }
    
    def make_coaching_decision(self,
                              agent_id: str,
                              performance: ExtractionPerformance,
                              context: Dict) -> CoachingDecision:
        """
        Intelligent coaching decision using Gemini 2.5 Pro
        """
        # Prepare comprehensive context for Gemini
        gemini_prompt = self._build_gemini_coaching_prompt(
            agent_id, 
            performance, 
            context
        )
        
        # Get Gemini's coaching recommendation
        response = self.gemini.generate_content(
            gemini_prompt,
            generation_config={
                'temperature': 0.1,  # Low temperature for consistency
                'response_mime_type': 'application/json'
            }
        )
        
        coaching_json = json.loads(response.text)
        
        # Parse and validate decision
        decision = CoachingDecision(
            strategy=coaching_json['strategy'],
            target_round=coaching_json.get('target_round'),
            new_prompt=coaching_json.get('new_prompt'),
            examples_to_add=coaching_json.get('examples', []),
            reasoning=coaching_json['reasoning'],
            confidence=coaching_json['confidence']
        )
        
        # Apply phase-specific constraints
        decision = self._apply_phase_constraints(decision)
        
        return decision
    
    def _build_gemini_coaching_prompt(self, 
                                     agent_id: str,
                                     performance: ExtractionPerformance,
                                     context: Dict) -> str:
        """
        Build comprehensive prompt for Gemini coaching
        """
        best_ever = context['best_ever']
        recent_runs = context['recent_runs']
        phase = context['learning_phase']
        
        prompt = f"""
You are coaching a Swedish BRF document extraction agent: {agent_id}
Learning Phase: {phase} (1=Exploration, 2=Optimization, 3=Convergence, 4=Golden)
PDFs Processed: {len(recent_runs)} recent runs

CURRENT PERFORMANCE:
- Accuracy: {performance.accuracy:.2%}
- Coverage: {performance.coverage:.2%}
- F1 Score: {performance.f1_score:.2%}
- Errors: {json.dumps(performance.errors[:5])}
- Missing Fields: {performance.missing_fields}

HISTORICAL CONTEXT:
Best Ever Performance:
- Accuracy: {best_ever['accuracy'] if best_ever else 0:.2%}
- Round: {best_ever['round_number'] if best_ever else 'N/A'}
- Prompt Used: {best_ever['prompt_text'][:500] if best_ever else 'None'}...

Recent 5 Runs (newest first):
"""
        for i, run in enumerate(recent_runs):
            prompt += f"""
Run {i+1}:
- Accuracy: {run['accuracy']:.2%}
- Round: {run['round_number']}
- Improvement: {run['improvement_delta']:.2%}
"""

        prompt += f"""

GOLDEN EXAMPLES AVAILABLE: {len(context['golden_examples'])}

COACHING TASK:
Based on the performance history, decide the best coaching strategy:

1. 'revert': Go back to a previous prompt that worked better (specify target_round)
2. 'refine': Make incremental improvements to current prompt
3. 'explore': Try a significantly different approach (Phase 1-2 only)
4. 'maintain': Keep current prompt (accuracy > 95%)

Consider:
- Is current performance worse than historical best?
- Are we making progress or stuck?
- Should we try something new or refine what works?
- What specific Swedish terms or patterns are we missing?

Return JSON with:
{{
    "strategy": "revert|refine|explore|maintain",
    "target_round": null or round_number to revert to,
    "new_prompt": "improved prompt text" or null,
    "examples": [
        {{"input": "example text", "expected": "expected output"}}
    ],
    "reasoning": "explain your coaching decision",
    "confidence": 0.0-1.0
}}
"""
        return prompt
    
    def _apply_phase_constraints(self, decision: CoachingDecision) -> CoachingDecision:
        """
        Apply learning phase specific constraints
        """
        if self.learning_phase == 1:
            # Phase 1: Exploration - allow aggressive changes
            return decision
            
        elif self.learning_phase == 2:
            # Phase 2: Optimization - limit exploration
            if decision.strategy == 'explore' and decision.confidence < 0.8:
                decision.strategy = 'refine'
                
        elif self.learning_phase == 3:
            # Phase 3: Convergence - mostly refinement
            if decision.strategy == 'explore':
                decision.strategy = 'refine'
                
        elif self.learning_phase == 4:
            # Phase 4: Golden - maintain unless critical
            if decision.strategy != 'maintain' and decision.confidence < 0.9:
                decision.strategy = 'maintain'
                
        return decision
    
    def apply_coaching(self,
                      agent_id: str,
                      doc_id: str,
                      decision: CoachingDecision) -> Dict:
        """
        Apply coaching decision and re-run extraction
        """
        if decision.strategy == 'revert':
            # Load previous prompt version
            prompt = self._load_prompt_version(agent_id, decision.target_round)
            
        elif decision.strategy == 'refine' or decision.strategy == 'explore':
            # Use new prompt from Gemini
            prompt = decision.new_prompt
            
            # Add examples if provided
            if decision.examples_to_add:
                prompt = self._inject_examples(prompt, decision.examples_to_add)
        else:
            # Maintain current
            return {}
        
        # Update agent registry with new prompt
        self._update_agent_prompt(agent_id, prompt)
        
        # Re-run extraction with new prompt
        # This would call the actual extraction pipeline
        new_extraction = self._run_extraction(agent_id, doc_id, prompt)
        
        return new_extraction
    
    def store_learning_outcome(self,
                              doc_id: str,
                              agent_id: str,
                              original: Dict,
                              coached: Dict,
                              decision: CoachingDecision,
                              improvement: float):
        """
        Store complete coaching session for learning
        """
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO coaching_performance (
                    session_id, doc_id, agent_id, round_number,
                    accuracy, coverage, prompt_version, prompt_text,
                    extraction_json, errors, coaching_applied,
                    improvement_delta, best_round_number, reverted_to_round,
                    created_at
                ) VALUES (
                    gen_random_uuid(), %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    NOW()
                )
            """, (
                doc_id, agent_id, self._get_current_round(agent_id, doc_id),
                coached.get('accuracy', 0), coached.get('coverage', 0),
                f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}", 
                decision.new_prompt or 'maintained',
                json.dumps(coached), json.dumps(decision.reasoning),
                json.dumps({
                    'strategy': decision.strategy,
                    'confidence': decision.confidence
                }),
                improvement,
                self._find_best_round(agent_id, doc_id),
                decision.target_round,
            ))
            self.db.commit()
    
    def add_golden_example(self, agent_id: str, doc_id: str, extraction: Dict):
        """
        Add high-quality extraction as golden example
        """
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO golden_examples (
                    example_id, agent_id, doc_type,
                    input_pages, expected_output, actual_output,
                    accuracy_score, validated_by, validation_timestamp
                ) VALUES (
                    gen_random_uuid(), %s, %s,
                    %s, %s, %s,
                    %s, %s, NOW()
                )
            """, (
                agent_id, self._classify_doc_type(doc_id),
                extraction.get('pages', []),
                json.dumps(extraction), json.dumps(extraction),
                extraction.get('accuracy', 1.0),
                'gemini-2.5-pro'
            ))
            self.db.commit()
```

## 🔄 **COACHING EXECUTION FLOW**

### **Step-by-Step Process**

```python
# Main execution pipeline integration
class ReinforcedPipeline:
    def __init__(self):
        self.coach = Card_G4_ReinforcedCoach(db_config)
        self.orchestrator = GoldenOrchestrator()
        
    def process_document_with_coaching(self, doc_id: str, pdf_path: str):
        """
        Complete pipeline with reinforced coaching
        """
        results = {}
        
        # 1. Run sectionizer with coaching
        sections = self.run_sectionizer_with_coaching(pdf_path)
        
        # 2. Map sections to agents
        agent_assignments = self.orchestrator.map_sections_to_agents(sections)
        
        # 3. Process each agent with coaching
        for agent_id, assignment in agent_assignments.items():
            # Initial extraction
            extraction = self.run_agent(agent_id, assignment)
            
            # Apply coaching if needed
            if self.should_coach(agent_id, extraction):
                extraction = self.coach.coach_extraction(
                    doc_id=doc_id,
                    agent_id=agent_id,
                    current_extraction=extraction,
                    ground_truth=self.get_ground_truth(doc_id, agent_id)
                )
            
            results[agent_id] = extraction
        
        # 4. Cross-validation between agents
        validated_results = self.cross_validate_results(results)
        
        # 5. Store final results
        self.store_results(doc_id, validated_results)
        
        return validated_results
    
    def should_coach(self, agent_id: str, extraction: Dict) -> bool:
        """
        Decide whether coaching is needed
        """
        phase = self.coach.learning_phase
        accuracy = extraction.get('accuracy', 0)
        
        if phase == 1:
            # Phase 1: Coach everything
            return True
        elif phase == 2:
            # Phase 2: Coach if below 85%
            return accuracy < 0.85
        elif phase == 3:
            # Phase 3: Coach if below 90%
            return accuracy < 0.90
        else:
            # Phase 4: Coach only failures
            return accuracy < 0.95
```

## 📊 **PERFORMANCE MONITORING**

### **Real-time Dashboard Queries**

```sql
-- Current learning phase status
SELECT 
    COUNT(DISTINCT doc_id) as pdfs_processed,
    AVG(accuracy) as avg_accuracy,
    AVG(improvement_delta) as avg_improvement,
    MAX(accuracy) as best_accuracy,
    COUNT(CASE WHEN accuracy > 0.95 THEN 1 END) as golden_count
FROM coaching_performance
WHERE created_at > NOW() - INTERVAL '24 hours';

-- Agent performance rankings
SELECT 
    agent_id,
    AVG(accuracy) as avg_accuracy,
    MAX(accuracy) as peak_accuracy,
    COUNT(*) as coaching_sessions,
    SUM(CASE WHEN improvement_delta > 0 THEN 1 ELSE 0 END) as successful_coachings
FROM coaching_performance
GROUP BY agent_id
ORDER BY avg_accuracy DESC;

-- Best prompts by agent
SELECT DISTINCT ON (agent_id)
    agent_id,
    prompt_version,
    accuracy,
    prompt_text
FROM coaching_performance
ORDER BY agent_id, accuracy DESC;
```

## 🎯 **KEY CONFIGURATION**

### **Environment Variables**
```bash
# Coaching configuration
export COACHING_ENABLED=true
export COACHING_MODEL="gemini-2.5-pro"
export MAX_COACHING_ROUNDS_SECTIONIZER=2
export MAX_COACHING_ROUNDS_AGENTS=5
export LEARNING_PHASE_AUTO_DETECT=true
export GOLDEN_THRESHOLD=0.95

# Gemini configuration
export GEMINI_API_KEY="your-key"
export GEMINI_TEMPERATURE=0.1
export GEMINI_MAX_TOKENS=4096

# Database
export COACHING_DB_URL="postgresql://user:pass@localhost:5432/coaching"
```

## 🔧 **INTEGRATION POINTS**

### **1. With Orchestrator**
```python
# In golden_orchestrator.py
def execute_with_coaching(self, doc_id, sections):
    if os.getenv('COACHING_ENABLED') == 'true':
        from coaching.card_g4_reinforced_coach import Card_G4_ReinforcedCoach
        self.coach = Card_G4_ReinforcedCoach(self.db_config)
        return self.coach.process_document_with_coaching(doc_id, sections)
    return self.execute_standard(sections)
```

### **2. With Agent Registry**
```python
# In agent_loader.py
def update_prompt_from_coaching(self, agent_id, new_prompt, version):
    """Update agent prompt based on coaching results"""
    self.agents[agent_id]['prompt'] = new_prompt
    self.agents[agent_id]['version'] = version
    self.agents[agent_id]['last_updated'] = datetime.now()
    self.save_agents()  # Persist to JSON
```

## ✅ **VALIDATION CHECKLIST**

Before proceeding to MD3:
- [ ] PostgreSQL tables created (coaching_performance, prompt_evolution, golden_examples)
- [ ] Gemini 2.5 Pro API configured and tested
- [ ] Card G4 implementation deployed to `/tmp/Golden_Orchestrator_Pipeline/coaching/`
- [ ] Environment variables set
- [ ] Integration with orchestrator verified

---

**Next: Read MD3_COACHING_EXECUTION_GUIDE.md for step-by-step execution instructions**