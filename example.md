# scaling guide

## current system

300+ options across 17 categories.

all alphabetically sorted.

"None" option skips blocks.

## adding more options

### from reference docs

you have:
- AngleShot.txt (100+ angles)
- HairColors.txt (40 colors)
- HairTexturesStyle.txt (200+ styles)
- Outfits.txt (50+ outfits)
- RevealingOutfit.txt (100+ variations)
- SexyPoses.txt (200+ poses)
- LocationsIndoor.txt (300+ locations)
- Atmospheres.txt (100+ atmospheres)
- Filters.txt (40 filters)
- etc.

### parse and add

edit `libraries/comprehensive_portrait.json`:

```json
"angle": {
  "Ceiling Shot": "ceiling-mounted camera angle looking down",
  "Extreme Low Angle": "extreme low angle from ground",
  "Helicopter Shot": "aerial helicopter perspective"
}
```

add as many as needed.

alphabetical sorting happens automatically.

### multi-library approach

if one lib gets too big (1000+ options), split by context:

```
portrait_casual.json    → everyday looks
portrait_formal.json    → elegant/professional
portrait_fantasy.json   → magical/ethereal
portrait_cyberpunk.json → neon/tech
```

switch library dropdown to change context.

## "None" handling

selecting "None" = blank = skip that block.

example:
- hair_ornament: "None" → no ornament text in prompt
- outfit_detail: "None" → just outfit, no detail

clean composition.

## current scale

17 categories × ~20 avg options = 340 selections

can scale to:
17 categories × 100 options = 1700 selections

or add more categories:
25 categories × 50 options = 1250 selections

system handles any scale.

## alphabetical advantage

with 100 options, alphabetical makes sense:

```
A-D: 25 options
E-H: 25 options  
I-L: 25 options
M-Z: 25 options
```

easy to scan.

no search needed if well-organized.
