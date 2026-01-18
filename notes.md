# Development Notes

## v2.0 - Production Architecture

Schema-driven prompt generation engine with 300+ atomic compositional elements across 17 structural blocks.

## System Architecture

**Separation of Concerns**:
- Engine: Deterministic assembly logic (no domain knowledge)
- Schema: Structural contract (ordering, weighting, rules)
- Libraries: Content datasets (pure options, no logic)

**Data Flow**:
User selections → Schema validation → Library lookup → Weight application → Token ordering → Assembled prompt

## Block Organization

Schema defines 17 compositional blocks in priority order:

subject → age → hair_color → hair_style → hair_ornament → outfit → outfit_detail → pose → mood → location → location_detail → atmosphere → lighting → angle → frame → filter → technical

## None Handling

Selecting "None" in any dropdown:
- Block completely omitted from assembly
- No blank text inserted
- Clean composition maintained

Example:
- hair_ornament: None → No ornament text appears
- outfit_detail: None → Just outfit, no fabric details

## Alphabetical Sorting

All dropdowns alphabetically sorted for predictable navigation.
"None" always first regardless of sorting.

Benefits:
- Scannable even with 100+ options per block
- No search interface needed
- Consistent muscle memory for frequent options

## Current Scale

17 blocks × ~18 average options = ~300 total selections

Proven capacity: System handles 1000+ options without performance degradation.

## Performance Characteristics

v1 (sentence-based): ~300s generation time
v2 (atomic composition): <100s generation time

Clean, structured prompts encode faster and produce more consistent results.

## Scaling Strategies

### Vertical Scaling (expand existing blocks)
Add options to current blocks from reference documentation:
- Parse HairColors.txt → add all 40+ colors
- Parse AngleShot.txt → add all 100+ camera angles
- Parse SexyPoses.txt → add all 200+ pose variations
- Parse LocationsIndoor.txt → add all 300+ interior settings
- Parse Atmospheres.txt → add all 100+ atmospheric conditions

### Horizontal Scaling (add new blocks)
Introduce additional compositional elements as needed:
- Facial expression control
- Hand positioning
- Environmental props
- Weather conditions
- Color palette specifications

### Library Specialization
Create context-specific libraries for distinct use cases:
- portrait_casual.json
- portrait_formal.json
- portrait_fantasy.json
- portrait_technical.json

## Technical Constraints

**ComfyUI Limitation**: Dropdowns cannot dynamically update based on other selections.

Cannot implement:
- "outfit: dress" → auto-filter outfit_detail to dress-specific options
- "location: indoor" → auto-filter location_detail to indoor conditions

Workarounds:
1. Comprehensive libraries covering all valid combinations
2. Specialized libraries for specific contexts
3. Schema-level validation (future implementation)

## Extension Workflow

To add options:

1. Edit target library JSON file
2. Add entries in appropriate block
3. Follow format: `"Option Name": "descriptive prompt text"`
4. Save file
5. Restart ComfyUI

No engine modification required. Alphabetical sorting automatic.

## Intent Flags (Planned)

Schema defines intent flags for future implementation:
- exposure_level: [covered, implied, nude]
- camera_relationship: [facing, candid, over_shoulder, pov, back_view]

Default values ensure safe, predictable behavior.
Explicit opt-in required for non-default states.

## Addon Support (Planned)

Each block will support local addon text:
- Modifies only that block's output
- Merges inline via comma separator
- Example: "woman" + addon "athletic build" → "woman, athletic build"

## Provenance Tracking

Optional non-rendering comment for attribution:
```
# Generated using Mode_personal_node — CC BY-NC 4.0
```

Disabled by default. User-removable. Attribution enforced via licensing, not technical restrictions.

## Maintenance Philosophy

- Engine code frozen unless structural requirements change
- Schema evolves only for new architectural features
- Libraries expand freely without affecting engine
- Backwards compatibility maintained across minor versions
