# PROFESSIONAL PROMPT GENERATOR
## For Dubai Police SWAT Technical Images
### Optimized for DALL-E 3, Midjourney, Stable Diffusion

---

## PROMPT GENERATION TEMPLATE

### Step 1: Define Your Need
What do you need to visualize?
- [ ] System overview
- [ ] Component detail
- [ ] Integration diagram
- [ ] Operational scenario
- [ ] Technical comparison

### Step 2: Use This Formula

```
[STYLE] + [SUBJECT] + [DETAILS] + [ENVIRONMENT] + [TECHNICAL SPECS] + [OUTPUT FORMAT]
```

---

## AUTOMATED PROMPT TEMPLATES

### 1. TECHNICAL SYSTEM OVERVIEW
```
INPUT: {component_name}
OUTPUT: "Technical illustration, isometric view, {component_name}, exploded diagram showing internal components, white background, CAD engineering drawing style, dimension lines with measurements, professional technical documentation, no shadows, high contrast line art, labeled parts, assembly sequence numbers, --ar 16:9 --style raw --quality 2"
```

### 2. TACTICAL OPERATOR VIEW
```
INPUT: {equipment_position}
OUTPUT: "Professional military technical diagram, tactical operator front view, {equipment_position}, black tactical vest with MOLLE webbing, clean white background, technical manual illustration style, no artistic effects, dimension arrows, component callouts, MIL-STD documentation quality, --ar 16:9 --s 50"
```

### 3. COMPONENT DETAIL
```
INPUT: {device_name}, {dimensions}
OUTPUT: "Ultra-detailed technical drawing of {device_name}, exact dimensions {dimensions}, orthographic projection showing front/side/top views, engineering blueprint style, white background, black lines only, ISO standard technical drawing, manufacturing specifications visible, tolerance markings, material callouts"
```

### 4. CABLE/CONNECTION DIAGRAM
```
INPUT: {cable_type}, {connectors}
OUTPUT: "Technical wiring diagram, {cable_type} with {connectors}, pinout diagram included, wire color coding, EMI/RFI shielding visible, cross-section view, bend radius specifications, connector gender clearly shown, AWG ratings, professional electrical schematic style"
```

### 5. ENVIRONMENTAL TESTING
```
INPUT: {test_condition}, {temperature}
OUTPUT: "Technical test environment illustration, {test_condition} at {temperature}, cutaway view showing heat dissipation, airflow arrows, temperature gradient visualization, component stress points highlighted, desert environment, professional thermal analysis style, scientific accuracy"
```

---

## PLATFORM-SPECIFIC OPTIMIZATIONS

### DALL-E 3 (Your Current Setup)
```python
def generate_dalle_prompt(component, style="technical"):
    base = f"Create a {style} illustration of {component}"
    specs = "photorealistic technical drawing, white background, professional CAD style"
    avoid = "no artistic interpretation, no shadows, no backgrounds"
    return f"{base}, {specs}, {avoid}"
```

### Midjourney
```python
def generate_midjourney_prompt(component, style="technical"):
    base = f"/imagine {style} diagram {component}"
    params = "--ar 16:9 --style raw --s 50 --q 2"
    weights = "technical::3, artistic::-1, professional::2"
    return f"{base} {weights} {params}"
```

### Stable Diffusion
```python
def generate_sd_prompt(component, style="technical"):
    positive = f"{style} drawing, {component}, blueprint, CAD, technical"
    negative = "artistic, painterly, shadows, background, people, weapons"
    settings = "Steps: 30, Sampler: DPM++, CFG: 7"
    return {"positive": positive, "negative": negative, "settings": settings}
```

---

## QUICK PROMPT BUILDER

### YOUR DUBAI POLICE SWAT SYSTEM

**Copy and modify these ready-to-use prompts:**

#### System Overview
```
"Technical illustration of tactical communication system, operator wearing black tactical vest with chest-mounted INVISIO V60 II control unit (70×63×25mm), Samsung Galaxy S23 Ultra on left forearm in tan case, Tetra radio on left hip, dual battery pack on right hip, 4 colored cables (orange, blue, 2 black) visible and labeled, white background, professional military technical manual style, dimension lines, component labels, no artistic effects --ar 16:9 --style raw"
```

#### INVISIO V60 II Detail
```
"Ultra-detailed technical drawing of INVISIO V60 II control unit, black tactical communication device, 70mm × 63mm × 25mm dimensions shown, 4 PTT buttons in 2×2 configuration clearly visible, 3 cable ports on bottom edge, LED status indicator, exploded view showing internal PCB layout, white background, ISO standard technical drawing, professional product documentation style"
```

#### Power System
```
"Technical diagram of dual 21,000mAh hot-swappable battery system, two rectangular LiFePO4 battery packs (150×80×25mm each), hot-swap controller module between them, LED indicators showing charge status, USB-C PD ports visible, connection diagram with pinouts, white background, electrical schematic style, professional power system documentation"
```

#### Integration on Operator
```
"Professional technical illustration, tactical operator front view in standing position, complete Dubai Police SWAT communication system visible, all components labeled with leader lines, color-coded cable routing shown, ergonomic reach zones indicated, white background, military field manual illustration style, no weapons, clear technical documentation"
```

---

## ADVANCED TECHNIQUES

### 1. Multi-View Generation
```
PROMPT: "{component} shown in 6 views: front, back, left, right, top, bottom, arranged in standard orthographic projection layout, technical drawing style"
```

### 2. Exploded Assembly
```
PROMPT: "{system} exploded view, components separated vertically, assembly sequence numbered 1-10, connection lines showing assembly path, torque specifications"
```

### 3. Cutaway Technical
```
PROMPT: "{device} cutaway view revealing internal components, PCB visible, component labels, cross-section hatching, technical manual illustration"
```

### 4. Comparison Diagram
```
PROMPT: "Split screen comparison, left side: {old_system}, right side: {new_system}, matching angles, clear labeling, advantages highlighted"
```

---

## QUALITY CHECKLIST

Before using any prompt, verify:
- [ ] Specific dimensions included
- [ ] Materials/colors specified
- [ ] Background defined (usually white)
- [ ] Style clearly stated (technical/CAD/manual)
- [ ] Unwanted elements excluded
- [ ] Platform-specific parameters added

---

## TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Too artistic | Add "technical drawing, no artistic interpretation" |
| Wrong size | Include exact mm dimensions |
| Bad perspective | Specify "orthographic" or "isometric" |
| Missing details | Add "ultra-detailed" or "high detail" |
| Wrong style | Use "MIL-STD" or "ISO technical standard" |

---

## BATCH PROCESSING

For multiple images, use this template:

```bash
# Base prompt
BASE="Technical illustration, white background, professional documentation"

# Components
ITEMS=("INVISIO V60" "Samsung S23" "Battery Pack" "Cable System")

# Generate all
for item in "${ITEMS[@]}"; do
    echo "$BASE, $item, detailed view with dimensions"
done
```

---

## FREE ALTERNATIVES

If API credits run out:
1. **Hugging Face Spaces** (free FLUX model)
2. **Bing Image Creator** (free DALL-E access)
3. **Leonardo.ai** (free tier available)
4. **Playground AI** (free credits daily)

---

**Remember:** 
- Technical accuracy > artistic beauty
- Include measurements always
- White backgrounds for documentation
- Avoid shadows and effects
- Label everything clearly

---

*Use these prompts with your installed MCP servers or copy directly to web interfaces*