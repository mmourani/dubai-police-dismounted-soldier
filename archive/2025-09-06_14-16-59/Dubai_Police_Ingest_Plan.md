# Dubai Police Project - Data Ingest Plan

## Project Overview
**Location**: `./Dubai_Police_Project/`  
**Purpose**: Comprehensive data ingestion and processing pipeline for Dubai Police SWAT Equipment and Tower Deployment documentation  
**Date**: September 2, 2025

## Directory Structure Analysis

### Current Organization
```
Dubai_Police_Project/
├── 00_Project_Overview/      # Project metadata and summaries
├── 01_Suppliers/             # Supplier information and questionnaires
├── 02_Technical/             # Technical specifications and BOQs
├── 03_Documentation/         # Formal documentation
├── 04_Communications/        # Email drafts and correspondence
├── 05_Visual_Assets/         # Diagrams and AI prompts
├── Archive/                  # Historical pricing and versions
└── v1.0/                     # Version control snapshots
```

## Data Sources Identified

### 1. Technical Documents (Priority: HIGH)
- **Location**: `02_Technical/`
- **Formats**: Markdown (.md), PDF
- **Key Files**:
  - `FINAL_Dubai_Police_ROM_DDP.md` - Master pricing document
  - `Dubai_Police_Detailed_BOQ.md` - Bill of Quantities
  - `Technical_Specifications_Comparison.md` - Equipment specs
  - `Power_Calculations_8Hour.md` - Power requirements
  - `Cable_Specifications.md` - Cable requirements
  - `Statement_of_Work.md` - SOW details
  - `Integration_Diagrams.md` - System architecture

### 2. Supplier Information (Priority: HIGH)
- **Location**: `01_Suppliers/`
- **Formats**: Markdown, CSV (if available)
- **Key Files**:
  - `Supplier_Directory.md` - Vendor contact list
  - `Supplier_Questionnaire.md` - RFQ templates

### 3. Pricing Archives (Priority: MEDIUM)
- **Location**: `Archive/old_pricing/`
- **Formats**: Markdown, PDF
- **Contains**: Historical ROM proposals in USD/AED
  - `Dubai_Police_ROM_Proposal_AED.md`
  - `Dubai_Police_ROM_Proposal_USD.md`
  - `Dubai_Police_ROM_DDP.md`
  - `Dubai_Police_ROM_Customer.md`

### 4. Visual Assets (Priority: LOW)
- **Location**: `05_Visual_Assets/`
- **Formats**: PNG, Markdown prompts
- **Contains**: 
  - AI generation prompts
  - Technical diagrams
  - Professional prompt templates

### 5. Communication Templates (Priority: MEDIUM)
- **Location**: `04_Communications/`
- **Formats**: Markdown email templates

### 6. Datasheets (Priority: HIGH)
- **Location**: `./Datasheets/` (to be organized)
- **Current Files**:
  - StreamCaster NEXUS datasheet (6.4 MB)
  - INVISIO X7 headset system (1.0 MB)
  - INVISIO V-Series Gen II (1.7 MB)
  - Dock-lite specifications (795 KB)

## Ingestion Pipeline

### Phase 1: Data Collection & Organization
```bash
# 1. Create organized structure
mkdir -p ./Dubai_Police_Project/Datasheets/{INVISIO,StreamCaster,Dock,Tait,Motorola}

# 2. Move datasheets to organized locations
mv "StreamCaster NEXUS*.pdf" ./Dubai_Police_Project/Datasheets/StreamCaster/
mv "INVISIO*.pdf" ./Dubai_Police_Project/Datasheets/INVISIO/
mv "dock-lite*.pdf" ./Dubai_Police_Project/Datasheets/Dock/

# 3. Aggregate all markdown files
find ./Dubai_Police_Project -name "*.md" -type f > manifest.txt

# 4. Collect PDFs for reference
find ./Dubai_Police_Project -name "*.pdf" -type f >> manifest.txt

# 5. Identify CSV/Excel files if any
find ./Dubai_Police_Project -name "*.csv" -o -name "*.xlsx" >> manifest.txt
```

### Phase 2: Data Processing

#### A. Markdown Processing
1. Parse markdown headers for structure
2. Extract tables (BOQ, pricing, specifications)
3. Identify key-value pairs (prices, quantities, part numbers)
4. Build relationships between documents

