# CABLE SPECIFICATIONS DOCUMENT
## Dubai Police SWAT Tactical Communication System

**Document Version:** 1.0  
**Date:** January 29, 2025  
**Purpose:** Define all cable requirements and specifications  

---

## EXECUTIVE SUMMARY

This document specifies all cables required for the Dubai Police SWAT tactical communication system. Four primary cables connect the system components, with each cable designed for military-grade reliability in extreme desert conditions.

**Total Cables Required:** 4 per operator kit
- 1× Tetra-to-INVISIO cable (60cm)
- 1× Samsung-to-INVISIO cable (50cm)  
- 2× USB-C power cables (80cm, 40cm)

---

## 1. SYSTEM CABLE OVERVIEW

### 1.1 Cable Architecture

```
TETRA TH1n ═══[Cable 1]═══> INVISIO V60 II <═══[Cable 2]═══ Samsung S25
                                    ↑
                          Power via connected devices
                                    
Battery Pack ═══[Cable 3]═══> Samsung S25
           ╚═══[Cable 4]═══> Spare/Accessories
```

### 1.2 Cable Requirements Matrix

| Cable ID | Function | Length | Connectors | Shielding | Temp Rating |
|----------|----------|---------|------------|-----------|-------------|
| CBL-001 | Tetra-INVISIO | 60cm | 26-pin to 6-pin | Dual | -40°C to +85°C |
| CBL-002 | Samsung-INVISIO | 50cm | USB-C to 6-pin | Single | -40°C to +85°C |
| CBL-003 | Power Primary | 80cm | USB-C to USB-C | None* | -40°C to +85°C |
| CBL-004 | Power Secondary | 40cm | USB-C to USB-C | None* | -40°C to +85°C |

*Power cables use twisted pair construction for EMI reduction

---

## 2. CABLE CBL-001: TETRA-TO-INVISIO

### 2.1 General Specifications

**Function:** Connects Tetra TH1n radio to INVISIO V60 II control unit  
**Length:** 60cm ±2cm (24 inches)  
**Flexibility:** Spiral section for extension to 90cm  
**Color:** Tan/Coyote Brown (Federal Standard 30219)  
**Operating Temperature:** -40°C to +85°C  
**Storage Temperature:** -55°C to +125°C  

### 2.2 Connector A: Tetra Radio Side

