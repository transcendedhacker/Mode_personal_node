# Changelog

## v2.0.0 - Schema-Driven Architecture

### Structural Changes

**Before (v1.x)**:
- 5-10 options per category
- Full sentences in dropdown options
- Approximately 80 total selections available
- Tightly coupled engine and content

**After (v2.0)**:
- 300+ atomic options across 17 compositional blocks
- Schema-driven architecture with strict separation of concerns
- Alphabetically sorted dropdown navigation
- "None" option for selective block skipping
- Intent flag preparation for future explicit control

### Architecture

```
Mode_personal_node/
├── engine/composer.py      → Deterministic assembly logic
├── schema/connector.json   → Structural contract and rules
└── libraries/*.json         → Content-only option datasets
```

### Library Structure

Example library block counts (comprehensive_portrait.json):
- subject: 5 options
- age: 7 options
- hair_color: 27 options
- hair_style: 22 options
- hair_ornament: 14 options
- outfit: 29 options
- outfit_detail: 10 options
- pose: 20 options
- mood: 15 options
- location: 15 options
- location_detail: 10 options
- atmosphere: 15 options
- lighting: 14 options
- angle: 18 options
- frame: 10 options
- filter: 15 options
- technical: 12 options

Total: 258 options in base library

### Features

**Alphabetical Sorting**: All dropdown options auto-sorted A-Z for predictable navigation. "None" always appears first.

**None Behavior**: Selecting "None" completely omits that block from composition. No blank text, clean assembly.

**Atomic Composition**: Each option represents a single compositional element. Multiple selections compose into structured prompts.

**Scalability**: System architecture supports thousands of options across unlimited libraries without engine modification.

### Example Composition

**Input Selections**:
- subject: "Woman"
- age: "23-27"
- hair_color: "Platinum Blonde"
- outfit: "Silk Slip Dress"
- pose: "Over Shoulder"
- (other blocks: None)

**Output**:
```
A woman 23-27 years old with platinum blonde hair, wearing red silk slip dress with spaghetti straps, (turning back to camera, looking over shoulder:1.2), photorealistic, sharp focus, highly detailed, 8k
```

### Scaling Strategy

**Current**: 258 options in base library
**Capacity**: System handles 1000+ options per library, unlimited libraries

**Multi-Library Approach**: For specialized contexts, create focused libraries:
- comprehensive_portrait.json (general purpose)
- cyberpunk_neon.json (genre-specific)
- Additional libraries as needed

Switch library dropdown to change entire option context.

### Technical Details

**ComfyUI Limitation**: Dropdowns cannot dynamically update based on other selections. Workaround is comprehensive libraries covering all combinations, or context-specific library switching.

**Weighting**: Model-specific weight multipliers applied to atmospheric and technical blocks (configurable in schema).

**BREAK Tokens**: Inserted at schema-defined positions for token priority control.

**Caching**: Option lists cached per library-block pair for performance.

### Future Extensions

Content expansion planned from reference documentation:
- Hair colors: 27 → 40+ options
- Camera angles: 18 → 100+ options
- Poses: 20 → 200+ options
- Locations: 15 → 300+ options
- Atmospheric conditions: 15 → 100+ options

All expansions require only library file edits, never engine modifications.
