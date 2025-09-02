-- Golden Agent Registry Update for existing PostgreSQL schema
-- Generated: 2025-09-02

BEGIN;

-- Clear existing agents
TRUNCATE TABLE agent_registry CASCADE;

-- Insert governance_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'governance_agent',
    'Governance Agent',
    'Board, management, and organizational data',
    ARRAY['Förvaltningsberättelse', 'Styrelsen', 'Valberedning', 'Årsstämma'],
    ARRAY[3,4,5,6,7,8],
    'Extrahera styrelseinformation från denna svenska BRF årsredovisning. Sök efter: styrelseordförande, styrelseledamöter, suppleanter, revisor. ENDAST JSON.',
    '{"chairman": "", "board_members": [], "auditor_name": "", "audit_firm": "", "org_number": ""}'::jsonb,
    0.85
);

-- Insert income_statement_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'income_statement_agent',
    'Income Statement Agent',
    'Revenue, expenses, and net income',
    ARRAY['Resultaträkning', 'Rörelseintäkter', 'Rörelsekostnader'],
    ARRAY[9,10],
    'Extrahera resultaträkningsdata från denna svenska BRF årsredovisning. Sök efter: årsavgifter, hyresintäkter, driftskostnader. ENDAST JSON.',
    '{"annual_fees": 0, "rental_income": 0, "operating_costs": 0, "net_income": 0}'::jsonb,
    0.85
);

-- Insert balance_sheet_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'balance_sheet_agent',
    'Balance Sheet Agent',
    'Assets, liabilities, and equity',
    ARRAY['Balansräkning', 'TILLGÅNGAR', 'SKULDER', 'EGET KAPITAL'],
    ARRAY[11,12],
    'Extrahera balansräkningsdata från denna svenska BRF årsredovisning. Sök efter: byggnader och mark, kassa och bank, skulder. ENDAST JSON.',
    '{"buildings_and_land": 0, "cash_and_bank": 0, "total_assets": 0, "total_equity": 0, "long_term_debt": 0}'::jsonb,
    0.85
);

-- Insert cash_flow_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'cash_flow_agent',
    'Cash Flow Agent',
    'Cash flow statement analysis',
    ARRAY['Kassaflödesanalys', 'Kassaflöde'],
    ARRAY[13],
    'Extrahera kassaflödesanalys från denna svenska BRF årsredovisning. ENDAST JSON.',
    '{"operating_activities": 0, "investing_activities": 0, "financing_activities": 0}'::jsonb,
    0.85
);

-- Insert property_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'property_agent',
    'Property Agent',
    'Property information and details',
    ARRAY['Föreningens fastighet', 'Byggnader och mark', 'Fastighetsbeteckning'],
    ARRAY[5,6],
    'Extrahera fastighetsinformation från denna svenska BRF årsredovisning. ENDAST JSON.',
    '{"property_designation": "", "address": "", "construction_year": "", "apartments_count": 0}'::jsonb,
    0.85
);

-- Insert multi_year_overview_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'multi_year_overview_agent',
    'Multi-Year Overview Agent',
    '5-year financial overview',
    ARRAY['Flerårsöversikt', 'Femårsöversikt', 'Ekonomisk flerårsöversikt'],
    ARRAY[7,8],
    'Extrahera flerårsöversikt från denna svenska BRF årsredovisning. ENDAST JSON.',
    '{"years": [], "net_revenue": [], "net_result": [], "solidity_percent": []}'::jsonb,
    0.85
);

-- Insert maintenance_events_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'maintenance_events_agent',
    'Maintenance & Events Agent',
    'Projects and significant events',
    ARRAY['Väsentliga händelser', 'Genomförda projekt', 'Planerat underhåll'],
    ARRAY[6,7],
    'Extrahera underhåll och väsentliga händelser från denna svenska BRF årsredovisning. ENDAST JSON.',
    '{"completed_projects": [], "planned_maintenance": [], "significant_events": []}'::jsonb,
    0.85
);

-- Insert note_loans_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'note_loans_agent',
    'Note Loans Agent',
    'Loan details from notes',
    ARRAY['Skulder till kreditinstitut', 'Långfristiga skulder', 'Not Lån'],
    ARRAY[18,19],
    'Extrahera låneinformation från noterna. ENDAST JSON.',
    '{"loans": [], "total_loans": 0, "weighted_avg_rate": 0.0}'::jsonb,
    0.85
);

