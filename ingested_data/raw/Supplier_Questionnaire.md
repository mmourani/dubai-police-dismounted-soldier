# SUPPLIER TECHNICAL QUESTIONNAIRE
**Project:** Dubai Police SWAT Tactical Communication System  
**Date:** January 29, 2025  
**Purpose:** Gather missing technical specifications for system integration

---

## SECTION 1: INVISIO COMMUNICATIONS

### V60 II Control Unit - Power & Operation

1. **Power Requirements**
   - [ ] Does the V60 II have an internal battery?
   - [ ] If powered from connected devices, what is the current draw from each port?
   - [ ] Minimum voltage required for operation?
   - [ ] Can it operate with only one powered device connected?
   - [ ] What happens if all connected devices lose power simultaneously?
   - [ ] Is there a backup capacitor for power loss transitions?

2. **Dual PTT Assembly**
   - [ ] Does the dual PTT require its own power source?
   - [ ] If yes, what type of battery? (AA/AAA/CR123/CR2032/Other: _______)
   - [ ] Expected battery life in hours at 20% transmit duty cycle?
   - [ ] Is there a low battery warning indicator (visual/audio)?
   - [ ] Can the PTT be powered via USB-C from the main power bank?
   - [ ] What is the operating current consumption?

3. **Audio Processing**
   - [ ] Audio latency from input to output in milliseconds?
   - [ ] Maximum SPL output capability?
   - [ ] Audio codec specifications?
   - [ ] Simultaneous audio mixing capability confirmed for 3 sources?
   - [ ] Independent volume control for each channel?

### Cable Specifications & Connectors

4. **Tetra Radio Interface**
   - [ ] Exact connector type on V60 II side? (Model/Part number: _______)
   - [ ] Is it MIL-DTL-38999 Series? If yes, which series (I/II/III/IV)?
   - [ ] Shell size? (9/11/13/15/17/19/21/23/25)
   - [ ] Pin configuration diagram available?
   - [ ] Audio impedance matching requirements?
   - [ ] PTT signal voltage/current specifications?

5. **Samsung Device Interface**
   - [ ] Connection type: USB-C or proprietary connector?
   - [ ] If USB-C, which pins are utilized?
   - [ ] Audio over USB protocol used? (UAC 1.0/2.0/proprietary)
   - [ ] Power delivery from phone supported?
   - [ ] Data rate requirements?
   - [ ] Cable maximum length without signal degradation?

6. **Cable Requirements**
   - [ ] Shielding requirements? (Braided/Foil/Both)
   - [ ] Minimum bend radius for tactical use?
   - [ ] Tensile strength requirement in kg?
   - [ ] EMI/RFI protection level required?
   - [ ] Operating temperature range for cables?
   - [ ] Color coding standard used?

### Environmental & Durability

7. **Desert Operations**
   - [ ] Confirmed operating temperature: -20°C to +60°C?
   - [ ] Has the system been tested above 50°C ambient?
   - [ ] Sand/dust ingress testing completed to IP6X?
   - [ ] Performance degradation at high temperature?
   - [ ] MTBF in desert conditions?
   - [ ] Recommended cleaning/maintenance interval in sandy conditions?

8. **Reliability Data**
   - [ ] Number of PTT activation cycles tested?
   - [ ] Connector mating cycles rating?
   - [ ] Warranty period for Middle East deployment?
   - [ ] Known failure modes in high-temperature operation?
   - [ ] Spare parts recommended per 10 units?

---

## SECTION 2: SAMSUNG GALAXY S25

### Power Consumption & Thermal Management

9. **Power Profile**
   - [ ] Average current draw with ATAK running, GPS active, 4G connected?
   - [ ] Peak current draw with screen at maximum brightness?
   - [ ] Power consumption in watts at typical operation?
   - [ ] Fast charging wattage supported? (25W/45W/65W)
   - [ ] Power Delivery version? (PD 2.0/3.0/PPS)
   - [ ] Wireless charging wattage if applicable?

10. **Thermal Performance**
    - [ ] CPU throttling temperature threshold?
    - [ ] Battery charging cutoff temperature?
    - [ ] Performance impact at 50°C ambient?
    - [ ] Recommended thermal mitigation accessories?
    - [ ] Screen brightness auto-dimming temperature?
    - [ ] GPS accuracy impact at high temperature?

### Integration Requirements

11. **Physical Specifications with Case**
    - [ ] Exact dimensions with Bunker MAAK case installed?
    - [ ] Total weight with case and screen protector?
    - [ ] Center of gravity location for mounting?
    - [ ] Vibration dampening required?
    - [ ] Drop test rating with case?

12. **Connectivity**
    - [ ] 5G bands supported in UAE?
    - [ ] Dual SIM capability?
    - [ ] External antenna connector available?
    - [ ] Bluetooth version and profiles?
    - [ ] NFC availability for tactical applications?

---

## SECTION 3: BUNKER SUPPLY MAAK CASE

### Mounting System

13. **MAAKLOCK Specifications**
    - [ ] Breaking force of MAAKLOCK connection in kg?
    - [ ] Quick-release mechanism activation force?
    - [ ] Can it support running/combat movements?
    - [ ] Rotation limits when mounted?
    - [ ] Vibration resistance rating?

14. **Forearm Mount Details**
    - [ ] Velcro strap specifications (width/length/breaking strength)?
    - [ ] Compatible with different arm sizes (circumference range)?
    - [ ] Anti-slip backing material?
    - [ ] Quick-release time in seconds?
    - [ ] Can it be operated with gloves?

