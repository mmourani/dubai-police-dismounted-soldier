# AI IMAGE GENERATION PROMPTS
## Technical Diagrams for Dubai Police SWAT System

**Purpose:** Standardized prompts for generating consistent technical visualizations  
**Platforms:** DALL-E 3, Midjourney, Stable Diffusion  
**Last Updated:** January 29, 2025

---

## 1. SYSTEM OVERVIEW DIAGRAM

### DALL-E 3 Prompt
```
Create a technical illustration of a tactical operator from the front view, 
standing position, wearing a black tactical vest with MOLLE webbing. Show:
- INVISIO V60 II control unit (70×63×25mm black box) centered on chest with 4 visible buttons
- Samsung Galaxy S25 in tan Bunker case (160×82×14mm) on LEFT forearm with 3 black velcro straps
- Tetra radio (140×60×35mm) in tan MOLLE pouch on left hip
- Dual battery pack (two 150×80×25mm units) in tan pouch on right hip
- 4 visible cables: orange (radio to control), blue (phone to control), 2 black (power)
- White background, professional CAD-style technical drawing with measurements
- No helmet, clear face visibility, neutral expression
- Include dimension lines and labels for each component
Style: Technical documentation, clean lines, high contrast
```

### Midjourney Prompt
```
/imagine technical diagram tactical communication system, front view operator, 
black tactical vest MOLLE webbing, chest-mounted control unit 4 buttons::2, 
left forearm Samsung phone tan case velcro straps::2, left hip radio pouch, 
right hip dual battery system, 4 colored cables visible orange blue black::1, 
white background, CAD technical illustration, dimension lines, component labels, 
professional military documentation style::3, photorealistic::-1, artistic::-1 
--ar 16:9 --style raw --s 50 --v 6
```

### Stable Diffusion Prompt
```
Positive: technical diagram, tactical operator front view, black tactical vest, 
MOLLE webbing, chest control unit with buttons, forearm phone mount, 
hip radio pouch, battery system, cable routing, white background, 
CAD drawing style, dimension lines, technical labels, military documentation

Negative: helmet, goggles, face covering, weapons, artistic, painterly, 
photorealistic, shadows, complex background, side view, action pose

Settings: Steps: 30, Sampler: DPM++ 2M Karras, CFG: 7, Size: 1024x768
```

---

## 2. COMPONENT DETAIL VIEWS

### INVISIO V60 II Control Unit
```
Ultra-detailed technical drawing of INVISIO V60 II control unit:
- Exact dimensions: 70mm × 63mm × 25mm
- Matte black military-grade plastic housing
- 4 PTT buttons in 2×2 configuration, each 15mm diameter
- 3 cable ports on bottom edge
- LED status indicator (green)
- Mounting clips on back
- Include exploded view showing internal layout
- White background, isometric projection
- Professional product documentation style
```

### Samsung S25 in Bunker Case
```
Technical illustration of Samsung Galaxy S25 in Bunker MAAK tactical case:
- Phone dimensions: 146.3 × 70.9 × 7.6mm
- Case adds 14mm thickness total
- Tan/coyote brown color (Federal Standard 30219)
- MAAKLOCK mounting points visible
- USB-C port with dust cover
- Screen protector installed
- Show both front view and side profile
- Include mounting strap configuration
- Technical drawing style with measurements
```

### Power System Configuration
```
Detailed technical diagram of dual battery hot-swap power system:
- Two batteries: each 150mm × 80mm × 25mm
- LiFePO4 cells visible through transparent case
- LED indicators: 4 green lights per battery
- USB-C output ports: 2 per battery
- Hot-swap controller module between batteries
- Connection cables and pinouts shown
- Exploded view with component labels
- White background, engineering drawing style
```

---

## 3. CABLE ROUTING DIAGRAM

### Vest Integration View
```
Technical illustration showing cable routing through tactical vest:
- Top-down view of opened tactical vest
- MOLLE webbing grid clearly visible
- Cable paths marked with colored lines:
  * Orange: Tetra to INVISIO (60cm)
  * Blue: Samsung to INVISIO (50cm)
  * Black (2×): Power cables (80cm, 40cm)
- Cable management points every 15cm
- Velcro keepers and routing channels
- Component positions clearly marked
- Professional wiring diagram style
```

