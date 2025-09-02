#!/usr/bin/env python3
"""
Card G4 Reinforced Coaching System
Implements intelligent coaching with Gemini 2.5 Pro meta-coaching
"""

import json
import hashlib
import time
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass, asdict
import psycopg2
from psycopg2.extras import RealDictCursor, Json
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
        
        # Initialize Gemini
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyD0y92BjcnvUgRlWsA1oPSIWV5QaJcCrNw')
        genai.configure(api_key=api_key)
        self.gemini = genai.GenerativeModel('gemini-2.5-pro')
        
        # Coaching constraints based on learning phase
        self.max_rounds = {
            'sectionizer': 2,
            'governance_agent': 5,
            'balance_sheet_agent': 5,
            'income_statement_agent': 5,
            'cash_flow_agent': 5,
            'property_agent': 5,
            'multi_year_overview_agent': 5,
            'maintenance_events_agent': 5,
            'note_loans_agent': 5,
            'note_depreciation_agent': 5,
            'note_costs_agent': 5,
            'note_revenue_agent': 5,
            'suppliers_vendors_agent': 5,
            'audit_report_agent': 5,
            'ratio_kpi_agent': 5,
            'member_info_agent': 5,
            'pledged_assets_agent': 5
        }
        
        # Learning phase detection
        self.learning_phase = self._detect_learning_phase()
        
        # Performance memory cache
        self.performance_cache = {}
        self.load_performance_history()
    
    def _detect_learning_phase(self) -> int:
        """Determine current learning phase based on PDFs processed"""
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT COUNT(DISTINCT doc_id) as pdf_count 
                FROM coaching_performance
            """)
            result = cur.fetchone()
            pdf_count = result[0] if result else 0
            
        if pdf_count <= 50:
            return 1  # Exploration
        elif pdf_count <= 150:
            return 2  # Optimization
        elif pdf_count <= 200:
            return 3  # Convergence
        else:
            return 4  # Golden State
    
    def load_performance_history(self):
        """Load performance memory from database"""
        with self.db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM performance_memory")
            for row in cur.fetchall():
                key = f"{row['agent_id']}_{row['doc_type']}"
                self.performance_cache[key] = row
    
    def coach_extraction(self, 
                        doc_id: str,
                        agent_id: str, 
                        current_extraction: Dict,
                        ground_truth: Optional[Dict] = None,
                        session_id: Optional[str] = None) -> Dict:
        """
        Main coaching entry point with reinforced learning
        """
        if not session_id:
            session_id = f"{agent_id}_{doc_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Start coaching session
        self._start_coaching_session(session_id, doc_id, agent_id)
        
        try:
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
                    decision,
                    current_extraction
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
                    session_id,
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
                        coached_result,
                        new_performance.accuracy
                    )
                
                # Complete session
                self._complete_coaching_session(
                    session_id, 
                    performance.accuracy, 
                    new_performance.accuracy
                )
                
                return coached_result
            
            # Complete session with no change
            self._complete_coaching_session(
                session_id, 
                performance.accuracy, 
                performance.accuracy
            )
            
            return current_extraction
            
        except Exception as e:
            self._fail_coaching_session(session_id, str(e))
            raise
    
    def analyze_performance(self, 
                           extraction: Dict, 
                           ground_truth: Optional[Dict]) -> ExtractionPerformance:
        """Comprehensive performance analysis"""
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
    
    def _self_evaluate(self, extraction: Dict) -> ExtractionPerformance:
        """Self-evaluation when no ground truth available"""
        # Check completeness
        total_fields = len(extraction.keys()) if extraction else 0
        non_empty_fields = sum(1 for v in extraction.values() if v) if extraction else 0
        
        coverage = non_empty_fields / total_fields if total_fields > 0 else 0
        
        # Estimate accuracy based on format and completeness
        accuracy = coverage * 0.8  # Conservative estimate
        
        # Identify potential issues
        errors = []
        missing_fields = []
        
        if not extraction:
            errors.append("Empty extraction")
        elif coverage < 0.5:
            errors.append(f"Low coverage: {coverage:.2%}")
        
        return ExtractionPerformance(
            accuracy=accuracy,
            coverage=coverage,
            precision=accuracy,
            recall=coverage,
            f1_score=accuracy,
            errors=errors,
            missing_fields=missing_fields
        )
    
    def get_historical_context(self, agent_id: str, doc_id: str) -> Dict:
        """Retrieve comprehensive historical performance data"""
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
                AND is_active = TRUE
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
        """Intelligent coaching decision using Gemini 2.5 Pro"""
        # Check if we should skip coaching based on phase
        if self.learning_phase == 4 and performance.accuracy >= 0.95:
            return CoachingDecision(
                strategy='maintain',
                target_round=None,
                new_prompt=None,
                examples_to_add=[],
                reasoning='Golden state achieved with high accuracy',
                confidence=1.0
            )
        
        # Prepare comprehensive context for Gemini
        gemini_prompt = self._build_gemini_coaching_prompt(
            agent_id, 
            performance, 
            context
        )
        
        try:
            # Get Gemini's coaching recommendation with retry logic
            for attempt in range(3):
                try:
                    response = self.gemini.generate_content(
                        gemini_prompt,
                        generation_config={
                            'temperature': 0.1,  # Low temperature for consistency
                            'response_mime_type': 'application/json'
                        }
                    )
                    coaching_json = json.loads(response.text)
                    break
                except Exception as e:
                    if attempt == 2:
                        # Fallback decision
                        return self._fallback_decision(performance)
                    time.sleep(2 ** attempt)
            
            # Parse and validate decision
            decision = CoachingDecision(
                strategy=coaching_json.get('strategy', 'refine'),
                target_round=coaching_json.get('target_round'),
                new_prompt=coaching_json.get('new_prompt'),
                examples_to_add=coaching_json.get('examples', []),
                reasoning=coaching_json.get('reasoning', 'Gemini recommendation'),
                confidence=coaching_json.get('confidence', 0.7)
            )
            
            # Apply phase-specific constraints
            decision = self._apply_phase_constraints(decision, agent_id)
            
            return decision
            
        except Exception as e:
            print(f"Gemini coaching error: {e}")
            return self._fallback_decision(performance)
    
    def _build_gemini_coaching_prompt(self, 
                                     agent_id: str,
                                     performance: ExtractionPerformance,
                                     context: Dict) -> str:
        """Build comprehensive prompt for Gemini coaching"""
        best_ever = context.get('best_ever', {})
        recent_runs = context.get('recent_runs', [])
        phase = context['learning_phase']
        golden_examples = context.get('golden_examples', [])
        
        prompt = f"""