-- Insert note_depreciation_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'note_depreciation_agent',
    'Note Depreciation Agent',
    'Asset depreciation details',
    ARRAY['Byggnader och mark', 'Avskrivningar', 'Materiella anläggningstillgångar'],
    ARRAY[16,17],
    'Extrahera avskrivningsinformation från noterna. ENDAST JSON.',
    '{"buildings_acquisition_cost": 0, "accumulated_depreciation": 0, "year_depreciation": 0}'::jsonb,
    0.85
);

-- Insert note_costs_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'note_costs_agent',
    'Note Costs Agent',
    'Detailed cost breakdown',
    ARRAY['Driftskostnader', 'Not Kostnader', 'Specifikation av kostnader'],
    ARRAY[15,16],
    'Extrahera kostnadsspecifikation från noterna. ENDAST JSON.',
    '{"heating": 0, "electricity": 0, "cleaning": 0, "total_operating_costs": 0}'::jsonb,
    0.85
);

-- Insert note_revenue_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'note_revenue_agent',
    'Note Revenue Agent',
    'Detailed revenue breakdown',
    ARRAY['Nettoomsättning', 'Rörelseintäkter', 'Not Intäkter'],
    ARRAY[14,15],
    'Extrahera intäktsspecifikation från noterna. ENDAST JSON.',
    '{"annual_fees_residential": 0, "parking_income": 0, "other_income": 0}'::jsonb,
    0.85
);

-- Insert suppliers_vendors_agent (CRITICAL!)
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'suppliers_vendors_agent',
    'Suppliers & Vendors Agent',
    'CRITICAL - Supplier and vendor information (10% of docs)',
    ARRAY['Leverantörer', 'Leverantörsförteckning', 'Avtalspartners', 'Samarbetspartners', 'Tjänsteleverantörer'],
    ARRAY[28,29,30],
    'Extrahera leverantörsinformation. VIKTIGT: Endast 10% har detta men mycket värdefullt. Sök efter: leverantörer, banker, försäkring, energi, städ. ENDAST JSON.',
    '{"banking": [], "insurance": [], "utilities": [], "property_services": [], "management": []}'::jsonb,
    0.80
);

-- Insert audit_report_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'audit_report_agent',
    'Audit Report Agent',
    'Audit opinions and findings',
    ARRAY['Revisionsberättelse', 'Revisorns rapport', 'Uttalanden'],
    ARRAY[21,22,23],
    'Extrahera revisionsberättelse från denna svenska BRF årsredovisning. ENDAST JSON.',
    '{"opinion": "", "recommends_approval": true, "auditor_name": "", "audit_firm": ""}'::jsonb,
    0.85
);

-- Insert ratio_kpi_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'ratio_kpi_agent',
    'Ratio & KPI Agent',
    'Financial ratios and key metrics',
    ARRAY['Nyckeltal', 'Ekonomisk ställning', 'Ekonomiska nyckeltal'],
    ARRAY[7,8],
    'Extrahera eller beräkna nyckeltal från denna svenska BRF årsredovisning. ENDAST JSON.',
    '{"solidity_percent": 0.0, "debt_per_sqm": 0, "annual_fee_per_sqm": 0}'::jsonb,
    0.85
);

-- Insert member_info_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'member_info_agent',
    'Member Info Agent',
    'Member statistics and transfers',
    ARRAY['Medlemsinformation', 'Antal medlemmar', 'Överlåtelser'],
    ARRAY[5,6],
    'Extrahera medlemsinformation från denna svenska BRF årsredovisning. ENDAST JSON.',
    '{"total_members": 0, "apartments_count": 0, "transfers_during_year": 0}'::jsonb,
    0.85
);

-- Insert pledged_assets_agent
INSERT INTO agent_registry (agent_id, name, specialization, typical_sections, typical_pages, bounded_prompt, output_schema, confidence_threshold)
VALUES (
    'pledged_assets_agent',
    'Pledged Assets Agent',
    'Securities and guarantees',
    ARRAY['Ställda säkerheter', 'Eventualförpliktelser', 'Ansvarsförbindelser'],
    ARRAY[19,20],
    'Extrahera ställda säkerheter från noterna. ENDAST JSON.',
    '{"total_mortgages": 0, "pledged_to_banks": 0, "contingent_liabilities": ""}'::jsonb,
    0.85
);

COMMIT;

-- Verify insertion
SELECT COUNT(*) as agent_count FROM agent_registry;
SELECT agent_id, name, specialization FROM agent_registry ORDER BY agent_id;