### Environmental Protection

15. **Ingress Protection**
    - [ ] IP rating with ports closed?
    - [ ] IP rating with USB-C port open?
    - [ ] Dust cover replacement part numbers?
    - [ ] Gasket material and temperature rating?
    - [ ] Chemical resistance (fuel, oil, solvents)?

---

## SECTION 4: POWER SYSTEM REQUIREMENTS

### Battery Specifications (Any Supplier)

16. **Electrical Characteristics**
    - [ ] Cell chemistry type? (LiFePO4/Li-ion/Li-polymer)
    - [ ] Nominal voltage?
    - [ ] Voltage range (min-max)?
    - [ ] Actual usable capacity at 50°C ambient?
    - [ ] Capacity retention after 500 cycles?
    - [ ] Self-discharge rate per month?

17. **Hot-Swap Functionality**
    - [ ] Switchover time in milliseconds?
    - [ ] Is there a supercapacitor for zero-interrupt switching?
    - [ ] Can both batteries charge simultaneously?
    - [ ] Battery balancing method?
    - [ ] Hot-swap controller specifications?
    - [ ] Visual/audio indication of swap readiness?

18. **Charging Specifications**
    - [ ] Charge time from 0-100% at 25°C?
    - [ ] Charge time from 0-100% at 50°C?
    - [ ] Maximum charging current?
    - [ ] Charging efficiency percentage?
    - [ ] Can it charge while providing power (pass-through)?

19. **Safety Systems**
    - [ ] Over-current protection threshold and response time?
    - [ ] Over-temperature cutoff temperature?
    - [ ] Short circuit protection response time?
    - [ ] Cell balancing accuracy?
    - [ ] UN38.3 transportation certification?
    - [ ] MIL-STD certification level?

20. **Physical Specifications**
    - [ ] Exact dimensions (L×W×H in mm)?
    - [ ] Weight in grams?
    - [ ] Mounting points/attachment method?
    - [ ] Connector types and positions?
    - [ ] LED indicators and their meanings?
    - [ ] Operating temperature range verified?

### USB-C Power Delivery

21. **Port Specifications**
    - [ ] Number of USB-C ports?
    - [ ] Power Delivery version per port?
    - [ ] Maximum current per port?
    - [ ] Total combined output power?
    - [ ] E-marker chip included in cables?
    - [ ] Supported voltage profiles?

---

## SECTION 5: CABLE REQUIREMENTS

### Tetra-INVISIO Cable

22. **Connector Specifications**
    - [ ] Tetra side: Exact 26-pin connector model/standard?
    - [ ] INVISIO side: Connector model/part number?
    - [ ] Pin-out diagram available?
    - [ ] Which pins carry audio/PTT/power?
    - [ ] Impedance requirements?

23. **Cable Construction**
    - [ ] Conductor material and AWG?
    - [ ] Shielding type and coverage percentage?
    - [ ] Jacket material and thickness?
    - [ ] Minimum bend radius?
    - [ ] Tensile strength?
    - [ ] Flexibility rating?

### Samsung-INVISIO Cable

24. **Technical Specifications**
    - [ ] USB-C version (2.0/3.0/3.1)?
    - [ ] Which USB-C pins are connected?
    - [ ] Audio transmission method (analog/digital)?
    - [ ] Power pins connected?
    - [ ] Cable length options available?
    - [ ] Right-angle connectors available?

### Power Cables

25. **USB-C PD Cables**
    - [ ] E-marker chip specifications?
    - [ ] Maximum current rating?
    - [ ] Voltage drop at 2m length?
    - [ ] Temperature rating of insulation?
    - [ ] Flexibility in cold conditions (-20°C)?
    - [ ] Connector retention force?

---

## SECTION 6: SYSTEM INTEGRATION

### Compatibility Testing

26. **Interoperability**
    - [ ] Has INVISIO been tested with Samsung Galaxy S25?
    - [ ] Has INVISIO been tested with Tetra TH1n radio?
    - [ ] Known compatibility issues?
    - [ ] Firmware updates required?
    - [ ] Software configuration needed?

27. **Performance Metrics**
    - [ ] End-to-end audio latency (Tetra to ear)?
    - [ ] Audio quality degradation with all systems active?
    - [ ] RF interference between components?
    - [ ] Battery life with full system operational?

### Training & Support

28. **Documentation**
    - [ ] User manuals available in English?
    - [ ] Technical integration guides?
    - [ ] Troubleshooting flowcharts?
    - [ ] Video training materials?
    - [ ] Online support portal access?

29. **Warranty & Service**
    - [ ] Warranty period for Middle East deployment?
    - [ ] On-site service available in Dubai?
    - [ ] Replacement unit turnaround time?
    - [ ] Technical support hours (GMT+4)?
    - [ ] Escalation procedures?

30. **Spare Parts**
    - [ ] Recommended spare parts list?
    - [ ] Consumables replacement schedule?
    - [ ] Parts availability in region?
    - [ ] Minimum order quantities?
    - [ ] Lead times for spare parts?

---

## RESPONSE INSTRUCTIONS

Please complete all applicable sections and return via email to:  
**[Project Manager Email]**

**Required Supporting Documents:**
- Technical datasheets
- Compliance certificates
- Test reports for desert conditions
- CAD drawings for custom cables
- Integration guides

**Response Deadline:** [Date]

**Note:** Information marked as proprietary will be handled under NDA.

---

*This questionnaire is part of the Dubai Police SWAT Tactical Communication System procurement process. All information will be used solely for system design and integration purposes.*