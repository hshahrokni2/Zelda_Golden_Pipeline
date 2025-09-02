-- Card G4 Reinforced Learning Database Schema
-- Creates tables for coaching performance tracking and golden examples

-- 1. Coaching Performance Table
CREATE TABLE IF NOT EXISTS coaching_performance (
    id SERIAL PRIMARY KEY,
    doc_id UUID NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    coaching_round INTEGER NOT NULL,
    accuracy FLOAT NOT NULL,
    coverage FLOAT NOT NULL,
    precision_score FLOAT,
    recall_score FLOAT,
    f1_score FLOAT,
    errors JSONB,
    missing_fields TEXT[],
    prompt_version VARCHAR(50),
    strategy_used VARCHAR(20), -- 'revert', 'refine', 'maintain', 'explore'
    improvement_delta FLOAT,
    execution_time_ms INTEGER,
    model_used VARCHAR(50),
    learning_phase INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_agent_accuracy (agent_id, accuracy DESC),
    INDEX idx_doc_agent (doc_id, agent_id),
    INDEX idx_created (created_at DESC)
);

-- 2. Golden Examples Table
CREATE TABLE IF NOT EXISTS golden_examples (
    id SERIAL PRIMARY KEY,
    doc_id UUID NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    extraction_json JSONB NOT NULL,
    accuracy_score FLOAT NOT NULL,
    coverage_score FLOAT NOT NULL,
    section_context TEXT,
    prompt_used TEXT,
    verified_by VARCHAR(50) DEFAULT 'auto',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_agent_golden (agent_id, accuracy_score DESC),
    INDEX idx_active (is_active, agent_id)
);

-- 3. Prompt Evolution Table
CREATE TABLE IF NOT EXISTS prompt_evolution (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    prompt_text TEXT NOT NULL,
    examples_count INTEGER DEFAULT 0,
    avg_accuracy FLOAT,
    usage_count INTEGER DEFAULT 0,
    is_golden BOOLEAN DEFAULT FALSE,
    parent_version VARCHAR(50),
    evolution_strategy VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    retired_at TIMESTAMP,
    UNIQUE(agent_id, version),
    INDEX idx_agent_version (agent_id, version),
    INDEX idx_golden (is_golden, agent_id)
);

-- 4. Coaching Sessions Table
CREATE TABLE IF NOT EXISTS coaching_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    doc_id UUID NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    rounds_completed INTEGER DEFAULT 0,
    max_rounds INTEGER,
    initial_accuracy FLOAT,
    final_accuracy FLOAT,
    total_improvement FLOAT,
    best_round INTEGER,
    best_accuracy FLOAT,
    gemini_calls_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'in_progress', -- 'in_progress', 'completed', 'failed'
    failure_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    INDEX idx_status (status, created_at DESC)
);

-- 5. Performance Memory Cache Table
CREATE TABLE IF NOT EXISTS performance_memory (
    agent_id VARCHAR(100) NOT NULL,
    doc_type VARCHAR(100),
    best_round INTEGER,
    best_accuracy FLOAT,
    best_prompt_version VARCHAR(50),
    successful_strategies TEXT[],
    failed_strategies TEXT[],
    avg_improvement_per_round FLOAT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (agent_id, doc_type),
    INDEX idx_agent_type (agent_id, doc_type)
);

-- 6. Learning Metrics Table
CREATE TABLE IF NOT EXISTS learning_metrics (
    id SERIAL PRIMARY KEY,
    phase INTEGER NOT NULL, -- 1=Exploration, 2=Optimization, 3=Convergence, 4=Golden
    pdf_count INTEGER NOT NULL,
    avg_accuracy FLOAT NOT NULL,
    avg_coverage FLOAT NOT NULL,
    avg_coaching_rounds FLOAT,
    golden_examples_count INTEGER,
    successful_agents TEXT[],
    struggling_agents TEXT[],
    phase_started_at TIMESTAMP,
    phase_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_phase (phase, created_at DESC)
);

-- 7. Agent Convergence Tracking
CREATE TABLE IF NOT EXISTS agent_convergence (
    agent_id VARCHAR(100) PRIMARY KEY,
    convergence_score FLOAT, -- 0-1, how stable the prompt is
    last_change_rounds_ago INTEGER DEFAULT 0,
    prompt_stability_score FLOAT,
    golden_prompt_candidate TEXT,
    ready_for_golden BOOLEAN DEFAULT FALSE,
    convergence_achieved_at TIMESTAMP,
    last_evaluated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Helper Functions

-- Function to calculate coaching effectiveness
CREATE OR REPLACE FUNCTION calculate_coaching_effectiveness(
    p_agent_id VARCHAR,
    p_window_size INTEGER DEFAULT 10
) RETURNS FLOAT AS $$
DECLARE
    effectiveness FLOAT;
BEGIN
    SELECT 
        AVG(improvement_delta) INTO effectiveness
    FROM (
        SELECT improvement_delta
        FROM coaching_performance
        WHERE agent_id = p_agent_id
        AND improvement_delta IS NOT NULL
        ORDER BY created_at DESC
        LIMIT p_window_size
    ) recent;
    
    RETURN COALESCE(effectiveness, 0);
END;
$$ LANGUAGE plpgsql;

-- Function to detect learning phase
CREATE OR REPLACE FUNCTION detect_learning_phase() RETURNS INTEGER AS $$
DECLARE
    pdf_count INTEGER;
BEGIN
    SELECT COUNT(DISTINCT doc_id) INTO pdf_count
    FROM coaching_performance;
    
    IF pdf_count <= 50 THEN
        RETURN 1; -- Exploration
    ELSIF pdf_count <= 150 THEN
        RETURN 2; -- Optimization
    ELSIF pdf_count <= 200 THEN
        RETURN 3; -- Convergence
    ELSE
        RETURN 4; -- Golden State
    END IF;
END;
$$ LANGUAGE plpgsql;

-- View for coaching dashboard
CREATE OR REPLACE VIEW coaching_dashboard AS
SELECT 
    a.agent_id,
    COUNT(DISTINCT cp.doc_id) as pdfs_processed,
    AVG(cp.accuracy) as avg_accuracy,
    MAX(cp.accuracy) as best_accuracy,
    AVG(cp.improvement_delta) as avg_improvement,
    COUNT(ge.id) as golden_examples,
    ac.convergence_score,
    ac.ready_for_golden,
    detect_learning_phase() as current_phase,
    calculate_coaching_effectiveness(a.agent_id) as effectiveness
FROM 
    agents a
    LEFT JOIN coaching_performance cp ON a.name = cp.agent_id
    LEFT JOIN golden_examples ge ON a.name = ge.agent_id AND ge.is_active = TRUE
    LEFT JOIN agent_convergence ac ON a.name = ac.agent_id
GROUP BY a.agent_id, a.name, ac.convergence_score, ac.ready_for_golden
ORDER BY avg_accuracy DESC;

-- Initial data insertion for tracking
INSERT INTO learning_metrics (phase, pdf_count, avg_accuracy, avg_coverage)
VALUES (1, 0, 0.0, 0.0)
ON CONFLICT DO NOTHING;