#### B. Table Extraction Priority
```python
# Priority tables to extract:
- BOQ tables from Dubai_Police_Detailed_BOQ.md
- Pricing tables from FINAL_Dubai_Police_ROM_DDP.md
- Specification comparisons from Technical_Specifications_Comparison.md
- Power calculations from Power_Calculations_8Hour.md
- Cable specifications from Cable_Specifications.md
- Supplier contact matrices from Supplier_Directory.md
```

#### C. Metadata Generation
```yaml
# Generate meta.yaml for doc-foundry:
project:
  client: "Dubai Police"
  project: "SWAT Equipment & Tower Deployment"
  version: "v1.0"
  brand: "beacon-red"
  
categories:
  - dismounted_soldier_equipment
  - sc4200_towers
  - sc4400_towers
  - network_infrastructure
  - communication_systems
  
pricing:
  currency: ["USD", "AED"]
  pricing_model: "ROM (Rough Order of Magnitude)"
  validity: "90 days"
  exchange_rate: 3.67  # 1 USD = 3.67 AED

equipment_categories:
  dismounted_soldier:
    - INVISIO_X7_headset
    - tactical_PTT
    - body_worn_antenna
    - tactical_battery_pack
    
  towers:
    - SC4200_base_stations
    - SC4400_base_stations
    - antennas_omnidirectional
    - power_systems
    - cables_and_connectors
```

### Phase 3: Data Transformation

#### A. Normalize Formats
1. Convert all prices to standard format (USD primary, AED secondary)
2. Standardize part numbers and SKUs
3. Unify supplier naming conventions
4. Create consistent date formats

#### B. Create Data Relationships
```sql
-- Conceptual schema for organizing data
CREATE TABLE equipment (
  id PRIMARY KEY,
  category VARCHAR,
  part_number VARCHAR,
  description TEXT,
  unit_price_usd DECIMAL,
  unit_price_aed DECIMAL,
  quantity INTEGER,
  total_price_usd DECIMAL,
  total_price_aed DECIMAL,
  supplier_id FOREIGN KEY,
  datasheet_path VARCHAR
);

CREATE TABLE suppliers (
  id PRIMARY KEY,
  name VARCHAR,
  contact_email VARCHAR,
  phone VARCHAR,
  website VARCHAR,
  country VARCHAR,
  product_categories TEXT[]
);

CREATE TABLE pricing_history (
  id PRIMARY KEY,
  equipment_id FOREIGN KEY,
  price_usd DECIMAL,
  price_aed DECIMAL,
  date DATE,
  version VARCHAR,
  document_source VARCHAR
);

CREATE TABLE technical_specs (
  id PRIMARY KEY,
  equipment_id FOREIGN KEY,
  spec_name VARCHAR,
  spec_value VARCHAR,
  unit VARCHAR
);
```

### Phase 4: Doc-Foundry Integration

#### A. Generate Project Structure
```bash
# Use doc-foundry to create complete project
mcp__doc-foundry__doc_generate_project \
  --client "Dubai Police" \
  --project "SWAT Equipment & SC4200/4400 Tower Deployment" \
  --version "v1.0" \
  --brand "beacon-red" \
  --working_dir "./Dubai_Police_Project" \
  --generate_pdfs true \
  --download_datasheets false
```

#### B. Evidence Capture
```bash
# Capture pricing evidence from suppliers
mcp__doc-foundry__research_capture_cost \
  --project_root "./Dubai_Police_Project" \
  --supplier_name "INVISIO" \
  --evidence_type "quote" \
  --cost_amount 2500 \
  --currency "USD"

# Export evidence table
mcp__doc-foundry__evidence_export_table \
  --project_root "./Dubai_Police_Project"
```

#### C. Dashboard Generation
```bash
# Generate interactive dashboard
mcp__doc-foundry__evidence_generate_dashboard \
  --project_root "./Dubai_Police_Project" \
  --include_charts true \
  --theme "light"
```

## Automation Script

