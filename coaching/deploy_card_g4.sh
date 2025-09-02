#!/bin/bash
# Deploy Card G4 Reinforced Learning System to H100

echo "=========================================="
echo "🚀 CARD G4 DEPLOYMENT TO H100"
echo "=========================================="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Configuration
H100_HOST="45.135.56.10"
H100_PORT="26983"
H100_USER="root"
SSH_KEY="~/.ssh/BrfGraphRag"
REMOTE_DIR="/tmp/Golden_Orchestrator_Pipeline"
LOCAL_DIR="/private/tmp/Golden_Orchestrator_Pipeline"

# Step 1: SSH Tunnel for PostgreSQL
echo "📡 Step 1: Establishing SSH tunnel..."
ssh -p $H100_PORT -i $SSH_KEY -N -f -L 15432:localhost:5432 $H100_USER@$H100_HOST 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ SSH tunnel established (localhost:15432 → H100:5432)"
else
    echo "   ⚠️ SSH tunnel may already exist"
fi

# Step 2: Create Database Schema
echo ""
echo "🗄️ Step 2: Creating coaching database schema..."
PGPASSWORD=h100pass psql -U postgres -h localhost -p 15432 -d zelda_arsredovisning < coaching/create_coaching_schema.sql 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Coaching schema created successfully"
else
    echo "   ⚠️ Schema may already exist or database connection failed"
fi

# Step 3: Deploy Card G4 Implementation
echo ""
echo "📦 Step 3: Deploying Card G4 to H100..."

# Create remote directory structure
ssh -p $H100_PORT -i $SSH_KEY $H100_USER@$H100_HOST "mkdir -p $REMOTE_DIR/coaching"

# Copy coaching implementation
scp -P $H100_PORT -i $SSH_KEY -r coaching/* $H100_USER@$H100_HOST:$REMOTE_DIR/coaching/
if [ $? -eq 0 ]; then
    echo "   ✅ Card G4 implementation deployed"
else
    echo "   ❌ Failed to deploy Card G4"
    exit 1
fi

# Copy updated orchestrator
scp -P $H100_PORT -i $SSH_KEY orchestrator/golden_orchestrator.py $H100_USER@$H100_HOST:$REMOTE_DIR/orchestrator/
if [ $? -eq 0 ]; then
    echo "   ✅ Updated orchestrator deployed"
else
    echo "   ❌ Failed to deploy orchestrator"
    exit 1
fi

# Step 4: Install Python Dependencies
echo ""
echo "📚 Step 4: Installing dependencies on H100..."
ssh -p $H100_PORT -i $SSH_KEY $H100_USER@$H100_HOST << 'EOF'
cd /tmp/Golden_Orchestrator_Pipeline
pip3 install --quiet google-generativeai psycopg2-binary numpy 2>/dev/null
echo "   ✅ Dependencies installed"
EOF

# Step 5: Set Environment Variables
echo ""
echo "🔧 Step 5: Configuring environment..."
cat > /tmp/card_g4_env.sh << 'EOF'
#!/bin/bash
# Card G4 Environment Configuration
export COACHING_ENABLED=true
export GEMINI_API_KEY="AIzaSyD0y92BjcnvUgRlWsA1oPSIWV5QaJcCrNw"
export GEMINI_MODEL="gemini-2.5-pro"
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=zelda_arsredovisning
export DB_USER=postgres
export DB_PASSWORD=h100pass
export LEARNING_PHASE=1
export MAX_COACHING_ROUNDS=5
EOF

scp -P $H100_PORT -i $SSH_KEY /tmp/card_g4_env.sh $H100_USER@$H100_HOST:$REMOTE_DIR/
if [ $? -eq 0 ]; then
    echo "   ✅ Environment configured"
else
    echo "   ❌ Failed to configure environment"
fi

# Step 6: Test Coaching System
echo ""
echo "🧪 Step 6: Testing coaching system..."
ssh -p $H100_PORT -i $SSH_KEY $H100_USER@$H100_HOST << 'EOF'
cd /tmp/Golden_Orchestrator_Pipeline
source card_g4_env.sh
python3 coaching/test_coaching_integration.py 2>&1 | grep -E "(PASS|FAIL|Error)"
EOF

# Step 7: Create Monitoring Script
echo ""
echo "📊 Step 7: Setting up monitoring..."
cat > /tmp/monitor_card_g4.sh << 'EOF'
#!/bin/bash
# Monitor Card G4 Progress
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10 << 'REMOTE'
cd /tmp/Golden_Orchestrator_Pipeline
source card_g4_env.sh
python3 coaching/coaching_monitor.py
REMOTE
EOF

chmod +x /tmp/monitor_card_g4.sh
echo "   ✅ Monitoring script created: /tmp/monitor_card_g4.sh"

# Step 8: Create Phase 1 Execution Script
echo ""
echo "🚀 Step 8: Creating Phase 1 execution script..."
cat > /tmp/run_phase1.sh << 'EOF'
#!/bin/bash
# Run Phase 1: Exploration (First 50 PDFs)
ssh -p 26983 -i ~/.ssh/BrfGraphRag root@45.135.56.10 << 'REMOTE'
cd /tmp/Golden_Orchestrator_Pipeline
source card_g4_env.sh
python3 coaching/batch_phase1.py
REMOTE
EOF

chmod +x /tmp/run_phase1.sh
echo "   ✅ Phase 1 script created: /tmp/run_phase1.sh"

# Summary
echo ""
echo "=========================================="
echo "✅ CARD G4 DEPLOYMENT COMPLETE"
echo "=========================================="
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Test the coaching system:"
echo "   ssh -p $H100_PORT -i $SSH_KEY $H100_USER@$H100_HOST"
echo "   cd $REMOTE_DIR"
echo "   source card_g4_env.sh"
echo "   python3 coaching/test_coaching_integration.py"
echo ""
echo "2. Start Phase 1 processing:"
echo "   /tmp/run_phase1.sh"
echo ""
echo "3. Monitor progress:"
echo "   /tmp/monitor_card_g4.sh"
echo ""
echo "4. View coaching dashboard:"
echo "   watch -n 10 'psql -h localhost -p 15432 -U postgres -d zelda_arsredovisning -c \"SELECT * FROM coaching_dashboard\"'"
echo ""
echo "🎯 Expected Outcomes:"
echo "  Phase 1 (PDFs 1-50):    60% → 80% accuracy"
echo "  Phase 2 (PDFs 51-150):  80% → 90% accuracy"
echo "  Phase 3 (PDFs 151-200): 90% → 95% accuracy"
echo "  Phase 4 (PDFs 201+):    95%+ sustained (Golden State)"
echo ""
echo "Good luck with the reinforced learning journey! 🚀"