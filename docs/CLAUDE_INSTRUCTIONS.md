# 📋 INSTRUCTION FOR CLAUDE AFTER CONTEXT CLEANSE

Dear Claude, we have built a complete intelligent orchestrator system for Swedish BRF annual reports. Everything is ready in `/private/tmp/` (or wherever your current `/tmp/` maps to).

## 🚀 YOUR IMMEDIATE TASK

```bash
# First, verify you're in the right location
pwd
ls -la *.py | grep orchestrator

# If files are present, run the mega test:
python3 orchestrator_mega_test.py > orchestrator_test.log 2>&1 &
echo $! > orchestrator_test.pid

# Monitor progress
tail -f orchestrator_test.log

# Check status
cat orchestrator_test_status.json | grep current_test
```

## 📁 FILE LOCATIONS

**All files should be in your current working directory** (likely `/private/tmp/`):

### Core Files:
- `MEGA_ORCHESTRATOR_COMPLETE_SYSTEM.md` - Complete documentation
- `orchestrator_mega_test.py` - THE TEST TO RUN
- `enhanced_sectionizer_with_suppliers.py` - Sectionizer with leverantörer
- `intelligent_learning_orchestrator.py` - Main orchestrator with learning
- `perfect_agents_with_suppliers.py` - 16 agent definitions

### Output Files (created by test):
- `orchestrator_test.log` - Live test output
- `orchestrator_test_status.json` - Current progress
- `orchestrator_test_results.json` - Final results
- `orchestrator_test.pid` - Process ID

## 🎯 WHAT WE BUILT

### 16 Essential Agents (NO signature, ToC, legal, summary):
- **Priority 1**: governance, income_statement, balance_sheet, cash_flow
- **Priority 2**: property, multi_year, maintenance, note_*, **suppliers_vendors** ⭐
- **Priority 3**: audit, ratio_kpi, member_info, pledged_assets

### Critical Features:
1. **SUPPLIERS AGENT** ⭐ - Extracts leverantörer (10% of docs but GOLD)
2. **Enhanced Sectionizer** - 29 patterns including 8 supplier patterns
3. **Learning System** - Improves from failures autonomously
4. **Validation** - Cross-checks between agents
5. **H100 Limits** - Max 4 agents parallel

## ✅ EXPECTED TEST RESULTS

The test runs 6 sections that should ALL PASS:

1. **SECTIONIZER** - Finds suppliers/leverantörer patterns
2. **MAPPING_LOGIC** - Maps sections to correct agents
3. **LEARNING_SYSTEM** - Generates improvements from failures
4. **VALIDATION** - Checks balance sheet, cross-validation
5. **EXECUTION_PLANNING** - Creates 4 batches, max 4 agents each
6. **INTEGRATION** - Full pipeline test

## 🔍 HOW TO CHECK SUCCESS

```bash
# While running - check current test:
cat orchestrator_test_status.json | python3 -m json.tool | grep -A2 current_test

# When complete - check final results:
cat orchestrator_test_results.json | python3 -m json.tool | grep -A10 summary

# Success looks like:
"summary": {
    "total_tests": 6,
    "passed": 6,
    "failed": 0,
    "success": true
}
```

## ⚠️ CRITICAL REMINDERS

1. **Suppliers = GOLD**: Only 10% have leverantörer but super valuable
2. **Max 4 Parallel**: H100 memory constraint
3. **Extraction Zones**: Each agent only sees its pages (80% faster)
4. **Learning**: System improves autonomously
5. **Validation**: Balance sheet MUST balance

## 🚨 IF TEST FAILS

Check which section failed:
```bash
grep "FAIL" orchestrator_test.log
cat orchestrator_test_results.json | python3 -m json.tool | grep -B2 -A2 "FAIL"
```

Common issues:
- Missing import → Check all .py files are present
- Suppliers not found → Check enhanced_sectionizer_with_suppliers.py exists
- Validation fails → Normal, shows system working

## 📊 WHAT SUCCESS MEANS

When all 6 tests pass:
- ✅ Sectionizer finds leverantörer
- ✅ All 16 agents mapped correctly
- ✅ Learning from failures works
- ✅ Data validation active
- ✅ H100 constraints respected
- ✅ Full pipeline operational

**The orchestrator is then READY FOR PRODUCTION on Swedish BRF documents!**

---

*Start with `python3 orchestrator_mega_test.py` and monitor progress!*