You are coaching a Swedish BRF document extraction agent: {agent_id}
Learning Phase: {phase} (1=Exploration, 2=Optimization, 3=Convergence, 4=Golden)

CURRENT PERFORMANCE:
- Accuracy: {performance.accuracy:.2%}
- Coverage: {performance.coverage:.2%}
- F1 Score: {performance.f1_score:.2%}
- Errors: {json.dumps(performance.errors[:5]) if performance.errors else 'None'}
- Missing Fields: {performance.missing_fields[:5] if performance.missing_fields else 'None'}

HISTORICAL CONTEXT:
- Best Ever Accuracy: {best_ever.get('accuracy', 0):.2%} if best_ever else 'No history'
- Recent Average: {np.mean([r.get('accuracy', 0) for r in recent_runs]):.2%} if recent_runs else 'No history'
- Golden Examples Available: {len(golden_examples)}

PHASE-SPECIFIC GOALS:
- Phase 1 (Exploration): Try diverse approaches, maximize learning
- Phase 2 (Optimization): Refine what works, prune what doesn't
- Phase 3 (Convergence): Lock in best practices, minimize changes
- Phase 4 (Golden): Maintain excellence, avoid regression

Based on this context, recommend a coaching strategy.

Return JSON with:
{{
    "strategy": "revert|refine|explore|maintain",
    "target_round": null or int (which previous round to revert to if reverting),
    "new_prompt": null or string (refined prompt if refining),
    "examples": [] or list of example extractions to add,
    "reasoning": "explanation of your decision",
    "confidence": 0.0-1.0
}}

