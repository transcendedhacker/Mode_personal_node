# Mode_personal_node

Ultra-clean, infinitely scalable prompt library system for ComfyUI.

## What This Is

A production-grade custom node for ComfyUI that uses **pure separation of concerns** to create a maintainable, scalable prompt composition system.

### Key Features

✅ **Pure data libraries** - No syntax, no weights, no formatting in data files  
✅ **Schema-driven rules** - All logic defined in one connector file  
✅ **Content-agnostic engine** - Core code never changes, only data  
✅ **SDXL & FLUX support** - Model-specific profiles via configuration  
✅ **Infinitely scalable** - Add unlimited libraries without touching code  
✅ **Production-ready** - Clean architecture, no technical debt

---

## Architecture

```
engine/      → Generic composition logic
schema/      → Rules defining interpretation
libraries/   → Pure JSON data files
```

**Three layers, zero entanglement.**

Read [ARCHITECTURE.md](ARCHITECTURE.md) for deep dive.

---

## Quick Start

1. Copy to `ComfyUI/custom_nodes/Mode_personal_node/`
2. Restart ComfyUI
3. Find nodes under "Modular Prompts"

See [QUICKSTART.md](QUICKSTART.md) for detailed usage.

---

## Example

**Input:**
- Library: `realistic_portrait`
- Character: `Classic Beauty`
- Scene: `Apartment Evening`
- Model: `SDXL`

**Output:**
```
(A woman with soft symmetrical features:1.1), in a small apartment living room, during warm evening light, (quietly reflective mood:1.2), wearing a silk camisole, BREAK, (soft lamp light from the side:1.3), BREAK, shot on 85mm lens, professional photography
```

---

## Extending

### Add New Library

1. Create `libraries/your_theme.json`
2. Follow structure (see examples)
3. Restart ComfyUI

**No code changes needed.**

### Customize Behavior

Edit `schema/connector.json`:
- Block order
- Weights per block
- BREAK positions
- Model profiles

**No code changes needed.**

---

## Why This Architecture

**Problems solved:**
- ❌ Old: Libraries contained formatting → ✅ Now: Pure data
- ❌ Old: Weights in data → ✅ Now: In schema
- ❌ Old: Code knew content → ✅ Now: Content-agnostic
- ❌ Old: Library switching broken → ✅ Now: Works properly
- ❌ Old: 300s generation time → ✅ Now: Fast, clean prompts

**Design principles:**
- Separation of concerns
- Data ≠ Logic
- Schema-driven behavior
- Scalability without code changes

---

## File Structure

```
Mode_personal_node/
├── __init__.py                    # ComfyUI node interface
├── engine/
│   └── composer.py                # Core composition engine  
├── schema/
│   └── connector.json             # Rules and structure
├── libraries/
│   ├── realistic_portrait.json
│   ├── fantasy_theme.json
│   └── cyberpunk_urban.json
├── ARCHITECTURE.md                # Deep dive documentation
├── QUICKSTART.md                  # Usage guide
└── README.md                      # This file
```

---

## Included Libraries

1. **realistic_portrait** - Natural photography, everyday scenes
2. **fantasy_theme** - Magical settings, mystical elements
3. **cyberpunk_urban** - Neon lighting, futuristic aesthetic

Each library is pure JSON data with no embedded logic.

---

## For Power Users

- All formatting logic in `schema/connector.json`
- Weight adjustments per block
- Model-specific multipliers
- Custom BREAK positioning
- Extensible without code changes

This is how professional systems are built.

---

## License

Free to use and modify.

---

## Philosophy

**Libraries are data.**  
**Schema defines rules.**  
**Engine implements rules.**  
**Node wires it together.**

Clean. Scalable. Production-ready.

Built for people who understand separation of concerns.