---

## 4. OPERATIONAL VIEWS

### Mission-Ready Configuration
```
Professional technical illustration of fully equipped operator:
- 3/4 view angle showing all components
- Operator in tactical stance (not action pose)
- All connections visible and labeled
- Power flow diagram overlay
- Audio routing visualization (left/right ear)
- Data flow indicators
- Desert environment background (subtle)
- Photorealistic rendering with technical annotations
Style: Military technical manual illustration
```

### Hand Signals with System
```
Technical diagram showing PTT button operation:
- Close-up of hand positions for each PTT button
- 4 separate hand positions illustrated
- Button functions labeled:
  * Button 1: Tetra Command
  * Button 2: Team Direct
  * Button 3: ATAK Group
  * Button 4: Emergency
- Ergonomic reach zones indicated
- Gloved hand for reference
- Clean technical illustration style
```

---

## 5. EXPLODED VIEW DIAGRAM

### Complete System Exploded
```
Comprehensive exploded view technical diagram:
- All components separated vertically
- Connection lines showing assembly
- Each component labeled with:
  * Part number
  * Description
  * Key specifications
- Assembly sequence numbered
- Torque specifications for connections
- Color-coded by subsystem:
  * Audio: Blue
  * Power: Red
  * Data: Green
  * Mounting: Gray
- White background, CAD style
- Professional assembly manual quality
```

---

## 6. COMPARISON DIAGRAMS

### Before/After Configuration
```
Split-screen technical comparison:
LEFT SIDE - Current System:
- Basic radio setup
- Handheld device
- Separate components
- Multiple cables

RIGHT SIDE - New System:
- Integrated configuration
- Forearm-mounted device
- Unified control unit
- Organized cable management

Style: Clean technical comparison
Labels: Clear advantages highlighted
```

---

## 7. ENVIRONMENTAL TESTING

### Desert Operations View
```
Technical illustration of system in extreme conditions:
- Operator silhouette with system
- Temperature indicators: 50°C ambient
- Sand/dust particles (subtle)
- Heat dissipation arrows from components
- Battery performance graph overlay
- Sunlight angle and intensity indicated
- Component temperature readings
- Professional environmental test documentation style
```

---

## PROMPT OPTIMIZATION TIPS

### For Best Results:

1. **DALL-E 3:**
   - Use specific measurements
   - Describe materials and colors precisely
   - Request "technical documentation style"
   - Avoid artistic interpretations

2. **Midjourney:**
   - Use weight modifiers (::2) for important elements
   - Negative weights for unwanted elements (::-1)
   - Include --style raw for less artistic interpretation
   - Lower stylize value (--s 50) for technical accuracy

3. **Stable Diffusion:**
   - Use negative prompts extensively
   - Higher CFG (7-9) for prompt adherence
   - DPM++ samplers for technical details
   - Upscale for final resolution

### Common Issues & Solutions:

| Issue | Solution |
|-------|----------|
| Wrong component size | Include exact dimensions in mm |
| Artistic style | Add "technical drawing" repeatedly |
| Wrong mounting position | Specify "LEFT forearm" clearly |
| Too many cables | State "exactly 4 cables visible" |
| Face covered | Add "no helmet, clear face" |

---

## IMAGE POST-PROCESSING

### Recommended Edits:
1. Add dimension lines in vector software
2. Insert component labels and callouts
3. Adjust colors to match Federal Standards
4. Add company logos and headers
5. Export at 300 DPI for print documentation

### Software Tools:
- Adobe Illustrator: Vector cleanup
- Figma: Quick annotations
- Draw.io: Technical diagrams
- Inkscape: Open-source alternative

---

## USAGE RIGHTS & LICENSING

**DALL-E 3:** Commercial use permitted with ChatGPT Plus  
**Midjourney:** Commercial use with paid subscription  
**Stable Diffusion:** Open license, commercial use allowed  

**Important:** Always verify latest terms of service before commercial use.

---

*These prompts are optimized for generating technical documentation visuals for the Dubai Police SWAT project. Adjust parameters based on specific platform capabilities and requirements.*