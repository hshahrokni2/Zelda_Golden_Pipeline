-- Golden Agent Registry Update
-- Generated: 2025-09-02T12:22:18.920616

BEGIN;

-- Clear existing agents
TRUNCATE TABLE agent_registry CASCADE;


INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'governance_agent',
    1,
    ARRAY['Förvaltningsberättelse', 'Styrelsen', 'Valberedning', 'Årsstämma'],
    'Extracts board, management, and organizational data',
    'Extrahera styrelseinformation från denna svenska BRF årsredovisning.
Sök efter: styrelseordförande, styrelseledamöter, suppleanter, kassör, sekreterare, valberedning, revisor, revisionsbolag.
Identifiera alla namn på personer och deras roller. Notera valperioder och mandattider.

ENDAST JSON - Respond ONLY with this structure:
{
  "chairman": "namn på ordförande",
  "board_members": [
    {"name": "fullständigt namn", "role": "Ledamot/Suppleant/Kassör/Sekreterare", "elected": "YYYY"}
  ],
  "auditor_name": "revisorns namn",
  "audit_firm": "revisionsbolag (Grant Thornton/PwC/KPMG/Ernst & Young/BDO)",
  "nomination_committee": ["namn1", "namn2"],
  "org_number": "NNNNNN-NNNN",
  "association_name": "Brf fullständiga namn"
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'income_statement_agent',
    1,
    ARRAY['Resultaträkning', 'Rörelseintäkter', 'Rörelsekostnader'],
    'Extracts income statement and financial metrics',
    'Extrahera resultaträkningsdata från denna svenska BRF årsredovisning.
Sök efter: nettoomsättning, årsavgifter, hyresintäkter, parkering, driftskostnader, reparation och underhåll,
förvaltningskostnader, personalkostnader, avskrivningar, räntekostnader, ränteintäkter, årets resultat.
Använd aktuellt års siffror (högra kolumnen). Alla belopp i SEK utan mellanslag.

ENDAST JSON - Respond ONLY with this structure:
{
  "annual_fees": 0,
  "rental_income": 0,
  "parking_income": 0,
  "other_income": 0,
  "total_revenues": 0,
  "operating_costs": 0,
  "maintenance_costs": 0,
  "management_costs": 0,
  "personnel_costs": 0,
  "depreciation": 0,
  "interest_expense": 0,
  "interest_income": 0,
  "net_income": 0,
  "year": "YYYY"
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'balance_sheet_agent',
    1,
    ARRAY['Balansräkning', 'TILLGÅNGAR', 'SKULDER', 'EGET KAPITAL'],
    'Extracts balance sheet items and ratios',
    'Extrahera balansräkningsdata från denna svenska BRF årsredovisning.
Sök efter: anläggningstillgångar, byggnader och mark, omsättningstillgångar, kassa och bank,
eget kapital, medlemsinsatser, upplåtelseavgifter, fond för yttre underhåll, balanserat resultat,
långfristiga skulder, kortfristiga skulder, leverantörsskulder.
Alla belopp i SEK. Summa tillgångar MÅSTE vara lika med summa eget kapital och skulder.

ENDAST JSON - Respond ONLY with this structure:
{
  "buildings_and_land": 0,
  "equipment": 0,
  "cash_and_bank": 0,
  "other_current_assets": 0,
  "total_assets": 0,
  "member_deposits": 0,
  "share_capital": 0,
  "maintenance_fund": 0,
  "retained_earnings": 0,
  "year_result": 0,
  "total_equity": 0,
  "long_term_debt": 0,
  "short_term_debt": 0,
  "total_liabilities": 0,
  "balance_date": "YYYY-MM-DD"
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'cash_flow_agent',
    1,
    ARRAY['Kassaflödesanalys', 'Kassaflöde'],
    'Extracts cash flow statement data',
    'Extrahera kassaflödesanalys från denna svenska BRF årsredovisning.
Sök efter: den löpande verksamheten, investeringsverksamheten, finansieringsverksamheten,
årets kassaflöde, likvida medel vid årets början/slut, avskrivningar, förändringar i rörelsekapital,
investeringar, upptagna lån, amorteringar.

ENDAST JSON - Respond ONLY with this structure:
{
  "operating_activities": 0,
  "investing_activities": 0,
  "financing_activities": 0,
  "total_cash_flow": 0,
  "opening_cash": 0,
  "closing_cash": 0
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'property_agent',
    2,
    ARRAY['Föreningens fastighet', 'Byggnader och mark', 'Fastighetsbeteckning'],
    'Extracts property-specific information',
    'Extrahera fastighetsinformation från denna svenska BRF årsredovisning.
Sök efter: fastighetsbeteckning, adress, kommun, byggår, tomtareal, bostadsyta, lokalyta,
antal lägenheter, antal lokaler, antal garage, parkeringsplatser, försäkringsbolag, försäkringstyp.

ENDAST JSON - Respond ONLY with this structure:
{
  "property_designation": "fastighetsbeteckning",
  "address": "gatuadress",
  "municipality": "kommun",
  "construction_year": "YYYY",
  "land_area_sqm": 0,
  "residential_area_sqm": 0,
  "commercial_area_sqm": 0,
  "apartments_count": 0,
  "commercial_units": 0,
  "parking_spaces": 0,
  "insurance_company": "försäkringsbolag",
  "insurance_type": "Fullvärde/Fastighetsförsäkring"
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'multi_year_overview_agent',
    2,
    ARRAY['Flerårsöversikt', 'Femårsöversikt', 'Ekonomisk flerårsöversikt'],
    'Specialized agent for 5-year overview tables',
    'Extrahera flerårsöversikt (5-års tabell) från denna svenska BRF årsredovisning.
Sök efter tabell med: nettoomsättning, rörelseresultat, årets resultat, balansomslutning, soliditet,
belåning kr/kvm, årsavgift kr/kvm, driftskostnad kr/kvm, likviditet.
Extrahera ALLA tillgängliga år (typiskt 5 år).

ENDAST JSON - Respond ONLY with arrays där varje index motsvarar samma år:
{
  "years": ["2024", "2023", "2022", "2021", "2020"],
  "net_revenue": [0, 0, 0, 0, 0],
  "operating_result": [0, 0, 0, 0, 0],
  "net_result": [0, 0, 0, 0, 0],
  "total_assets": [0, 0, 0, 0, 0],
  "solidity_percent": [0, 0, 0, 0, 0],
  "debt_per_sqm": [0, 0, 0, 0, 0],
  "annual_fee_per_sqm": [0, 0, 0, 0, 0]
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'maintenance_events_agent',
    2,
    ARRAY['Väsentliga händelser', 'Genomförda projekt', 'Planerat underhåll', 'Underhållsplan'],
    'Extracts significant events and projects',
    'Extrahera underhåll och väsentliga händelser från denna svenska BRF årsredovisning.
Sök efter: genomförda projekt, planerat underhåll, större reparationer, stambyte, takbyte, fasadrenovering,
fönsterbyte, hissrenovering, tvättstuga, efter räkenskapsårets utgång.

ENDAST JSON - Respond ONLY with this structure:
{
  "completed_projects": [
    {"description": "projektbeskrivning", "cost": 0, "year": "YYYY"}
  ],
  "planned_maintenance": [
    {"description": "planerat arbete", "estimated_cost": 0, "planned_year": "YYYY"}
  ],
  "significant_events": [
    {"event": "händelsebeskrivning", "date": "YYYY-MM", "impact": "påverkan"}
  ],
  "maintenance_fund_allocation": 0
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'note_loans_agent',
    2,
    ARRAY['Skulder till kreditinstitut', 'Långfristiga skulder', 'Not.*Lån'],
    'Extracts detailed loan information from notes',
    'Extrahera låneinformation från noterna i denna svenska BRF årsredovisning.
Sök efter: långivare (Swedbank, Handelsbanken, SEB, Nordea, SBAB, Danske Bank), lånenummer,
räntesats, räntebindning, förfallodag, amortering, räntetak/swap.

ENDAST JSON - Respond ONLY with this structure:
{
  "loans": [
    {
      "lender": "bank",
      "loan_number": "lånenummer",
      "balance": 0,
      "interest_rate": 0.0,
      "rate_type": "Rörlig/Fast",
      "maturity": "YYYY-MM-DD",
      "next_rate_adjustment": "YYYY-MM-DD",
      "amortization": 0
    }
  ],
  "total_loans": 0,
  "weighted_avg_rate": 0.0,
  "within_one_year": 0,
  "after_five_years": 0
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'note_depreciation_agent',
    2,
    ARRAY['Byggnader och mark', 'Avskrivningar', 'Materiella anläggningstillgångar'],
    'Extracts asset and depreciation details from notes',
    'Extrahera avskrivningsinformation från noterna.
Sök efter: anskaffningsvärde, ackumulerade avskrivningar, årets avskrivning, bokfört värde,
taxeringsvärde byggnader, taxeringsvärde mark, avskrivningsprinciper.

ENDAST JSON - Respond ONLY with this structure:
{
  "buildings_acquisition_cost": 0,
  "land_acquisition_cost": 0,
  "accumulated_depreciation": 0,
  "year_depreciation": 0,
  "buildings_book_value": 0,
  "land_book_value": 0,
  "buildings_tax_value": 0,
  "land_tax_value": 0,
  "depreciation_rate_percent": 0.0
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'note_costs_agent',
    2,
    ARRAY['Driftskostnader', 'Not.*Kostnader', 'Specifikation av kostnader'],
    'Extracts detailed cost breakdown from notes',
    'Extrahera kostnadsspecifikation från noterna.
Sök efter detaljerade kostnader: värme, el, vatten och avlopp, sophämtning, städning, snöröjning,
försäkring, fastighetsskatt, förvaltningsarvode, revisionsarvode, styrelsearvode.

ENDAST JSON - Respond ONLY with this structure:
{
  "heating": 0,
  "electricity": 0,
  "water_sewage": 0,
  "waste_management": 0,
  "cleaning": 0,
  "snow_removal": 0,
  "property_insurance": 0,
  "property_tax": 0,
  "management_fee": 0,
  "audit_fee": 0,
  "board_compensation": 0,
  "repairs": 0,
  "other_costs": 0,
  "total_operating_costs": 0
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'note_revenue_agent',
    2,
    ARRAY['Nettoomsättning', 'Rörelseintäkter', 'Not.*Intäkter'],
    'Extracts detailed revenue breakdown from notes',
    'Extrahera intäktsspecifikation från noterna.
Sök efter: årsavgifter bostäder, årsavgifter lokaler, hyresintäkter, parkering, förråd,
överlåtelseavgifter, pantförskrivningsavgifter, bredband, tvättstuga.

ENDAST JSON - Respond ONLY with this structure:
{
  "annual_fees_residential": 0,
  "annual_fees_commercial": 0,
  "commercial_rent": 0,
  "parking_income": 0,
  "storage_income": 0,
  "transfer_fees": 0,
  "mortgage_fees": 0,
  "internet_cable_tv": 0,
  "laundry": 0,
  "other_income": 0,
  "fee_per_sqm": 0
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'suppliers_vendors_agent',
    2,
    ARRAY['Leverantörer', 'Leverantörsförteckning', 'Avtalspartners', 'Samarbetspartners', 'Tjänsteleverantörer'],
    'CRITICAL - Extracts supplier and vendor information (10% of docs but extremely valuable)',
    'Extrahera leverantörsinformation från denna svenska BRF årsredovisning.
VIKTIGT: Endast 10% av rapporter har denna information men när den finns är den mycket värdefull.
Sök efter listor eller omnämnanden av: leverantörer, tjänsteleverantörer, avtalspartners, entreprenörer.
Inkludera ALLA nämnda företagsnamn för: banker, försäkringsbolag, energibolag, värmeleverantör,
elleverantör, sophämtning, städbolag, fastighetsskötsel, hisservice, VVS, elektriker, snöröjning,
trädgårdsskötsel, ekonomisk förvaltning, teknisk förvaltning, juridiska tjänster.

ENDAST JSON - Respond ONLY with found suppliers (tom array om inga hittas):
{
  "banking": [
    {"name": "banknamn", "service": "typ av tjänst", "contact": "kontaktinfo om tillgänglig"}
  ],
  "insurance": [
    {"name": "försäkringsbolag", "type": "försäkringstyp", "policy_number": "om tillgänglig"}
  ],
  "utilities": [
    {"name": "leverantör", "service": "el/värme/vatten/avfall", "contract_info": "avtalsinformation"}
  ],
  "property_services": [
    {"name": "företag", "service": "städ/snö/trädgård/fastighetsskötsel", "frequency": "daglig/vecka/månad"}
  ],
  "technical_services": [
    {"name": "företag", "service": "hiss/VVS/el/ventilation", "contract_type": "service/akut"}
  ],
  "management": [
    {"name": "företag", "service": "ekonomisk/teknisk förvaltning", "contact": "kontaktperson"}
  ],
  "other_suppliers": [
    {"name": "företag", "service": "tjänstebeskrivning", "notes": "övrig info"}
  ],
  "supplier_list_location": "sida X om leverantörslista finns"
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'audit_report_agent',
    3,
    ARRAY['Revisionsberättelse', 'Revisorns rapport', 'Uttalanden'],
    'Extracts audit report and opinions',
    'Extrahera revisionsberättelse från denna svenska BRF årsredovisning.
Sök efter: uttalanden, tillstyrker/avstyrker, ansvarsfrihet, rättvisande bild, anmärkning,
revisorns namn, auktoriserad/godkänd revisor, ort och datum.

ENDAST JSON - Respond ONLY with this structure:
{
  "opinion": "Utan anmärkning/Med anmärkning",
  "recommends_approval": true,
  "recommends_discharge": true,
  "auditor_name": "revisorns namn",
  "audit_firm": "revisionsbolag",
  "auditor_title": "Auktoriserad/Godkänd revisor",
  "signature_date": "YYYY-MM-DD",
  "signature_location": "ort",
  "remarks": ["eventuella anmärkningar"]
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'ratio_kpi_agent',
    3,
    ARRAY['Nyckeltal', 'Ekonomisk ställning', 'Ekonomiska nyckeltal'],
    'Calculates and extracts financial ratios',
    'Extrahera eller beräkna nyckeltal från denna svenska BRF årsredovisning.
Sök efter: soliditet %, likviditet, belåningsgrad, skuldkvot, driftskostnad kr/kvm,
räntekänslighet, amorteringstakt.

ENDAST JSON - Respond ONLY with this structure:
{
  "solidity_percent": 0.0,
  "current_ratio": 0.0,
  "debt_to_equity": 0.0,
  "interest_coverage": 0.0,
  "debt_per_sqm": 0,
  "annual_fee_per_sqm": 0,
  "operating_cost_per_sqm": 0,
  "avg_fee_increase_percent": 0.0,
  "financial_assessment": "God/Tillfredsställande/Svag"
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'member_info_agent',
    3,
    ARRAY['Medlemsinformation', 'Antal medlemmar', 'Överlåtelser', 'Andrahandsuthyrning'],
    'Extracts member statistics',
    'Extrahera medlemsinformation från denna svenska BRF årsredovisning.
Sök efter: antal medlemmar, antal lägenheter, överlåtelser, upplåtelser, andrahandsuthyrning,
överlåtelseavgift, pantsättningsavgift.

ENDAST JSON - Respond ONLY with this structure:
{
  "total_members": 0,
  "apartments_count": 0,
  "transfers_during_year": 0,
  "sublets_approved": 0,
  "transfer_fee": 0,
  "mortgage_registration_fee": 0,
  "members_at_year_end": 0
}',
    NOW(),
    NOW()
);

INSERT INTO agent_registry (
    agent_name,
    priority,
    handles_sections,
    description,
    prompt_template,
    created_at,
    updated_at
) VALUES (
    'pledged_assets_agent',
    3,
    ARRAY['Ställda säkerheter', 'Eventualförpliktelser', 'Ansvarsförbindelser'],
    'Extracts pledged assets and contingent liabilities',
    'Extrahera ställda säkerheter från noterna.
Sök efter: fastighetsinteckningar, totalt uttagna pantbrev, varav pantsatta, disponibla pantbrev,
eventualförpliktelser, borgensåtaganden.

ENDAST JSON - Respond ONLY with this structure:
{
  "total_mortgages": 0,
  "pledged_to_banks": 0,
  "available_mortgages": 0,
  "contingent_liabilities": "beskrivning eller ''Inga''",
  "guarantees": "beskrivning eller ''Inga''"
}',
    NOW(),
    NOW()
);

COMMIT;

-- Verify insertion
SELECT COUNT(*) as agent_count FROM agent_registry;