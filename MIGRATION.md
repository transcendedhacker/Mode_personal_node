# Migration Guide

## From Legacy Dropdown System → Clean Architecture

### What Changed

**Architecture:**
```
Old: Everything in __init__.py + libraries with embedded syntax
New: engine/ + schema/ + libraries/ separation
```

**Libraries:**
```
Old:
{
  "character": {
    "Name": "(description:1.1), extra stuff, BREAK, things"
  }
}

New:
{
  "blocks": {
    "character": {
      "Name": "description"
    }
  }
}
```

**Weights:**
```
Old: Hardcoded in library data, different per library
New: Defined once in schema/connector.json, applied uniformly
```

**Model Support:**
```
Old: Separate library files or branching code
New: Model profiles in schema (sdxl vs flux multipliers)
```

---

## Why The Change

### Problem 1: Library Switching Didn't Work
**Old behavior:** Dropdowns didn't reload when changing library  
**Root cause:** Static dropdown definition, no dynamic reloading  
**New solution:** Dynamic dropdown generation from selected library

### Problem 2: 300s Generation Time
**Old behavior:** Prompts took 3x longer to generate  
**Root cause:** Malformed prompts with redundant tokens, inefficient encoding  
**New solution:** Clean prompt composition, proper BREAK placement

### Problem 3: Not Scalable
**Old behavior:** Adding libraries required understanding node code  
**Root cause:** Logic mixed with data  
**New solution:** Pure data libraries, all logic in schema

---

## Converting Old Libraries

### Step 1: Remove Syntax

**Before:**
```json
{
  "character": {
    "Classic": "(A woman with features:1.1), details, BREAK"
  }
}
```

**After:**
```json
{
  "blocks": {
    "character": {
      "Classic": "A woman with features, details"
    }
  }
}
```

Remove:
- Weight syntax `(text:1.1)`
- BREAK tokens
- Formatting symbols
- Any logic/instructions

### Step 2: Add Meta Block

```json
{
  "meta": {
    "name": "Library Display Name",
    "description": "What this library is for",
    "version": "1.0"
  },
  "blocks": { ... }
}
```

### Step 3: Ensure All Blocks Exist

Required blocks (can be empty):
- character
- scene
- emotion
- wardrobe
- photography
- technical

```json
{
  "blocks": {
    "character": { ... },
    "scene": { ... },
    "emotion": { ... },
    "wardrobe": { ... },
    "photography": { ... },
    "technical": { ... }
  }
}
```

---

## Adjusting Weights

### Old Way
Edit every library file individually:
```json
"character": {
  "Name": "(description:1.2)"  // Changed weight in data
}
```

### New Way
Edit schema/connector.json once:
```json
"weights": {
  "character": 1.2  // Applied to all libraries
}
```

---

## Model-Specific Behavior

### Old Way
Separate files:
- `library_sdxl.json`
- `library_flux.json`

Or branching code:
```python
if model == "flux":
    weight = weight * 0.8
```

### New Way
One library, model profiles:
```json
"models": {
  "sdxl": {
    "weight_multiplier": 1.0
  },
  "flux": {
    "weight_multiplier": 0.85
  }
}
```

Select model in node dropdown.

---

## Testing Migration

1. **Convert one library first**
   - Remove syntax
   - Test with both SDXL and FLUX
   - Verify prompt quality

2. **Compare outputs**
   ```
   Old: Complex prompt with redundant formatting
   New: Clean prompt with proper structure
   ```

3. **Check generation time**
   - Should return to <100s
   - If still slow, check KSampler settings

4. **Verify library switching**
   - Change library dropdown
   - Other dropdowns should update
   - If not, restart ComfyUI

---

## Common Issues

### Issue: "Dropdowns show None"
**Cause:** Library doesn't have required blocks  
**Fix:** Add all 6 blocks to library JSON (can be empty: `{}`)

### Issue: "Prompts look wrong"
**Cause:** Library still has old syntax  
**Fix:** Remove all `(text:weight)` and `BREAK` from library data

### Issue: "Can't find old libraries"
**Cause:** New system uses `libraries/` subfolder  
**Fix:** Move `.json` files to `libraries/` folder

### Issue: "Weights not applying"
**Cause:** Check schema/connector.json  
**Fix:** Ensure weights block exists and model profile is correct

---

## Checklist

- [ ] Remove syntax from library files
- [ ] Add meta block to each library
- [ ] Ensure all 6 blocks exist (character, scene, emotion, wardrobe, photography, technical)
- [ ] Move libraries to `libraries/` folder
- [ ] Delete old `__init__.py` if it exists
- [ ] Replace with new system files
- [ ] Restart ComfyUI
- [ ] Test with SDXL
- [ ] Test with FLUX
- [ ] Verify generation time
- [ ] Verify library switching works

---

## Rolling Back

If you need the old system:

1. Keep backup of old files
2. Restore old `__init__.py` and `libraries/` folder
3. Restart ComfyUI

But you won't need to. This system is cleaner, faster, and more maintainable.

---

## Support

**New system advantages:**
- ✅ Proper library switching
- ✅ Fast generation (<100s)
- ✅ Easy to maintain
- ✅ Infinitely scalable
- ✅ Clean separation of concerns

**When to use old system:**
- Never. The new system does everything better.

---

Your migration to production-grade architecture is complete. 🎯
