# Architecture Documentation

## Philosophy

**Pure Separation of Concerns**

- **Libraries** = Pure data (no syntax, no weights, no formatting)
- **Schema** = Rules defining interpretation (ordering, weights, model profiles)
- **Engine** = Content-agnostic composition logic
- **Node** = Minimal interface wiring it all together

This allows infinite scalability without touching code.

---

## Folder Structure

```
Mode_personal_node/
├── __init__.py                 # ComfyUI node interface
├── engine/
│   └── composer.py             # Core composition engine
├── schema/
│   └── connector.json          # Rules and structure
└── libraries/
    ├── realistic_portrait.json
    ├── fantasy_theme.json
    └── cyberpunk_urban.json
```

---

## How It Works

### 1. Libraries (Pure Data)

Libraries contain ONLY text descriptions, organized into blocks:

```json
{
  "meta": {
    "name": "Library Name",
    "description": "What this library is for"
  },
  "blocks": {
    "character": {
      "Option Name": "Pure text description"
    },
    "scene": { ... },
    "emotion": { ... }
  }
}
```

**NO weights, NO BREAK, NO syntax** - just clean data.

### 2. Schema (Rules)

The connector defines HOW to interpret libraries:

```json
{
  "structure": {
    "block_order": ["character", "scene", ...],
    "separator": ", ",
    "break_positions": [4, 6]
  },
  "weights": {
    "character": 1.1,
    "emotion": 1.2
  },
  "models": {
    "sdxl": { "weight_multiplier": 1.0 },
    "flux": { "weight_multiplier": 0.85 }
  }
}
```

### 3. Engine (Logic)

The composer reads schema + libraries and produces final prompts:

```python
composer.compose(
    library_id="realistic_portrait",
    selections={"character": "Classic Beauty", ...},
    model_profile="sdxl"
)
```

Output:
```
(A woman with soft features:1.1), in apartment, ...
```

### 4. Node (Interface)

Minimal ComfyUI wrapper that exposes dropdowns and calls composer.

---

## Adding New Libraries

1. Create `libraries/your_theme.json`
2. Follow the structure:
   ```json
   {
     "meta": { "name": "Theme Name" },
     "blocks": {
       "character": {},
       "scene": {},
       "emotion": {},
       "wardrobe": {},
       "photography": {},
       "technical": {}
     }
   }
   ```
3. Restart ComfyUI
4. New library appears in dropdown

**No code changes needed.**

---

## Customizing Behavior

### Change block order:
Edit `schema/connector.json` → `structure.block_order`

### Change weights:
Edit `schema/connector.json` → `weights`

### Add BREAK positions:
Edit `schema/connector.json` → `structure.break_positions`

### Adjust model profiles:
Edit `schema/connector.json` → `models.sdxl` or `models.flux`

---

## Model Profiles

### SDXL
```json
"sdxl": {
  "enable_weights": true,
  "weight_multiplier": 1.0
}
```

### FLUX
```json
"flux": {
  "enable_weights": true,
  "weight_multiplier": 0.85
}
```

FLUX needs lighter weights, so multiplier is 0.85.

---

## Why This Architecture

**Problems with old system:**
- Libraries contained formatting → hard to maintain
- Weights hardcoded in data → can't change globally
- Node code knew about content → not scalable
- Library switching didn't work → dropdowns didn't reload

**This system:**
- ✅ Libraries are pure data → easy to create/maintain
- ✅ Schema defines all rules → change once, affects all
- ✅ Engine is content-agnostic → infinitely scalable
- ✅ Clean separation → each part does one thing well

---

## Performance

**Old system: 300s generation**
- Likely caused by malformed prompts or inefficient encoding

**New system:**
- Clean prompt generation
- No unnecessary tokens
- Proper BREAK placement
- Should return to <100s generation

---

## Migration Notes

### From Legacy Dropdown System

**Old:**
```json
{
  "character": {
    "Name": "(description:1.1) BREAK stuff"
  }
}
```

**New:**
```json
{
  "blocks": {
    "character": {
      "Name": "description"
    }
  }
}
```

Weights and formatting come from schema, not data.

---

## Future Extensibility

Want hierarchical dropdowns? Add to schema:

```json
"dropdown_hierarchy": {
  "character_type": {
    "type": "category",
    "options": ["Natural", "Fantasy", "Cyberpunk"]
  },
  "character": {
    "depends_on": "character_type",
    "filter_by": "category"
  }
}
```

Engine stays the same, just reads new schema rules.

---

## Key Principle

**Data ≠ Logic**

Libraries should be pure content that anyone can edit.

Schema should define interpretation rules.

Engine should implement those rules without knowing the content.

This is how you build scalable systems.