```bash
#!/bin/bash
# Dubai Police Project Comprehensive Ingest Script

PROJECT_ROOT="./Dubai_Police_Project"
OUTPUT_DIR="./ingested_data"
DATASHEETS_DIR="$PROJECT_ROOT/Datasheets"

echo "=== Dubai Police Project Ingest Pipeline ==="
echo "Starting at: $(date)"

# Step 1: Create backup
echo "Creating backup..."
tar -czf "backup_$(date +%Y%m%d_%H%M%S).tar.gz" "$PROJECT_ROOT"

# Step 2: Organize datasheets
echo "Organizing datasheets..."
mkdir -p "$DATASHEETS_DIR"/{INVISIO,StreamCaster,Dock,Tait,Motorola}

# Move PDFs to appropriate folders
for pdf in *.pdf; do
  if [[ -f "$pdf" ]]; then
    case "$pdf" in
      *INVISIO*) mv "$pdf" "$DATASHEETS_DIR/INVISIO/" ;;
      *StreamCaster*|*NEXUS*) mv "$pdf" "$DATASHEETS_DIR/StreamCaster/" ;;
      *dock*|*Dock*) mv "$pdf" "$DATASHEETS_DIR/Dock/" ;;
      *) mv "$pdf" "$DATASHEETS_DIR/" ;;
    esac
  fi
done

# Step 3: Create output structure
echo "Creating output directories..."
mkdir -p "$OUTPUT_DIR"/{raw,processed,meta,exports,evidence}

# Step 4: Collect source files
echo "Collecting source files..."
find "$PROJECT_ROOT" -type f \( -name "*.md" -o -name "*.pdf" -o -name "*.csv" \) \
  -exec cp {} "$OUTPUT_DIR/raw/" \; 2>/dev/null

# Step 5: Extract metadata from markdown files
echo "Processing markdown files..."
for file in "$OUTPUT_DIR"/raw/*.md; do
  if [[ -f "$file" ]]; then
    basename=$(basename "$file" .md)
    # Extract tables and structured data
    grep -E "^\|" "$file" > "$OUTPUT_DIR/processed/${basename}_tables.txt" 2>/dev/null
    # Extract pricing information
    grep -E "\$|USD|AED|[0-9]+\.[0-9]{2}" "$file" > "$OUTPUT_DIR/processed/${basename}_pricing.txt" 2>/dev/null
  fi
done

# Step 6: Generate meta.yaml for doc-foundry
echo "Generating metadata file..."
cat > "$OUTPUT_DIR/meta/meta.yaml" << 'EOF'
client: "Dubai Police"
project: "SWAT Equipment & SC4200/4400 Tower Deployment"
version: "v1.0"
brand: "beacon-red"

title: "Technical and Commercial Proposal for Dubai Police SWAT Equipment and Communication Towers"
executive_summary: |
  Comprehensive solution for Dubai Police SWAT team equipment including 
  INVISIO communication systems and SC4200/4400 tower infrastructure deployment.

objectives: |
  - Deploy advanced tactical communication equipment for SWAT personnel
  - Install SC4200/4400 tower infrastructure for enhanced coverage
  - Ensure 8-hour operational capability with backup power systems
  - Provide comprehensive training and support

deliverables: |
  - INVISIO X7 headset systems for dismounted soldiers
  - SC4200/4400 base station towers with full infrastructure
  - Power backup systems with 8-hour autonomy
  - Complete cable and antenna systems
  - Training and commissioning services

assumptions: |
  - Site access will be provided by Dubai Police
  - Power infrastructure is available at tower locations
  - Import permits will be handled by client
  - 90-day project timeline from PO

payment_terms: |
  - 30% advance payment upon PO
  - 40% upon delivery to site
  - 20% upon commissioning completion
  - 10% after acceptance and handover

warranty_support: |
  - 2 years manufacturer warranty on all equipment
  - 1 year installation warranty
  - 24/7 technical support hotline
  - Quarterly preventive maintenance visits

sla: |
  - 4-hour response time for critical issues
  - 24-hour response time for non-critical issues
  - 95% uptime guarantee
  - Spare parts availability within 48 hours
EOF

# Step 7: Create supplier list
echo "Building supplier database..."
cat > "$OUTPUT_DIR/meta/suppliers.yaml" << 'EOF'
suppliers:
  - name: "INVISIO Communications"
    website: "https://www.invisio.com"
    email: "sales@invisio.com"
    phone: "+46 8 650 7950"
    country: "Sweden"
    products: "Tactical communication headsets"
    
  - name: "Tait Communications"
    website: "https://www.taitcommunications.com"
    email: "sales@taitcommunications.com"
    phone: "+64 3 358 3399"
    country: "New Zealand"
    products: "SC4200/4400 base stations"
    
  - name: "Motorola Solutions"
    website: "https://www.motorolasolutions.com"
    email: "sales@motorolasolutions.com"
    phone: "+1 847 576 5000"
    country: "USA"
    products: "Radio systems and infrastructure"
EOF

# Step 8: Generate document package using doc-foundry
echo "Generating document package..."
# This would call the actual doc-foundry command
# mcp__doc-foundry__doc_generate_pack \
#   --meta_path "$OUTPUT_DIR/meta/meta.yaml" \
#   --out_dir "$OUTPUT_DIR/exports" \
#   --pdf true

# Step 9: Create summary report
echo "Creating summary report..."
cat > "$OUTPUT_DIR/ingest_summary.md" << EOF
# Dubai Police Project Ingest Summary
Date: $(date)

## Files Processed
- Markdown files: $(find "$OUTPUT_DIR/raw" -name "*.md" | wc -l)
- PDF files: $(find "$OUTPUT_DIR/raw" -name "*.pdf" | wc -l)
- CSV files: $(find "$OUTPUT_DIR/raw" -name "*.csv" | wc -l)

## Datasheets Organized
- INVISIO: $(find "$DATASHEETS_DIR/INVISIO" -name "*.pdf" 2>/dev/null | wc -l)
- StreamCaster: $(find "$DATASHEETS_DIR/StreamCaster" -name "*.pdf" 2>/dev/null | wc -l)
- Other: $(find "$DATASHEETS_DIR" -maxdepth 1 -name "*.pdf" 2>/dev/null | wc -l)

## Output Generated
- Processed files: $(find "$OUTPUT_DIR/processed" -type f | wc -l)
- Metadata files: $(find "$OUTPUT_DIR/meta" -type f | wc -l)

## Next Steps
1. Review generated meta.yaml
2. Run doc-foundry generation
3. Verify output quality
4. Commit changes to git
EOF

echo "=== Ingestion Complete ==="
echo "Summary available at: $OUTPUT_DIR/ingest_summary.md"
echo "Completed at: $(date)"
```

