# SYSTEM INTEGRATION DIAGRAMS
**Version: v1.0**
## Dubai Police SWAT Dismounted Vest Kit
### Architecture and Connectivity Overview

---

## CONFIGURATION 1: SILVUS NEXUS INTEGRATED SYSTEM

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     TACTICAL VEST PLATFORM                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    STREAMCASTER NEXUS™                    │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │              SM5200 MANET RADIO                   │   │    │
│  │  │   • 2W Native / 4W Effective Power                │   │    │
│  │  │   • MN-MIMO Waveform                             │   │    │
│  │  │   • AES256 Encryption                            │   │    │
│  │  └────────────┬─────────────────────────────────────┘   │    │
│  │                │                                         │    │
│  │  ┌─────────────┴──────────┬─────────────┬──────────┐   │    │
│  │  │   PTT L/R Audio        │  Ethernet   │   USB    │   │    │
│  │  │   Interface             │  Port       │  Ports   │   │    │
│  │  └─────────┬───────────────┴─────────────┴──────────┘   │    │
│  └────────────┼─────────────────────────────────────────────┘    │
│               │                                                   │
│     ┌─────────┴──────────┬──────────────┬──────────────┐        │
│     │                    │              │              │        │
│     ▼                    ▼              ▼              ▼        │
│ ┌─────────┐      ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│ │ INVISIO │      │ Samsung  │   │  MOHOC   │   │ Antenna  │    │
│ │ V60 II  │◄────►│ Galaxy   │   │  Camera  │   │  System  │    │
│ │ + X7    │      │   S25    │   │(Optional)│   │  (MIMO)  │    │
│ └─────────┘      └──────────┘   └──────────┘   └──────────┘    │
│                                                                   │
└───────────────────────────────────────────────────────────────┘
```

### Detailed Connection Diagram - NEXUS Configuration

```
                        CHEST-MOUNTED ASSEMBLY
    ┌──────────────────────────────────────────────────────────┐
    │                                                          │
    │  Antenna #1 (TNC)          Antenna #2 (TNC)            │
    │       │                         │                       │
    │       └────┬────────────────────┘                       │
    │            │                                             │
    │     ┌──────▼──────────────────────────────┐            │
    │     │     STREAMCASTER NEXUS™             │            │
    │     │  ┌───────────────────────────┐      │            │
    │     │  │  3-Point Snap Lock Mount  │      │            │
    │     │  └───────────────────────────┘      │            │
    │     │                                      │            │
    │     │  Power: USB-PD (9V@3A) or 9-32VDC  │            │
    │     │  Audio: Integrated PTT (L/R)        │            │
    │     │  Data:  1x ETH, 2x USB, 1x RS232    │            │
    │     └─────┬───────┬────────┬──────────────┘            │
    │           │       │        │                            │
    │    Audio  │  USB  │   ETH  │                            │
    │      Cable│ Type-C│  Cable │                            │
    │           ▼       ▼        ▼                            │
    │    ┌──────────┐ ┌────────────┐ ┌───────────┐          │
    │    │ INVISIO  │ │  Samsung   │ │  Network  │          │
    │    │  V60 II  │ │  Galaxy    │ │  Device   │          │
    │    │    +     │ │    S25     │ │(Optional) │          │
    │    │   X7     │ │   (ATAK)   │ └───────────┘          │
    │    └────┬─────┘ └────────────┘                         │
    │         │                                               │
    │    Dual PTT                                             │
    │    Control                                              │
    │                                                          │
    └──────────────────────────────────────────────────────────┘
```

### Power Distribution - NEXUS

```
                    POWER FLOW DIAGRAM
    
    External Power Source
    (USB-PD or 9-32VDC)
            │
            ▼
    ┌───────────────┐
    │  NEXUS Power  │
    │  Management   │
    └───────┬───────┘
            │
    ┌───────┴────────┬─────────────┬──────────────┐
    ▼                ▼             ▼              ▼
 SM5200          INVISIO       Samsung S25    MOHOC
 Radio           V60 II         (USB-PD)     Camera
(Internal)    (From Radio)                  (Battery)
```

---

## CONFIGURATION 2: KAGWERKS DOCK-LITE MODULAR SYSTEM

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     TACTICAL VEST PLATFORM                       │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │ KAGWERKS       │  │  SILVUS        │  │   INVISIO      │   │
│  │ DOCK-LITE      │  │  SL5200        │  │   V60 II ADP   │   │
│  │                │  │  MANET Radio   │  │                │   │
│  │ • 3-Port USB   │  │                │  │ • Audio Hub    │   │
│  │ • ISW Support  │  │ • 2W/4W Power  │  │ • Data Bridge  │   │
│  │ • S25 Mount*   │  │ • MN-MIMO      │  │ • Power Dist   │   │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘   │
│           │                    │                    │           │
│           │         ┌──────────┴──────────┐         │           │
│           │         │                      │         │           │
│     ┌─────▼─────┐   │   ┌──────────┐     │   ┌─────▼─────┐    │
│     │ Samsung   │◄──┼──►│ Antenna  │     └──►│  INVISIO  │    │
│     │ Galaxy    │   │   │  System  │         │    X7     │    │
│     │   S25     │   │   │  (MIMO)  │         │  Headset  │    │
│     │  (ATAK)   │   │   └──────────┘         └───────────┘    │
│     └───────────┘   │                                           │
│                     │   ┌──────────┐                           │
│                     └──►│  MOHOC   │                           │
│                         │  Camera  │                           │
│                         │(Optional)│                           │
│                         └──────────┘                           │
│                                                                   │
└───────────────────────────────────────────────────────────────┘
```

