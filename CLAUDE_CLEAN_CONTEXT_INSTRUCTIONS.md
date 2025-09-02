# 📋 CLAUDE INSTRUCTIONS - CLEAN CONTEXT

Dear Claude, we have built a complete **Golden Orchestrator Pipeline** for Swedish BRF annual reports.

## 🎯 YOUR IMMEDIATE TASK

```bash
# Navigate to the Golden directory
cd /tmp/Golden_Orchestrator_Pipeline  # or /private/tmp/Golden_Orchestrator_Pipeline

# Verify structure
ls -la

# Run the complete test
python3 run_golden_pipeline.py
```

## 📁 SELF-CONTAINED GOLDEN STRUCTURE

```
Golden_Orchestrator_Pipeline/
├── sectionizer/
│   ├── golden_sectionizer.py         # Enhanced with suppliers detection
│   └── golden_two_pass_sectionizer.py
├── orchestrator/
│   └── golden_orchestrator.py        # Intelligent learning orchestrator
├── agents/
│   └── golden_agents.py              # 16 essential agents
├── tests/
│   └── golden_mega_test.py           # Comprehensive test suite
├── docs/
│   └── COMPLETE_SYSTEM.md            # Full documentation
└── run_golden_pipeline.py            # MAIN ENTRY POINT
```

## ✅ WHAT THIS SYSTEM DOES

### 16 Essential Agents (NO signature, ToC, legal, summary)
1. **Core Financial** (P1): governance, income_statement, balance_sheet, cash_flow
2. **Property & Details** (P2): property, multi_year, maintenance, notes
3. **SUPPLIERS** (P2) ⭐: leverantörer/vendors - CRITICAL for 10% of docs
4. **Analysis** (P3): audit, ratios, member_info, pledged_assets

### Key Features
- **Enhanced Sectionizer**: 29 patterns including 8 supplier patterns
- **Learning System**: Improves autonomously from failures
- **Validation**: Cross-checks between agents
- **H100 Optimized**: Max 4 agents parallel (memory constraint)
- **Extraction Zones**: Each agent only sees its pages (80% faster)

## 🧪 EXPECTED TEST RESULTS

The test runs 6 sections - ALL should PASS:

1. **SECTIONIZER** - Finds suppliers/leverantörer ✅
2. **MAPPING_LOGIC** - Correct agent assignments ✅
3. **LEARNING_SYSTEM** - Generates improvements ✅
4. **VALIDATION** - Data quality checks ✅
5. **EXECUTION_PLANNING** - 4 batches, max 4 agents ✅
6. **INTEGRATION** - Full pipeline test ✅

## 📊 CHECK RESULTS

```bash
# While running
tail -f /tmp/Golden_Orchestrator_Pipeline/orchestrator_test.log

# When complete
cat /tmp/Golden_Orchestrator_Pipeline/orchestrator_test_results.json | python3 -m json.tool | grep -A10 summary
```

Success looks like:
```json
"summary": {
    "total_tests": 6,
    "passed": 6,
    "failed": 0,
    "success": true
}
```

## ⚠️ CRITICAL REMINDERS

1. **Suppliers = GOLD**: Only 10% have leverantörer but extremely valuable
2. **Max 4 Parallel**: H100 memory constraint must be respected
3. **Git Initialized**: Already has git with initial commit
4. **Self-Contained**: All imports are relative, no external dependencies

## 🚀 PRODUCTION READY

When all 6 tests pass, the Golden Pipeline is ready for:
- Processing 30,000 Swedish BRF documents
- Extracting suppliers (banks, insurance, utilities)
- Learning from failures autonomously
- Validating data quality

---

**Start with: `cd /tmp/Golden_Orchestrator_Pipeline && python3 run_golden_pipeline.py`**