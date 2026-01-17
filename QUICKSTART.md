# Quick Start Guide

## Installation

1. **Copy folder:**
   ```
   E:/Mode_personal_node/ → ComfyUI/custom_nodes/Mode_personal_node/
   ```

2. **Restart ComfyUI**

3. **Find nodes:**
   Right-click → Modular Prompts
   - Modular Prompt Composer
   - Modular Negative Prompt

---

## Basic Usage

### Simple Workflow

```
[Modular Prompt Composer] → [CLIP Text Encode +] ┐
                                                   ├→ [KSampler]
[Modular Negative Prompt]  → [CLIP Text Encode -] ┘
```

### Using the Composer

1. **Select Library** - Pick theme (realistic_portrait, fantasy_theme, etc.)
2. **Select Model Profile** - SDXL or FLUX
3. **Choose options** - One from each category dropdown
4. **Generate**

---

## Example

**Settings:**
- Library: `realistic_portrait`
- Model: `sdxl`
- Character: `Classic Beauty`
- Scene: `Apartment Evening`
- Emotion: `Contemplative`
- Wardrobe: `Silk Camisole`
- Photography: `Warm Lamp`
- Technical: `Portrait 85mm`

**Output:**
```
(A woman with soft symmetrical features, natural facial proportions, calm human expression, subtle makeup, realistic skin texture:1.1), in a small apartment living room, during warm evening light, (quietly reflective mood, sitting with legs loosely crossed, relaxed posture:1.2), wearing a silk camisole with soft folds, fitted shorts, natural draping, BREAK, (soft lamp light from the side, diffused warm glow, calm atmosphere:1.3), BREAK, shot on 85mm lens, cinematic focus separation, soft bokeh background
```

---

## Adding Your Own Library

1. **Create file:**
   ```
   libraries/my_theme.json
   ```

2. **Use template:**
   ```json
   {
     "meta": {
       "name": "My Theme",
       "description": "Description"
     },
     "blocks": {
       "character": {
         "Option 1": "Description text"
       },
       "scene": {},
       "emotion": {},
       "wardrobe": {},
       "photography": {},
       "technical": {}
     }
   }
   ```

3. **Restart ComfyUI**

4. **Use it** - Appears in Library dropdown

---

## Tips

### For SDXL
- Weights are applied automatically (1.1, 1.2, 1.3)
- Use quality keywords in Technical block

### For FLUX
- Weights are reduced automatically (×0.85)
- More natural language works better
- Less aggressive negative prompts needed

### General
- Keep libraries focused on one theme
- 5-10 options per block is ideal
- Use descriptive option names
- Test and save good workflows

---

## Troubleshooting

**Nodes don't appear:**
- Check folder is in `ComfyUI/custom_nodes/`
- File must be named `__init__.py`
- Restart ComfyUI completely

**Library doesn't show:**
- Check JSON file in `libraries/` folder
- Validate JSON syntax
- All 6 blocks must exist (can be empty: `{}`)

**Slow generation:**
- This shouldn't happen with clean architecture
- Check your KSampler settings
- Verify CLIP isn't loading repeatedly

---

## Key Files

```
__init__.py              # ComfyUI node
engine/composer.py       # Core logic
schema/connector.json    # Rules and settings
libraries/*.json         # Your theme data
```

**To customize:**
- Libraries → Add/edit theme data
- Schema → Change weights/order/formatting
- Engine/Node → You shouldn't need to touch these

---

## Support

**Read the docs:**
- `ARCHITECTURE.md` - How it works
- `README.md` - Project overview

**Common issues:**
- Library switching not working → This version FIXES that
- Generation too slow → Clean architecture should fix this
- Want more control → Edit `schema/connector.json`

---

Your cat-approved, production-ready prompt system. 😺
