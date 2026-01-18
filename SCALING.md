# Scaling Guide

## Current Implementation

300+ atomic options across 17 compositional blocks.
All options alphabetically sorted with "None" skip option.

## Library Expansion

### From Reference Documentation

Available source material for expansion:
- AngleShot.txt: 100+ camera angles
- HairColors.txt: 40+ hair colors
- HairTexturesStyle.txt: 200+ hair styling variations
- Outfits.txt: 50+ outfit types
- RevealingOutfit.txt: 100+ outfit variations
- SexyPoses.txt: 200+ pose descriptions
- LocationsIndoor.txt: 300+ interior settings
- Atmospheres.txt: 100+ atmospheric conditions
- Filters.txt: 40+ color grading presets

### Addition Process

Edit library JSON file directly:

```json
"angle": {
  "Birds-Eye View": "bird's-eye view from above",
  "Ceiling Shot": "ceiling-mounted camera angle looking down",
  "Dutch Angle": "dutch angle, tilted perspective",
  "Extreme Low Angle": "extreme low angle from ground level",
  "Helicopter Shot": "aerial helicopter perspective"
}
```

Add entries in alphabetical order (automatic sorting occurs on load).
Restart ComfyUI after modifications.

### Multi-Library Strategy

When single library exceeds practical navigation limits (subjective, typically 1000+ options), split by context:

```
libraries/
├── comprehensive_portrait.json    → General purpose, balanced coverage
├── portrait_casual.json           → Everyday scenarios and styling
├── portrait_formal.json           → Professional and elegant contexts
├── portrait_fantasy.json          → Fantastical and imaginative elements
├── portrait_cyberpunk.json        → Technological and dystopian themes
└── portrait_historical.json       → Period-specific styling and settings
```

User switches library dropdown to change entire option set.

## None Handling

Selecting "None" in any block:
- Block completely omitted from prompt assembly
- No placeholder text inserted
- Clean, minimal composition maintained

Example workflow:
- subject: "Woman"
- hair_ornament: "None" → No ornament mentioned in output
- outfit_detail: "None" → Just outfit base, no fabric characteristics
- filter: "None" → No color grading applied

## Scale Capacity

### Current
17 blocks × ~20 average options = ~340 total selections

### Proven Capacity
17 blocks × 100 options per block = 1,700 total selections
(tested with no performance degradation)

### Theoretical Maximum
25 blocks × 100 options per block = 2,500 total selections
(untested but architecturally supported)

## Navigation at Scale

With 100 options per block, alphabetical organization provides efficient navigation:

```
A-D: 25 options
E-H: 25 options
I-L: 25 options
M-P: 25 options
Q-T: 25 options
U-Z: 25 options
```

Standard dropdown scrolling remains functional.
No search interface required if options well-named.

## Naming Conventions

For optimal alphabetical navigation:

**Good**:
- "Ceiling Shot"
- "Dutch Angle"
- "Eye-Level"
- "Low Angle"
- "Worm's-Eye View"

**Avoid**:
- "Shot from ceiling" (clusters under 'S')
- "Angle: Dutch" (prefix pollution)
- "Low-angle shot" (inconsistent formatting)

Consistency in naming structure improves navigation predictability.

## Performance Considerations

Prompt assembly performance is constant regardless of library size.
Bottlenecks occur only during:
1. Initial library loading (one-time, on ComfyUI startup)
2. Dropdown population (one-time, on node creation)

Runtime composition is O(n) where n = number of selected blocks (not total options).

## Validation Strategy

When expanding libraries:
1. Add options incrementally (10-20 at a time)
2. Test composition output for each addition batch
3. Verify alphabetical sorting correctness
4. Check for duplicate entries
5. Confirm prompt assembly remains coherent

Schema validation (future implementation) will automate consistency checking.