**Type:** 26-pin Multi-Contact Connector  
**Standard:** Likely MIL-DTL-38999 Series III equivalent  
**Shell Size:** 15 or 17 (TBD based on radio model)  
**Insert Arrangement:** Custom for Tetra  
**Contact Type:** Socket (female)  
**Contact Plating:** Gold over nickel (50μ" minimum)  
**Keying:** Position A  
**Coupling:** Threaded with safety wire holes  
**Sealing:** Environmental O-ring  

**Pin Assignment (Preliminary):**

| Pin | Function | Wire Color | AWG |
|-----|----------|------------|-----|
| 1 | Audio Out + | White | 24 |
| 2 | Audio Out - | White/Black | 24 |
| 3 | Audio In + | Red | 24 |
| 4 | Audio In - | Red/Black | 24 |
| 5 | PTT Signal | Yellow | 26 |
| 6 | PTT Ground | Yellow/Black | 26 |
| 7 | Power + (if required) | Orange | 22 |
| 8 | Power Ground | Black | 22 |
| 9-26 | Reserved/NC | - | - |

### 2.3 Connector B: INVISIO Side

**Type:** INVISIO Proprietary 6-pin Circular  
**Model:** V-Series Tactical Connector  
**Contact Type:** Pin (male)  
**Locking:** Push-pull with positive lock  
**Sealing:** IP68 rated with cap  
**Mating Cycles:** >5,000  
**Contact Resistance:** <50mΩ  

**Pin Assignment:**

| Pin | Function | Wire Color |
|-----|----------|------------|
| 1 | Audio Left | White |
| 2 | Audio Right | Red |
| 3 | Audio Ground | Black |
| 4 | PTT | Yellow |
| 5 | Power (if used) | Orange |
| 6 | Data/Reserved | Green |

### 2.4 Cable Construction

**Conductors:**
- Audio pairs: 24 AWG stranded (7/32)
- PTT: 26 AWG stranded (7/34)
- Power (if used): 22 AWG stranded (19/34)
- Material: Tinned copper

**Shielding:**
- Inner: Aluminum/Mylar foil (100% coverage)
- Outer: Tinned copper braid (85% coverage)
- Drain wire: 26 AWG tinned copper

**Insulation:**
- Primary: ETFE (Ethylene Tetrafluoroethylene)
- Temperature rating: -65°C to +150°C
- Voltage rating: 300V
- Dielectric strength: 1500V/mil

**Jacket:**
- Material: TPU (Thermoplastic Polyurethane)
- Thickness: 0.040" (1.0mm)
- Abrasion resistance: MIL-DTL-17 Grade A
- Chemical resistance: JP-8, DEET, hydraulic fluid

### 2.5 Performance Specifications

**Electrical:**
- Impedance: 50Ω ±5% (audio pairs)
- Capacitance: <100pF/meter
- Attenuation: <0.5dB @ 10kHz
- Crosstalk: >60dB @ 1kHz
- Shielding effectiveness: >60dB (10MHz-1GHz)

**Mechanical:**
- Tensile strength: >50 lbs (222N)
- Flex life: >100,000 cycles (±90°)
- Minimum bend radius: 6× cable diameter
- Crush resistance: 100 lbs/inch

---

## 3. CABLE CBL-002: SAMSUNG-TO-INVISIO

### 3.1 General Specifications

**Function:** Connects Samsung S25 to INVISIO V60 II for audio/PTT  
**Length:** 50cm ±2cm (20 inches)  
**Type:** Straight with strain reliefs  
**Color:** Black  
**Operating Temperature:** -40°C to +85°C  

### 3.2 Connector A: Samsung Side

**Type:** USB Type-C Male  
**Standard:** USB 3.2 Gen 1  
**Orientation:** Right-angle (90°)  
**Shell Material:** Aluminum with nickel plating  
**Contact Rating:** 5A continuous  
**Features:** E-marker chip for PD negotiation  

**Pin Utilization:**

| USB-C Pin | Function | Usage |
|-----------|----------|-------|
| A1, B12 | GND | Ground |
| A4, B9 | VBUS | Power (5V) |
| A5 | CC1 | Configuration |
| B5 | CC2 | Configuration |
| A6 | D+ | USB 2.0 Data |
| A7 | D- | USB 2.0 Data |
| B6 | D+ | USB 2.0 Data |
| B7 | D- | USB 2.0 Data |
| A8 | SBU1 | Audio Left |
| B8 | SBU2 | Audio Right |

### 3.3 Connector B: INVISIO Side

**Type:** INVISIO 6-pin (same as CBL-001)  
**Configuration:** Audio + PTT + Power  

### 3.4 Cable Construction

**Conductors:**
- Power: 20 AWG (VBUS/GND)
- Data: 28 AWG twisted pair
- Audio: 26 AWG twisted pair
- Configuration: 28 AWG

**Shielding:**
- Overall: Aluminum/Mylar foil + drain wire
- EMI suppression: Ferrite core near USB-C

**Jacket:**
- Material: Flexible PVC
- Diameter: 4.5mm
- Flexibility: High-flex grade

### 3.5 Special Requirements

**Audio Processing:**
- USB Audio Class 1.0 compliance
- Sample rate: 48kHz
- Bit depth: 16-bit
- Latency: <10ms

---

## 4. CABLES CBL-003/004: USB-C POWER DELIVERY

### 4.1 General Specifications

**Function:** Power delivery from battery pack to devices  
**Lengths:** CBL-003: 80cm, CBL-004: 40cm  
**Rating:** USB-C PD 3.0, 45W (3A @ 15V)  
**Color:** Black with orange strain reliefs  

### 4.2 Connector Specifications

**Both Ends:** USB Type-C Male  
**Shell:** Aluminum, black anodized  
**Contacts:** Gold plated, 5A rated  
**E-Marker:** Required for >3A operation  

**E-Marker Specifications:**
- Chip: TI TPS65987 or equivalent
- Max current: 5A
- Max voltage: 20V
- USB PD version: 3.0
- Cable type: Electronically marked

### 4.3 Cable Construction

**Conductors:**
- VBUS/GND: 18 AWG (5A capability)
- CC: 28 AWG
- Data (if included): 28 AWG twisted
- Total conductors: 24

**Construction:**
- Twisted pairs for data lines
- Power pairs separated
- Overall shield optional
- Drain wire if shielded

**Jacket:**
- Material: TPE (Thermoplastic Elastomer)
- Thickness: 0.8mm
- Outer diameter: 5.5mm
- Braided outer layer for durability

### 4.4 Electrical Specifications

**Power Delivery:**
- Voltage drop: <250mV @ 3A (80cm)
- Resistance: <180mΩ (round trip)
- Current rating: 5A maximum
- Power profiles: 5V/3A, 9V/3A, 15V/3A, 20V/2.25A

**Safety Features:**
- Over-current protection in E-marker
- Temperature monitoring
- Voltage regulation feedback

---

## 5. ENVIRONMENTAL SPECIFICATIONS

### 5.1 Temperature Performance

**All Cables Must Operate:**
- Continuous: -20°C to +60°C
- Intermittent: -40°C to +85°C
- Storage: -55°C to +125°C
- Temperature shock: ΔT = 100°C in 5 seconds

### 5.2 Environmental Resistance

**Ingress Protection:**
- Mated connectors: IP67 minimum
- Unmated with caps: IP67
- Submersion: 1 meter for 30 minutes

**Chemical Resistance:**
- Fuels: JP-8, diesel, gasoline
- Solvents: Acetone, MEK (limited exposure)
- Personal: DEET, sunscreen
- Cleaning: Isopropyl alcohol

**UV Resistance:**
- 1000 hours UV-B exposure
- No cracking or significant degradation
- Color fastness: ΔE < 3

### 5.3 Mechanical Durability

**Vibration:**
- Random: 0.04 g²/Hz, 20-2000 Hz
- Sinusoidal: 10G peak, 10-500 Hz
- Duration: 6 hours per axis

**Shock:**
- Operational: 40G, 11ms half-sine
- Survival: 75G, 6ms half-sine
- Drop: 2 meters onto concrete

**Flex Life:**
- ±90° flex: 100,000 cycles minimum
- Twist: ±180°/meter, 10,000 cycles
- Rolling: 10,000 cycles over 25mm mandrel

---

## 6. MARKING AND IDENTIFICATION

### 6.1 Cable Marking

**Each Cable Shall Include:**
- Cable type designation (CBL-001 through CBL-004)
- Manufacturer name/logo
- Date code (YYWW format)
- Serial number (if required)
- Length marking every meter

**Marking Method:**
- Hot stamp or laser marking
- Indelible ink permitted
- Must survive operational life

### 6.2 Connector Marking

**Each Connector:**
- Function label (e.g., "TETRA", "INVISIO", "PWR")
- Polarity marking if applicable
- Pin 1 indicator
- Mating connector part number

### 6.3 Color Coding

| Cable Type | Primary Color | Stripe/Band |
|------------|--------------|-------------|
| Audio/Data | Tan/Coyote | None |
| Power Primary | Black | Orange band |
| Power Secondary | Black | Yellow band |
| Spare/Future | Black | Green band |

---

## 7. QUALITY ASSURANCE

### 7.1 Testing Requirements

**100% Production Testing:**
- Continuity: All conductors
- Insulation resistance: >100MΩ @ 500V
- Hi-pot: 1500V for 1 second
- VSWR: <1.5:1 (if applicable)

**Sampling Testing (AQL 2.5):**
- Insertion/withdrawal force
- Contact resistance
- Shielding effectiveness
- Environmental cycling

### 7.2 Acceptance Criteria

**Electrical:**
- No opens or shorts
- Resistance within ±5% of specification
- Shielding effectiveness >60dB

**Mechanical:**
- Connectors mate smoothly
- Positive lock engagement
- No visible damage

**Visual:**
- Correct marking and labeling
- No contamination or debris
- Proper strain relief installation

### 7.3 Documentation

**Required with Each Shipment:**
- Certificate of Conformance
- Test data (by lot)
- Material certifications
- Assembly drawings

---

## 8. LOGISTICS AND SPARES

### 8.1 Packaging

**Individual Cable:**
- Anti-static bag
- Connector caps installed
- Coiled to prevent kinking
- Label with P/N and S/N

**Kit Packaging:**
- Foam insert with cable positions
- Moisture barrier bag
- Desiccant included
- Shock indicator

### 8.2 Recommended Spares

**Per 10 Operator Kits:**

| Cable Type | Quantity | Percentage |
|------------|----------|------------|
| Tetra-INVISIO | 2 | 20% |
| Samsung-INVISIO | 2 | 20% |
| Power Primary | 3 | 30% |
| Power Secondary | 2 | 20% |
| Connector caps | 20 | 200% |

### 8.3 Maintenance

**Field Cleaning:**
- Isopropyl alcohol (70%)
- Lint-free wipes
- Compressed air
- Contact cleaner (approved type)

**Inspection Interval:**
- Visual: Before each mission
- Electrical: Monthly
- Complete test: Annually

---

## 9. COMPLIANCE AND STANDARDS

### 9.1 Applicable Standards

**Military:**
- MIL-DTL-38999: Circular connectors
- MIL-DTL-17: Cable, radio frequency
- MIL-STD-810H: Environmental testing
- MIL-STD-461G: EMI/EMC requirements

**Commercial:**
- USB 3.2: USB specifications
- USB PD 3.0: Power delivery
- IEC 60529: IP ratings
- RoHS: Material compliance

### 9.2 Certifications Required

- RoHS compliant
- REACH compliant
- Conflict minerals declaration
- UL/CE marking (where applicable)

---

## 10. SUPPLIER REQUIREMENTS

### 10.1 Qualified Suppliers

**Recommended Manufacturers:**
1. **Glenair:** Military tactical cables
2. **Amphenol:** MIL-DTL-38999 specialists
3. **TE Connectivity:** Rugged connectors
4. **Times Microwave:** RF/tactical cables

### 10.2 Custom Cable Assembly

**Required Capabilities:**
- MIL-SPEC connector experience
- Environmental testing facility
- ISO 9001 certification
- ITAR compliance (if applicable)

### 10.3 Lead Times

| Cable Type | Prototype | Production |
|------------|-----------|------------|
| Standard USB-C | 1 week | 2-3 weeks |
| Custom Tactical | 3-4 weeks | 6-8 weeks |
| MIL-SPEC Assembly | 4-6 weeks | 8-10 weeks |

---

## APPENDICES

### Appendix A: Connector Pin-Out Diagrams
*[Detailed engineering drawings to be added]*

### Appendix B: Bend Radius Calculations
*[Minimum bend radius for each cable type]*

### Appendix C: EMI/RFI Test Results
*[Shielding effectiveness measurements]*

### Appendix D: Environmental Test Reports
*[Temperature, humidity, immersion test data]*

---

*End of Cable Specifications Document*