### Detailed Connection Diagram - DOCK-LITE Configuration

```
                    MODULAR COMPONENT LAYOUT
    
    ┌──────────────────────────────────────────────────────┐
    │                   CHEST RIG / VEST                    │
    │                                                        │
    │  ┌─────────────────────┐    ┌────────────────────┐  │
    │  │   KAGWERKS DOCK     │    │   Radio Pouch      │  │
    │  │  ┌──────────────┐   │    │  ┌──────────────┐  │  │
    │  │  │  Samsung S25 │   │    │  │ Silvus       │  │  │
    │  │  │    Mounted   │   │    │  │ SL5200       │  │  │
    │  │  └──────┬───────┘   │    │  └──────┬───────┘  │  │
    │  │         │           │    │         │          │  │
    │  │   USB-C Hub:        │    │    TNC Ports:     │  │
    │  │   Port 1 ───────────┼────┼───► Antenna #1    │  │
    │  │   Port 2 ───────────┼────┼───► Antenna #2    │  │
    │  │   Port 3 ──┐        │    │                    │  │
    │  └────────────┼────────┘    └────────────────────┘  │
    │               │                                       │
    │          Cable│Management                            │
    │               │System                                │
    │               ▼                                       │
    │  ┌──────────────────────────────────────┐           │
    │  │        INVISIO V60 II ADP            │           │
    │  │   COM1 ◄──── Radio Cable ────────────┘           │
    │  │   COM2 ◄──── EUD Cable                           │
    │  │   COM3 ◄──── Spare/Future                        │
    │  │   USB  ◄──── Power/Data                          │
    │  └─────────────┬────────────────────────┘           │
    │                 │                                     │
    │                 └──► INVISIO X7 Headset             │
    │                                                        │
    └────────────────────────────────────────────────────┘
```

### Cable Routing Diagram - DOCK-LITE

```
           CABLE MANAGEMENT SCHEMATIC
    
    Samsung S25 (DOCK)
         │
         ├── USB-C ──► INVISIO V60 ADP (Data/Audio)
         ├── USB-C ──► Silvus SL5200 (Control)
         └── USB-C ──► Power Bank (Backup)
    
    Silvus SL5200
         │
         ├── TNC ────► Antenna #1 (MIMO)
         ├── TNC ────► Antenna #2 (MIMO)
         ├── Audio ──► INVISIO V60 (COM1)
         └── Power ──► Internal Battery
    
    INVISIO V60 II ADP
         │
         ├── Headset ─► X7 In-Ear System
         ├── PTT ────► Dual Control
         ├── USB ────► Digital Audio
         └── Power ──► From Radio/USB
```

---

## ANTENNA CONFIGURATION (BOTH SYSTEMS)

### MIMO Antenna Layout

```
              VEST-MOUNTED ANTENNA SYSTEM
    
    Front View:                    Side View:
    
    ┌─────────┐                   Antenna #1
    │    O    │ <- Helmet            │
    │   ╱│╲   │                      │ 
    │  ╱ │ ╲  │                      ▼
    │ ┌──┴──┐ │              ┌──────────────┐
    │ │Vest │ │              │              │
    │ │     │ │              │    MOLLE     │
    │ │ Ant1│◄├──────────────┤   Webbing    │
    │ │     │ │              │              │
    │ │ Ant2│◄├──────────────┤              │
    │ │     │ │              └──────────────┘
    │ └─────┘ │                      ▲
    │         │                      │
    └─────────┘                  Antenna #2
    
    Separation: >λ/4 (minimum 7.5cm @ 1GHz)
    Pattern: Omnidirectional
    Polarization: Vertical
```

---

## DATA FLOW ARCHITECTURE

### NEXUS Data Flow

```
    ATAK Application
         │
         ▼
    Samsung S25
         │
    ┌────┴────┐
    │   USB   │
    └────┬────┘
         ▼
    NEXUS Hub ◄────► SM5200 Radio ◄────► MANET Network
         │                                      ▲
         ▼                                      │
    Audio System                          Other Units
```

### DOCK-LITE Data Flow

```
    ATAK Application
         │
         ▼
    Samsung S25
         │
    ┌────┴────────┬──────────┐
    │  DOCK Hub   │          │
    └─────┬───────┘          │
          │                  │
          ▼                  ▼
    INVISIO V60 ADP    Silvus SL5200
          │                  │
          ▼                  ▼
    Audio Output       MANET Network
                             ▲
                             │
                       Other Units
```

---

## INTEGRATION NOTES

### Critical Integration Points

1. **Power Management**
   - NEXUS: Centralized power distribution
   - DOCK-LITE: Distributed power systems

2. **Cable Requirements**
   - NEXUS: ~3 primary cables
   - DOCK-LITE: ~7-8 cables required

3. **Weight Distribution**
   - NEXUS: Center chest concentration
   - DOCK-LITE: Distributed across vest

4. **Maintenance Access**
   - NEXUS: Single unit service
   - DOCK-LITE: Component-level access

5. **Training Complexity**
   - NEXUS: Single system operation
   - DOCK-LITE: Multiple system coordination

---

## MOUNTING SPECIFICATIONS

### Vest Integration Points

```
         MOLLE WEBBING LAYOUT
    
    Row 1: ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
    Row 2: ├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
    Row 3: ├─┼─NEXUS/DOCK──┼─┼─┤
    Row 4: ├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
    Row 5: ├─Radio─┼─┼─Pouch─┼─┤
    Row 6: └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
    
    Spacing: 1" horizontal, 1.5" vertical
    Load: <5kg per attachment point
```

---

*Diagrams represent conceptual integration - actual implementation may vary*
*All connections subject to final vendor specifications*