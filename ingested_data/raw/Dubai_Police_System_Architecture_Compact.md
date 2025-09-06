# DUBAI POLICE SWAT - TACTICAL COMMUNICATION SYSTEM

## SYSTEM ARCHITECTURE

```
         [OPERATOR HEAD]
               │
        ┌──────┴──────┐
        │ INVISIO V60 │
        │ Control Unit│
        └──────┬──────┘
               │
      ┌────────┼────────┐
      │        │        │
   LEFT EAR    │    RIGHT EAR
   [TETRA]     │    [SAMSUNG]
               │
        ┌──────┴──────┐
        │  INVISIO X7 │
        │   Headset   │
        │  39dB SNR   │
        └─────────────┘
```

## COMPONENT LAYOUT

```
    [HAND]        [BELT-L]      [BELT-R]
       │             │             │
  Samsung S25   Tetra Radio   Power Bank
       │          TH1n        42,000mAh
  Bunker Case      │          Hot-Swap
       │        26-pin           │
  Hand Mount   Connector     USB-C PD
```

## DUAL PTT CONFIGURATION

```
     ┌─────────────┐
     │  DUAL PTT   │
     ├─────────────┤
     │ LEFT │RIGHT │
     │ PTT  │ PTT  │
     └─────────────┘
          │
    ┌─────┴─────┐
    │           │
  TETRA    SAMSUNG
  Command  Team/ATAK
```

## CONNECTIVITY FLOW

```
Samsung S25 ◄──4G/5G──► Etisalat Network
     │                        │
     ▼                        ▼
  ATAK App              VoIP Services
     │
     ▼
Blue Force Tracking
```

## POWER DISTRIBUTION

```
    42,000mAh Battery
           │
    ┌──────┼──────┐
    │             │
Samsung S25   INVISIO V60
(~15 hours operation)
```

## AUDIO ROUTING

```
Tetra ──► Left Ear (Command)
Samsung ──► Right Ear (Team)
```

## ENVIRONMENTAL SPECS
- **Protection:** IP68
- **Temperature:** -20°C to 60°C
- **Humidity:** Up to 95%
- **Drop Test:** 2 meters
- **Operations:** Desert/Urban

## MOUNTING SYSTEM

```
    TACTICAL VEST
  ┌─────────────┐
  │ [MOLLE]     │
  │   ├─Power   │
  │   └─Tetra   │
  │             │
  │ Cable Mgmt  │
  └─────────────┘
```

## KEY FEATURES

### Audio System
- INVISIO V60 II Control Unit
- INVISIO X7 In-Ear Headset
- Dual-channel audio mixing
- 39dB SNR protection

### Hand Device
- Samsung Galaxy S25
- Bunker Supply Tactical Case
- Glove-compatible touchscreen
- Anti-glare protection
- Quick-release mechanism

### Power System
- 42,000mAh capacity
- Hot-swappable design
- 15-hour operation
- USB-C PD distribution

### Connectivity
- 4G/5G cellular (Etisalat)
- ATAK software ready
- Blue Force Tracking
- VoIP integration

### PTT Operation
- Left PTT: Tetra command net
- Right PTT: Samsung/ATAK team
- Independent channel control

## OPERATIONAL WORKFLOW

```
START ──► POWER ON ──► MISSION ──► END
  │          │           │         │
  └─Test     └─Operate   └─PTT     └─Standby
```

## SYSTEM INTEGRATION
- Snag-free cable routing
- MOLLE vest integration
- Quick-disconnect points
- Desert tan color scheme