## Quality Assurance Checklist

### Data Validation
- [ ] All part numbers follow standard format
- [ ] Prices are within expected ranges (USD 100-500,000)
- [ ] Quantities match across BOQ and pricing documents
- [ ] Supplier information is complete (name, email, website)
- [ ] No duplicate entries in equipment lists
- [ ] Currency conversions are accurate (1 USD = 3.67 AED)

### Document Completeness
- [ ] Technical specifications for all equipment items
- [ ] Pricing available for all BOQ items
- [ ] Supplier assigned to each product category
- [ ] Power calculations verified
- [ ] Cable specifications complete
- [ ] Integration diagrams up to date

### Output Verification
- [ ] Meta.yaml contains all required fields
- [ ] Supplier list includes all vendors
- [ ] Document package generates without errors
- [ ] PDFs render correctly
- [ ] Evidence tracking functional

## Error Handling

```python
# Common error handling patterns

def safe_parse_price(price_str):
    """Safely parse price strings with multiple formats"""
    try:
        # Remove currency symbols and commas
        clean_price = price_str.replace('$', '').replace(',', '').replace('AED', '').strip()
        return float(clean_price)
    except (ValueError, AttributeError):
        logging.warning(f"Could not parse price: {price_str}")
        return 0.0

def validate_supplier(supplier_name):
    """Validate and normalize supplier names"""
    known_suppliers = {
        'invisio': 'INVISIO Communications',
        'tait': 'Tait Communications',
        'motorola': 'Motorola Solutions'
    }
    normalized = supplier_name.lower().strip()
    for key, value in known_suppliers.items():
        if key in normalized:
            return value
    return supplier_name  # Return original if no match

def handle_missing_data(field_name, default_value):
    """Handle missing required fields gracefully"""
    logging.info(f"Missing {field_name}, using default: {default_value}")
    return default_value
```

## Success Metrics

- **Coverage**: 100% of documents in project directory processed
- **Accuracy**: >95% successful table extraction from markdown
- **Speed**: Complete pipeline execution in <5 minutes
- **Quality**: All generated documents pass doc-foundry validation
- **Organization**: Zero orphaned files in root directory

## Post-Ingestion Tasks

1. **Git Operations**:
   ```bash
   git add -A
   git commit -m "feat: organized project structure and ingested data"
   git tag -a "v1.0-ingested" -m "Post-ingestion checkpoint"
   ```

2. **Documentation Update**:
   - Update README with new structure
   - Create CHANGELOG.md entry
   - Document datasheet locations

3. **Backup Verification**:
   - Verify backup integrity
   - Store backup in secure location
   - Document backup location and date

## Timeline

- **Preparation & Backup**: 5 minutes
- **Data Organization**: 10 minutes
- **Processing & Extraction**: 10 minutes
- **Doc-Foundry Generation**: 5 minutes
- **Verification & QA**: 10 minutes
- **Documentation**: 5 minutes

**Total Estimated Time**: 45 minutes

---

*This comprehensive ingest plan ensures all Dubai Police project data is properly organized, processed, and ready for document generation using doc-foundry and other MCP tools.*