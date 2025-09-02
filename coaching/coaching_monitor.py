#!/usr/bin/env python3
"""
Real-time monitoring dashboard for Card G4 Reinforced Learning
Shows coaching progress, accuracy trends, and agent performance
"""

import os
import sys
import psycopg2
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

def get_database_connection():
    """Get connection to PostgreSQL database"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '5432')),
        database=os.getenv('DB_NAME', 'zelda_arsredovisning'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'h100pass')
    )

def get_learning_phase(conn) -> Tuple[int, str]:
    """Get current learning phase"""
    with conn.cursor() as cur:
        cur.execute("SELECT detect_learning_phase()")
        phase = cur.fetchone()[0]
        
    phase_names = {
        1: "Exploration (1-50 PDFs)",
        2: "Optimization (51-150 PDFs)",
        3: "Convergence (151-200 PDFs)",
        4: "Golden State (201+ PDFs)"
    }
    
    return phase, phase_names.get(phase, "Unknown")

def get_overall_metrics(conn) -> Dict:
    """Get overall coaching metrics"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                COUNT(DISTINCT doc_id) as total_pdfs,
                COUNT(DISTINCT agent_id) as total_agents,
                AVG(accuracy) as avg_accuracy,
                MAX(accuracy) as best_accuracy,
                AVG(improvement_delta) as avg_improvement,
                COUNT(*) as total_coaching_sessions
            FROM coaching_performance
        """)
        
        row = cur.fetchone()
        return {
            'total_pdfs': row[0] or 0,
            'total_agents': row[1] or 0,
            'avg_accuracy': row[2] or 0.0,
            'best_accuracy': row[3] or 0.0,
            'avg_improvement': row[4] or 0.0,
            'total_sessions': row[5] or 0
        }

def get_agent_performance(conn) -> List[Dict]:
    """Get performance by agent"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                agent_id,
                COUNT(DISTINCT doc_id) as pdfs_processed,
                AVG(accuracy) as avg_accuracy,
                MAX(accuracy) as best_accuracy,
                AVG(improvement_delta) as avg_improvement,
                COUNT(CASE WHEN improvement_delta > 0 THEN 1 END) as improved_count,
                COUNT(*) as total_rounds
            FROM coaching_performance
            GROUP BY agent_id
            ORDER BY avg_accuracy DESC
            LIMIT 10
        """)
        
        agents = []
        for row in cur.fetchall():
            agents.append({
                'agent': row[0],
                'pdfs': row[1],
                'avg_acc': row[2] or 0.0,
                'best_acc': row[3] or 0.0,
                'avg_imp': row[4] or 0.0,
                'improved': row[5],
                'rounds': row[6]
            })
        
        return agents

def get_recent_sessions(conn, limit: int = 5) -> List[Dict]:
    """Get recent coaching sessions"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                session_id,
                agent_id,
                initial_accuracy,
                final_accuracy,
                total_improvement,
                rounds_completed,
                status,
                created_at
            FROM coaching_sessions
            ORDER BY created_at DESC
            LIMIT %s
        """, (limit,))
        
        sessions = []
        for row in cur.fetchall():
            sessions.append({
                'session': row[0][:20] + '...' if len(row[0]) > 20 else row[0],
                'agent': row[1],
                'initial': row[2] or 0.0,
                'final': row[3] or 0.0,
                'improvement': row[4] or 0.0,
                'rounds': row[5] or 0,
                'status': row[6],
                'time': row[7].strftime('%H:%M:%S') if row[7] else 'N/A'
            })
        
        return sessions

def get_golden_examples_count(conn) -> Dict:
    """Get golden examples statistics"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(DISTINCT agent_id) as agents_with_golden,
                AVG(accuracy_score) as avg_golden_accuracy
            FROM golden_examples
            WHERE is_active = TRUE
        """)
        
        row = cur.fetchone()
        return {
            'total': row[0] or 0,
            'agents': row[1] or 0,
            'avg_accuracy': row[2] or 0.0
        }

def get_convergence_status(conn) -> List[Dict]:
    """Get agent convergence status"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                agent_id,
                convergence_score,
                ready_for_golden,
                last_change_rounds_ago
            FROM agent_convergence
            WHERE convergence_score IS NOT NULL
            ORDER BY convergence_score DESC
            LIMIT 5
        """)
        
        agents = []
        for row in cur.fetchall():
            agents.append({
                'agent': row[0],
                'convergence': row[1] or 0.0,
                'ready': row[2],
                'stable_for': row[3] or 0
            })
        
        return agents

def display_dashboard(conn):
    """Display comprehensive coaching dashboard"""
    # Clear screen (works on Unix-like systems)
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Get all metrics
    phase, phase_name = get_learning_phase(conn)
    overall = get_overall_metrics(conn)
    agents = get_agent_performance(conn)
    sessions = get_recent_sessions(conn)
    golden = get_golden_examples_count(conn)
    convergence = get_convergence_status(conn)
    
    # Header
    print("=" * 80)
    print("🎮 CARD G4 REINFORCED LEARNING MONITOR".center(80))
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(80))
    print("=" * 80)
    
    # Learning Phase
    print(f"\n📊 LEARNING PHASE: {phase_name}")
    progress = min(overall['total_pdfs'] / 200, 1.0)
    bar_length = 50
    filled = int(bar_length * progress)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"Progress: [{bar}] {overall['total_pdfs']}/200 PDFs")
    
    # Overall Metrics
    print(f"\n📈 OVERALL METRICS")
    print(f"  Average Accuracy:    {overall['avg_accuracy']:.2%}")
    print(f"  Best Accuracy:       {overall['best_accuracy']:.2%}")
    print(f"  Avg Improvement:     {overall['avg_improvement']:+.2%}")
    print(f"  Total Sessions:      {overall['total_sessions']}")
    print(f"  Golden Examples:     {golden['total']} ({golden['agents']} agents)")
    
    # Target Status
    target_acc = {1: 0.80, 2: 0.90, 3: 0.95, 4: 0.95}.get(phase, 0.95)
    if overall['avg_accuracy'] >= target_acc:
        print(f"\n  🎯 PHASE TARGET ACHIEVED! ({target_acc:.0%})")
    else:
        gap = target_acc - overall['avg_accuracy']
        print(f"\n  📊 Gap to target: {gap:.2%} (Target: {target_acc:.0%})")
    
    # Agent Performance
    print(f"\n🤖 TOP AGENTS BY ACCURACY")
    print(f"  {'Agent':<30} {'PDFs':>6} {'Avg':>8} {'Best':>8} {'Improved':>10}")
    print(f"  {'-'*30} {'-'*6} {'-'*8} {'-'*8} {'-'*10}")
    
    for agent in agents[:5]:
        improved_pct = agent['improved'] / agent['rounds'] * 100 if agent['rounds'] > 0 else 0
        print(f"  {agent['agent']:<30} {agent['pdfs']:>6} {agent['avg_acc']:>7.2%} {agent['best_acc']:>7.2%} {improved_pct:>9.1f}%")
    
    # Recent Sessions
    print(f"\n🔄 RECENT COACHING SESSIONS")
    print(f"  {'Time':<10} {'Agent':<25} {'Initial':>8} {'Final':>8} {'Delta':>8} {'Status':<10}")
    print(f"  {'-'*10} {'-'*25} {'-'*8} {'-'*8} {'-'*8} {'-'*10}")
    
    for session in sessions:
        status_icon = '✅' if session['status'] == 'completed' else '❌' if session['status'] == 'failed' else '🔄'
        print(f"  {session['time']:<10} {session['agent']:<25} {session['initial']:>7.2%} {session['final']:>7.2%} {session['improvement']:>+7.2%} {status_icon} {session['status']:<8}")
    
    # Convergence Status
    if convergence:
        print(f"\n🎯 CONVERGENCE STATUS")
        print(f"  {'Agent':<30} {'Score':>10} {'Stable':>10} {'Ready':>8}")
        print(f"  {'-'*30} {'-'*10} {'-'*10} {'-'*8}")
        
        for agent in convergence:
            ready = '✅' if agent['ready'] else '⏳'
            print(f"  {agent['agent']:<30} {agent['convergence']:>9.2f} {agent['stable_for']:>9}r {ready:>8}")
    
    # Footer
    print("\n" + "=" * 80)
    print("Press Ctrl+C to exit | Updates every 10 seconds")

def main():
    """Main monitoring loop"""
    try:
        conn = get_database_connection()
        
        while True:
            try:
                display_dashboard(conn)
                time.sleep(10)  # Update every 10 seconds
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                time.sleep(5)
        
        conn.close()
        print("\n👋 Monitor stopped")
        
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        print("\nMake sure PostgreSQL is running and coaching tables are created")
        print("Run: psql -f create_coaching_schema.sql")

if __name__ == "__main__":
    import time
    main()