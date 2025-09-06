# Assets Directory

This directory contains visual assets for proposals including diagrams, charts, and images.

## Organization

Assets should be organized by project:
```
assets/
├── project-name-diagram1.png
├── project-name-architecture.svg  
├── common/
│   ├── logo.png
│   └── generic-architecture.png
└── README.md
```

## Asset Types

**Diagrams**
- System architecture diagrams
- Network topology charts
- Process flow diagrams
- Integration maps

**Images** 
- Product photos
- Screenshots
- UI mockups
- Reference materials

**Common Assets**
- Corporate logos
- Generic templates
- Reusable diagrams
- Brand elements

## File Formats

Supported formats:
- **PNG** - Screenshots, photos, diagrams with transparency
- **JPG** - Photos, complex images without transparency  
- **SVG** - Scalable vector graphics (preferred for diagrams)
- **PDF** - Complex diagrams, charts from design tools

## Naming Convention

Use descriptive, project-specific names:
- `project-id-system-architecture.png`
- `project-id-network-diagram.svg`
- `client-name-integration-flow.pdf`

## Integration

Assets are referenced in YAML specs:
```yaml
sections:
  - id: system_architecture
    diagrams:
      - assets/project-name-system-architecture.png
```

**Status**: Ready for project-specific assets