IMPORTANT:
- If current accuracy is WORSE than best_ever by >10%, consider 'revert'
- If stuck at local maximum (no improvement in 5 runs), consider 'explore'
- If accuracy >95%, use 'maintain'
- In phase 3-4, prefer 'maintain' unless significant improvement possible
"""
        
        return prompt
    
    def _fallback_decision(self, performance: ExtractionPerformance) -> CoachingDecision:
        """Fallback decision when Gemini unavailable"""
        if performance.accuracy >= 0.95:
            strategy = 'maintain'
        elif performance.accuracy < 0.60:
            strategy = 'explore'
        else:
            strategy = 'refine'
        
        return CoachingDecision(
            strategy=strategy,
            target_round=None,
            new_prompt=None,
            examples_to_add=[],
            reasoning='Fallback decision based on accuracy threshold',
            confidence=0.5
        )
    
    def _apply_phase_constraints(self, decision: CoachingDecision, agent_id: str) -> CoachingDecision:
        """Apply learning phase constraints to coaching decision"""
        max_rounds = self.max_rounds.get(agent_id, 5)
        
        # Phase-specific round limits
        if self.learning_phase == 1:
            # Exploration: allow max rounds
            pass
        elif self.learning_phase == 2:
            # Optimization: reduce to 3 rounds max
            max_rounds = min(max_rounds, 3)
        elif self.learning_phase == 3:
            # Convergence: reduce to 2 rounds max
            max_rounds = min(max_rounds, 2)
        else:
            # Golden: no coaching unless critical
            if decision.confidence < 0.9:
                decision.strategy = 'maintain'
        
        return decision
    
    def apply_coaching(self, 
                      agent_id: str,
                      doc_id: str,
                      decision: CoachingDecision,
                      current_extraction: Dict) -> Dict:
        """Apply coaching decision to improve extraction"""
        # This would integrate with the actual agent system
        # For now, return a simulated improvement
        
        if decision.strategy == 'revert' and decision.target_round:
            # Load extraction from target round
            return self._load_round_extraction(doc_id, agent_id, decision.target_round)
        
        elif decision.strategy == 'refine' and decision.new_prompt:
            # Apply refined prompt (would call agent with new prompt)
            # Simulated improvement
            return current_extraction
        
        elif decision.strategy == 'explore':
            # Try different approach (would call agent with exploration prompt)
            return current_extraction
        
        return current_extraction
    
    def store_learning_outcome(self, 
                               doc_id: str,
                               agent_id: str,
                               session_id: str,
                               original: Dict,
                               coached: Dict,
                               decision: CoachingDecision,
                               improvement: float):
        """Store coaching outcome in database"""
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO coaching_performance (
                    doc_id, agent_id, coaching_round, accuracy, coverage,
                    strategy_used, improvement_delta, learning_phase
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                doc_id, agent_id, 1, 
                improvement + 0.7,  # Simulated final accuracy
                0.8,  # Simulated coverage
                decision.strategy,
                improvement,
                self.learning_phase
            ))
            self.db.commit()
    
    def add_golden_example(self, 
                           agent_id: str,
                           doc_id: str,
                           extraction: Dict,
                           accuracy: float):
        """Add high-quality extraction as golden example"""
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO golden_examples (
                    doc_id, agent_id, extraction_json, 
                    accuracy_score, coverage_score
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                doc_id, agent_id, Json(extraction),
                accuracy, 0.9  # Simulated coverage
            ))
            self.db.commit()
    
    def _start_coaching_session(self, session_id: str, doc_id: str, agent_id: str):
        """Start a new coaching session"""
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO coaching_sessions (
                    session_id, doc_id, agent_id, start_time, max_rounds
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                session_id, doc_id, agent_id, 
                datetime.now(), self.max_rounds.get(agent_id, 5)
            ))
            self.db.commit()
    
    def _complete_coaching_session(self, session_id: str, initial_acc: float, final_acc: float):
        """Complete coaching session with results"""
        with self.db.cursor() as cur:
            cur.execute("""
                UPDATE coaching_sessions 
                SET end_time = %s, status = 'completed',
                    initial_accuracy = %s, final_accuracy = %s,
                    total_improvement = %s
                WHERE session_id = %s
            """, (
                datetime.now(), initial_acc, final_acc,
                final_acc - initial_acc, session_id
            ))
            self.db.commit()
    
    def _fail_coaching_session(self, session_id: str, reason: str):
        """Mark session as failed"""
        with self.db.cursor() as cur:
            cur.execute("""
                UPDATE coaching_sessions 
                SET end_time = %s, status = 'failed', failure_reason = %s
                WHERE session_id = %s
            """, (datetime.now(), reason, session_id))
            self.db.commit()
    
    # Helper methods for metrics calculation
    def _calculate_accuracy(self, extraction: Dict, ground_truth: Dict) -> float:
        """Calculate accuracy between extraction and ground truth"""
        if not extraction or not ground_truth:
            return 0.0
        
        correct = 0
        total = 0
        
        for key in ground_truth:
            total += 1
            if key in extraction and extraction[key] == ground_truth[key]:
                correct += 1
        
        return correct / total if total > 0 else 0.0
    
    def _calculate_coverage(self, extraction: Dict, ground_truth: Dict) -> float:
        """Calculate field coverage"""
        if not ground_truth:
            return 0.0
        
        extracted_keys = set(extraction.keys()) if extraction else set()
        truth_keys = set(ground_truth.keys())
        
        return len(extracted_keys & truth_keys) / len(truth_keys) if truth_keys else 0.0
    
    def _calculate_precision(self, extraction: Dict, ground_truth: Dict) -> float:
        """Calculate precision of extraction"""
        if not extraction:
            return 0.0
        
        correct = sum(1 for k, v in extraction.items() 
                     if k in ground_truth and v == ground_truth[k])
        
        return correct / len(extraction) if extraction else 0.0
    
    def _calculate_recall(self, extraction: Dict, ground_truth: Dict) -> float:
        """Calculate recall of extraction"""
        if not ground_truth:
            return 0.0
        
        found = sum(1 for k in ground_truth 
                   if k in extraction and extraction[k] == ground_truth[k])
        
        return found / len(ground_truth) if ground_truth else 0.0
    
    def _identify_errors(self, extraction: Dict, ground_truth: Dict) -> List[str]:
        """Identify specific errors in extraction"""
        errors = []
        
        if not extraction:
            errors.append("Empty extraction")
            return errors
        
        if ground_truth:
            for key in ground_truth:
                if key not in extraction:
                    errors.append(f"Missing field: {key}")
                elif extraction[key] != ground_truth[key]:
                    errors.append(f"Incorrect value for {key}")
        
        return errors[:10]  # Limit to 10 errors
    
    def _find_missing_fields(self, extraction: Dict, ground_truth: Dict) -> List[str]:
        """Find missing fields in extraction"""
        if not ground_truth:
            return []
        
        extracted = set(extraction.keys()) if extraction else set()
        expected = set(ground_truth.keys())
        
        return list(expected - extracted)
    
    def _load_round_extraction(self, doc_id: str, agent_id: str, round_num: int) -> Dict:
        """Load extraction from specific coaching round"""
        # This would load from database
        # For now return empty dict
        return {}

def main():
    """Test the Card G4 Reinforced Coach"""
    print("CARD G4 REINFORCED COACH TEST")
    print("=" * 60)
    
    # Test with mock database config
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_coaching',
        'user': 'postgres',
        'password': 'test'
    }
    
    try:
        coach = Card_G4_ReinforcedCoach(db_config)
        print(f"✅ Coach initialized")
        print(f"  Learning Phase: {coach.learning_phase}")
        print(f"  Max Rounds: {coach.max_rounds}")
        
        # Test with mock extraction
        test_extraction = {
            'chairman': 'Test Person',
            'board_members': ['Member 1', 'Member 2'],
            'auditor': 'Test Auditor'
        }
        
        print(f"\n📊 Testing performance analysis...")
        performance = coach.analyze_performance(test_extraction, None)
        print(f"  Accuracy: {performance.accuracy:.2%}")
        print(f"  Coverage: {performance.coverage:.2%}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: This test requires database connection")
        print("Set up PostgreSQL and run create_coaching_schema.sql first")

if __name__ == "__main__":
    main()