# v2.0 - massive scale implementation

## what changed

### before (v1)
- 5-10 options per category
- full sentences in dropdowns
- 80 total selections

### after (v2)
- 300+ atomic options
- 17 categories
- alphabetically sorted
- "None" skips blocks

## structure

```
comprehensive_portrait.json:
- subject (5)
- age (7)  
- hair_color (27)
- hair_style (22)
- hair_ornament (14)
- outfit (29)
- outfit_detail (10)
- pose (20)
- mood (15)
- location (15)
- location_detail (10)
- atmosphere (15)
- lighting (14)
- angle (18)
- frame (10)
- filter (15)
- technical (12)

total: 258 options in one library
```

## features

### alphabetical sorting
all dropdowns auto-sorted A-Z.
"None" always first.

### "None" behavior
selecting "None" = skip block entirely.
no blank text, just omitted from composition.

### clean composition
atomic parts → weighted → BREAK placement → final prompt.

example:
```
User selects:
- subject: "Woman"
- age: "23-27"
- hair_color: "Platinum Blonde"
- outfit: "Silk Slip Dress"
- pose: "Over Shoulder"

Output:
"A woman 23-27 years old with platinum blonde hair, wearing red silk slip dress, 
(turning back to camera, looking over shoulder:1.2), ..."
```

### scalability
current: 258 options
can add 1000s more by:
- expanding existing blocks
- adding new categories
- creating specialized libs

## how to scale

### parse reference docs

you provided:
- HairColors.txt → add all 40 colors
- AngleShot.txt → add all 100+ angles
- Outfits.txt → add all options
- SexyPoses.txt → add all 200+ poses
- LocationsIndoor.txt → add all 300+ locations

just edit json, add entries, restart.

### alphabetical advantage

with 100 options in dropdown:
- still easy to scan A-Z
- no search needed
- predictable location

### multi-library strategy

if one lib hits 1000+ options, split by context:
- portrait_casual
- portrait_formal  
- portrait_alternative
- portrait_fantasy

switch library = switch context.

## comfyui limitation

dropdowns can't dynamically update based on other selections.

so "outfit: dress" can't auto-filter "outfit_detail" to dress-specific options.

workaround:
- comprehensive libs with all combos
- or specialized libs for contexts


expand from your reference docs:
1. add all hair colors (27 → 40)
2. add all angles (18 → 100+)
3. add all poses (20 → 200+)
4. add all locations (15 → 300+)
5. add all atmospheres (15 → 100+)

system handles any scale.

alphabetical + "None" = clean navigation.

atomic composition = fast clean prompts.

