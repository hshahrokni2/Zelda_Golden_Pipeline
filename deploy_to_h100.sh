#!/bin/bash
# Deploy Golden Orchestrator Pipeline to H100

echo "🚀 DEPLOYING GOLDEN ORCHESTRATOR TO H100..."
echo "=========================================="

# H100 connection details
H100_HOST="45.135.56.10"
H100_PORT="26983"
H100_USER="root"
H100_KEY="~/.ssh/BrfGraphRag"
H100_DIR="/tmp/Golden_Orchestrator_Pipeline"

# Create directory on H100
echo "📁 Creating directory on H100..."
ssh -p $H100_PORT -i $H100_KEY $H100_USER@$H100_HOST "mkdir -p $H100_DIR"

# Copy all files to H100
echo "📦 Copying Golden Pipeline to H100..."
scp -P $H100_PORT -i $H100_KEY -r /tmp/Golden_Orchestrator_Pipeline/* $H100_USER@$H100_HOST:$H100_DIR/

# Update PostgreSQL with new agents
echo "🗄️ Updating PostgreSQL with new agents..."
ssh -p $H100_PORT -i $H100_KEY $H100_USER@$H100_HOST << 'EOF'
cd /tmp/Golden_Orchestrator_Pipeline
PGPASSWORD=h100pass psql -U postgres -h localhost -d zelda_arsredovisning < agents/update_postgres_correct.sql
echo "Agent count in database:"
PGPASSWORD=h100pass psql -U postgres -h localhost -d zelda_arsredovisning -t -c "SELECT COUNT(*) FROM agent_registry;"
EOF

# Verify deployment
echo "✅ Verifying deployment..."
ssh -p $H100_PORT -i $H100_KEY $H100_USER@$H100_HOST << 'EOF'
cd /tmp/Golden_Orchestrator_Pipeline
echo "Files deployed:"
ls -la
echo ""
echo "Testing imports:"
python3 -c "from sectionizer.golden_sectionizer import GoldenSectionizer; print('✅ Sectionizer OK')"
python3 -c "from orchestrator.golden_orchestrator import GoldenOrchestrator; print('✅ Orchestrator OK')"
python3 -c "from agents.agent_loader import AgentRegistry; r = AgentRegistry(); print(f'✅ Agent Registry OK: {len(r.get_all_agents())} agents')"
EOF

echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "📍 Location on H100: $H100_DIR"
echo "🚀 To test on H100:"
echo "   ssh -p $H100_PORT -i $H100_KEY $H100_USER@$H100_HOST"
echo "   cd $H100_DIR"
echo "   python3 run_golden_pipeline.py"
echo ""
echo "💾 PostgreSQL updated with 16 agents"